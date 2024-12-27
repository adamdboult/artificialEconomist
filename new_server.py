"""
Hi
"""

import sys

import json
import os
import argparse

import re

from urllib.parse import unquote
import random
from http.server import HTTPServer, BaseHTTPRequestHandler

# import numpy as np

import fire
import pymongo
from pymongo.errors import ServerSelectionTimeoutError

# import http.server
# import socketserver


import model, sample, encoder

import tensorflow as tf

if len(sys.argv) > 1:
    gpu_flag = int(sys.argv[1])
    # gpu_flag = 1
else:
    gpu_flag = 0

if gpu_flag == 0:
    print("----Running in CPU mode")
    # import tensorflow as tf
elif gpu_flag == 1:
    print("----Running in GPU mode")
    # import tensorflow-gpu as tf
else:
    raise ValueError("Unexpected value for gpu_flag")

if len(sys.argv) > 2:
    mongo_address = sys.argv[2]
else:
    mongo_address = "localhost"

if len(sys.argv) > 3:
    mongo_port = int(sys.argv[3])
else:
    mongo_port = 27017

if len(sys.argv) > 4:
    listen_address = sys.argv[4]
else:
    listen_address = "localhost"

if len(sys.argv) > 5:
    listen_port = sys.argv[5]
else:
    listen_port = 8008


# sys.path.insert(1, '/home/adam/Projects/artificialEconomist/gpt-2/src')


# import os
# file_path = os.path.dirname(os.path.abspath(__file__))
# os.chdir(file_path)
# os.chdir("./gpt-2")


# file_path = os.path.dirname(os.path.abspath(__file__))
# dest_path = os.path.join(file_path, "..")
# print("4")
# print(dest_path)
# print("5")
# os.chdir(dest_path)
# os.chdir("./gpt-2")

# mongo_client = pymongo.MongoClient('localhost', 27518)
print("before")
mongo_client = pymongo.MongoClient(mongo_address, mongo_port)
print("after")


my_db = mongo_client.pymongo_test
posts = my_db.posts
post_data_test = {
    "title": "Python and MongoDB",
    "content": "Artificial Economist data",
    "author": "Adam",
}
print("a")
try:
    result_test = posts.insert_one(post_data_test)
    # print("One post: {0}".format(result.inserted_id))
    print(f"One post: {result_test.inserted_id}")
    print(result_test)
    print("done")
except ServerSelectionTimeoutError:
    print("Not posting. No server")
# except Exception as e:
#    # Catch other exceptions and log them
#    print(f"An unexpected error occurred: {e}")
# result_test = posts.insert_one(post_data_test)
# print(f"One post: {result_test.inserted_id}")
# try:
#    result = posts.insert_one(post_data_test)
#    print(f"One post: {result.inserted_id}")
# except:
#    print("Not posting. No server")


def interact_model(
    model_name="econstormodel",
    # model_name='117M',
    # model_name='myModel',
    seed=None,
    nsamples=1,
    batch_size=1,
    length=None,
    temperature=1,
    top_k=40,
    # top_k=0,
    top_p=0.9,
    # top_p=0.0,
    # raw_text="t",
):
    """
    Interactively run the model
    :model_name=117M : String, which model to use
    :seed=None : Integer seed for random number generators, fix seed to reproduce
     results
    :nsamples=1 : Number of samples to return total
    :batch_size=1 : Number of batches (only affects speed/memory).  Must divide nsamples.
    :length=None : Number of tokens in generated text, if None (default), is
     determined by model hyperparameters
    :temperature=1 : Float value controlling randomness in boltzmann
     distribution. Lower temperature results in less random completions. As the
     temperature approaches zero, the model will become deterministic and
     repetitive. Higher temperature results in more random completions.
    :top_k=0 : Integer value controlling diversity. 1 means only 1 word is
     considered for each step (token), resulting in deterministic completions,
     while 40 means 40 words are considered at each step. 0 (default) is a
     special setting meaning no restrictions. 40 generally is a good value.
    :top_p=0.0 : Float value controlling diversity. Implements nucleus sampling,
     overriding top_k if set to a value > 0. A good setting is 0.9.
    """
    print("Starting function")
    print(batch_size)
    print(type(batch_size))
    if batch_size is None:
        batch_size = 1
    print(batch_size)
    print(type(batch_size))
    print(nsamples)
    print(type(nsamples))
    print(nsamples % batch_size)

    if nsamples % batch_size != 0:
        raise ValueError(
            f"nsamples ({nsamples}) must be a multiple of batch_size ({batch_size})."
        )
    # assert nsamples % batch_size == 0
    print("here")
    this_dir = os.path.join("models")
    print(this_dir)
    print(os.getcwd())
    enc = encoder.get_encoder(model_name, "./models")
    hparams = model.default_hparams()
    with open(
        os.path.join("models", model_name, "hparams.json"), encoding="utf-8"
    ) as f:
        hparams.override_from_dict(json.load(f))
    print("step 2")
    if length is None:
        length = hparams.n_ctx // 2
    elif length > hparams.n_ctx:
        raise ValueError(f"Can't get samples longer than window size: {hparams.n_ctx}")
    print("!!!3")

    # Keep this as 0 to force CPU.
    # gpu_mode = 0
    if gpu_flag == 0:
        config = tf.ConfigProto(
            device_count={"GPU": 0}
            # device_count = {'GPU': 1}
        )
    else:
        config = tf.ConfigProto(
            # device_count = {'GPU': 0}
            device_count={"GPU": 1}
            # https://forums.developer.nvidia.com/t/tensorflow-gpu-not-working-in-nano/82171/2
        )
        config.gpu_options.allow_growth = True
        config.gpu_options.per_process_gpu_memory_fraction = 0.4

    # sess = tf.Session(config=config)
    # with tf.Session(graph=tf.Graph()) as sess:
    with tf.Session(graph=tf.Graph(), config=config) as sess:
        print("!!!4")
        context = tf.placeholder(tf.int32, [batch_size, None])
        # np.random.seed(seed)
        random.seed(seed)
        tf.set_random_seed(seed)
        output = sample.sample_sequence(
            hparams=hparams,
            length=length,
            context=context,
            batch_size=batch_size,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
        )
        print("!!!5")
        saver = tf.train.Saver()
        ckpt = tf.train.latest_checkpoint(os.path.join("models", model_name))
        print(saver)
        print(sess)
        print(ckpt)
        saver.restore(sess, ckpt)

        class S(BaseHTTPRequestHandler):
            """
            Documentation todo
            """

            def _set_headers(self):
                self.send_response(200)
                # self.send_header("Content-type", "text/html")
                self.send_header("Content-type", "application/json")
                self.end_headers()

            def _html(self, message):
                """
                This just generates an HTML document that includes `message`
                in the body. Override, or re-write this do do more interesting stuff.
                """
                new_content_string = (
                    "<html><body><h1>" + message + "</h1></body></html>"
                )
                # content = f"<html><body><h1>{message}</h1></body></html>"
                content = new_content_string
                return content.encode("utf8")  # NOTE: must return a bytes object!

            def do_GET(self):
                """
                Documentation
                """
                self._set_headers()

                id_and_question = unquote(self.path[1:])
                id_end = str.find(id_and_question, "|")

                question_id = id_and_question[:id_end]
                raw_text = id_and_question[id_end + 1 :]
                # raw_text = unquote(self.path[1:])
                if len(raw_text) > 50:
                    raw_text = raw_text[:50]
                print("----GOT QUESTION----")
                # print(id_and_question)
                print(question_id)
                print(raw_text)

                context_tokens = enc.encode(raw_text)
                # generated = 0
                # print ("!!!7")
                # for _ in range(nsamples // batch_size):
                #    print ("!!!8")
                #    out = sess.run(output, feed_dict={
                #        context: [context_tokens for _ in range(batch_size)]
                #    })[:, len(context_tokens):]
                #    print ("!!!9")
                #    for i in range(batch_size):
                #        generated += 1
                #        text = enc.decode(out[i])
                ##        #print("=" * 40 + " SAMPLE " + str(generated) + " " + "=" * 40)
                #        print(text)

                # print ("!!!8")
                # output = sample.sample_sequence(
                #    hparams     = hparams,
                #    length      = length,
                #    context     = context,
                #    batch_size  = batch_size,
                #    temperature = temperature,
                #    top_k       = top_k,
                #    top_p       = top_p
                # )

                out = sess.run(
                    output,
                    feed_dict={context: [context_tokens for _ in range(batch_size)]},
                )[:, len(context_tokens) :]
                # print ("!!!9")
                # print("Got answer:")
                # print(out)

                text = enc.decode(out[0])
                # print("=" * 40 + " SAMPLE " + str(generated) + " " + "=" * 40)
                # print(text)

                response = text
                print("----GOT RESPONSE----")
                print("Question is:")
                print(raw_text)
                print("Response is:")
                print(response)
                end_of_text = "<|endoftext|>"
                position = str.find(response, end_of_text)

                if position >= 0:
                    response = response[:position]

                response_list = response.split(".\n")

                final_text = ""

                for item in response_list:
                    item = item.replace("\n", " ")
                    item = item.replace("\t", " ")
                    # item = item.replace("\s", " ")
                    item = re.sub(r"\s", " ", item)  # Replace all whitespace with space
                    item = re.sub(
                        r" {2,}", " ", item
                    )  # Replace multiple spaces with a single space
                    item = item + "."
                    item = item.replace("..", ".")
                    # item = item.replace("  ", " ")
                    # item = item.replace("  ", " ")
                    # item = item.replace("  ", " ")
                    item = item.replace(" .", ".")
                    item = item.strip()  # Remove trailing and leading whitespace

                    final_text = final_text + item + "\n\n"

                print("Final text is:")
                print(final_text)
                # self.wfile.write(self._html("hi!"))
                # self.wfile.write(final_text.encode(encoding='utf_8'))
                print("---SENT!----\n\n")
                post_data = {
                    "id": question_id,
                    "question": raw_text,
                    "response": final_text,
                }
                try:
                    result = posts.insert_one(post_data)
                    # print("One post: {0}".format(result.inserted_id))
                    print(f"One post: {result.inserted_id}")
                    print(result)
                    print("done")
                except ServerSelectionTimeoutError:
                    print("Not posting. No server")
                # except Exception as e:
                #    # Catch other exceptions and log them
                #    print(f"An unexpected error occurred: {e}")

            def do_HEAD(self):
                """
                Documentation
                """
                self._set_headers()

            def do_POST(self):
                """
                Doesn't do anything with posted data
                """
                self._set_headers()
                self.wfile.write(self._html("POST!"))

        # def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=listen_port):
        # def run(server_class=HTTPServer, handler_class=S, addr="artificialeconomist_tensorflow", port=listen_port):
        def run(
            server_class=HTTPServer,
            handler_class=S,
            addr=listen_address,
            port=listen_port,
        ):
            addr = ""
            server_address = (addr, port)
            print("here?")
            print(addr)
            print(port)
            print("done")
            httpd = server_class(server_address, handler_class)

            print_string = "Starting httpd server on " + str(addr) + ":" + str(port)
            # print(f"Starting httpd server on {addr}:{port}")
            print(print_string)
            httpd.serve_forever()

        # if __name__ == "__main__":

        parser = argparse.ArgumentParser(description="Run a simple HTTP server")
        parser.add_argument(
            "-l",
            "--listen",
            # default="localhost",
            default=listen_address,
            help="Specify the IP address on which the server listens",
        )
        parser.add_argument(
            "-p",
            "--port",
            type=int,
            default=listen_port,
            help="Specify the port on which the server listens",
        )
        args = parser.parse_args()
        run(addr=args.listen, port=args.port)


sys.argv = [sys.argv[0]]

if __name__ == "__main__":
    fire.Fire(interact_model)
# interact_model()
