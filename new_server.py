"""
Hi
"""

import sys

import json
import os

# import argparse

import re

from urllib.parse import unquote

# import random
from http.server import HTTPServer, BaseHTTPRequestHandler

# import numpy as np

# import fire
import pymongo
from pymongo.errors import ServerSelectionTimeoutError

# import http.server
# import socketserver


import model
import sample
import encoder

# import tensorflow as tf
import tensorflow.compat.v1 as tf

tf.disable_v2_behavior()


def get_final_text_from_response(response):
    """
    Documentation
    """
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
    return final_text


def get_settings_from_argv():
    """
    Documentation
    """
    settings = {}

    if len(sys.argv) > 5:
        settings["gpu_flag"] = int(sys.argv[1])
        settings["mongo_address"] = sys.argv[2]
        settings["mongo_port"] = int(sys.argv[3])
        settings["listen_address"] = sys.argv[4]
        settings["listen_port"] = int(sys.argv[5])
    else:
        settings["gpu_flag"] = 0
        settings["mongo_address"] = "localhost"
        settings["mongo_port"] = 27017
        settings["listen_address"] = "localhost"
        settings["listen_port"] = 8008

    if settings["gpu_flag"] == 0:
        print("----Running in CPU mode")
        # import tensorflow as tf
    elif settings["gpu_flag"] == 1:
        print("----Running in GPU mode")
        # import tensorflow-gpu as tf
    else:
        raise ValueError("Unexpected value for gpu_flag")

    return settings


def get_db_posts(mongo_address, mongo_port):
    """
    README
    """
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
    return posts


def get_question_id_and_raw_text(id_and_question):
    """
    Documentation
    """
    id_end = str.find(id_and_question, "|")

    question_id = id_and_question[:id_end]
    raw_text = id_and_question[id_end + 1 :]

    return (question_id, raw_text)


def run(
    server_class,
    handler_class,
    addr,
    port,
):
    """
    Documentation
    """
    addr = ""
    server_address = (addr, port)
    print("here?")
    print(addr)
    print(port)
    print("done")
    httpd = server_class(server_address, handler_class)

    # print_string = "Starting httpd server on " + str(addr) + ":" + str(port)
    # print(f"Starting httpd server on {addr}:{port}")
    print("Starting httpd server on " + str(addr) + ":" + str(port))
    httpd.serve_forever()


def get_config(gpu_flag):
    """
    Documentation
    """
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
    return config


def interact_model(
    *,
    posts,
    gpu_flag,
    listen_address,
    listen_port,
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
    model_name = "econstormodel"
    # seed = None
    # nsamples = 1
    batch_size = 1
    # length = None

    # if batch_size is None:
    #    batch_size = 1

    # if nsamples % batch_size != 0:
    #    raise ValueError(
    #        f"nsamples ({nsamples}) must be a multiple of batch_size ({batch_size})."
    #    )
    # assert nsamples % batch_size == 0
    # this_dir = os.path.join("models")
    enc = encoder.get_encoder(model_name, "./models")
    hparams = model.default_hparams()
    with open(
        os.path.join("models", model_name, "hparams.json"), encoding="utf-8"
    ) as f:
        hparams.override_from_dict(json.load(f))
    # if length is None:
    #    length = hparams.n_ctx // 2
    # elif length > hparams.n_ctx:
    #    raise ValueError(f"Can't get samples longer than window size: {hparams.n_ctx}")
    # length = hparams.n_ctx // 2
    # config = get_config(gpu_flag)

    with tf.Session(graph=tf.Graph(), config=get_config(gpu_flag)) as sess:
        print("!!!4")
        context = tf.placeholder(tf.int32, [batch_size, None])
        # random.seed(seed)
        # tf.set_random_seed(seed)
        # random.seed()
        # tf.set_random_seed()
        output = sample.sample_sequence(
            hparams=hparams,
            length=hparams.n_ctx // 2,
            context=context,
            batch_size=batch_size,
            temperature=1,
            top_k=40,
            top_p=0.9,
        )
        saver = tf.train.Saver()
        ckpt = tf.train.latest_checkpoint(os.path.join("models", model_name))
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

            # Note pylint is disabled on the following because pylint wants do_get and BaseHTTPRequestHandler needs it to be as it is
            def do_GET(self):  # pylint: disable=invalid-name
                """
                Documentation
                """
                self._set_headers()
                question_id, raw_text = get_question_id_and_raw_text(
                    unquote(self.path[1:])
                )
                # id_and_question = unquote(self.path[1:])
                # id_end = str.find(id_and_question, "|")

                # question_id = id_and_question[:id_end]
                # raw_text = id_and_question[id_end + 1 :]
                # raw_text = unquote(self.path[1:])
                if len(raw_text) > 50:
                    raw_text = raw_text[:50]
                print("----GOT QUESTION----")
                print(question_id)
                print(raw_text)
                context_tokens = enc.encode(raw_text)

                out = sess.run(
                    output,
                    feed_dict={context: [context_tokens for _ in range(batch_size)]},
                )[:, len(context_tokens) :]

                # text = enc.decode(out[0])

                # response = text
                response = enc.decode(out[0])
                print("----GOT RESPONSE----")
                print("Question is:")
                print(raw_text)
                print("Response is:")
                print(response)
                response = get_final_text_from_response(response)

                print("Final text is:")
                print(response)
                # self.wfile.write(self._html("hi!"))
                # self.wfile.write(response.encode(encoding='utf_8'))
                print("---SENT!----\n\n")
                post_data = {
                    "id": question_id,
                    "question": raw_text,
                    "response": response,
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

            # Note pylint is disabled on the following because pylint wants do_get and BaseHTTPRequestHandler needs it to be as it is
            def do_HEAD(self):  # pylint: disable=invalid-name
                """
                Documentation
                """
                self._set_headers()

            # Note pylint is disabled on the following because pylint wants do_get and BaseHTTPRequestHandler needs it to be as it is
            def do_POST(self):  # pylint: disable=invalid-name
                """
                Doesn't do anything with posted data
                """
                self._set_headers()
                self.wfile.write(self._html("POST!"))

        # def run(
        #    server_class=HTTPServer,
        #    handler_class=S,
        #    addr=listen_address,
        #    port=listen_port,
        # ):
        #    addr = ""
        #    server_address = (addr, port)
        #    print("here?")
        #    print(addr)
        #    print(port)
        #    print("done")
        #    httpd = server_class(server_address, handler_class)

        #    # print_string = "Starting httpd server on " + str(addr) + ":" + str(port)
        #    # print(f"Starting httpd server on {addr}:{port}")
        #    print("Starting httpd server on " + str(addr) + ":" + str(port))
        #    httpd.serve_forever()

        # parser = argparse.ArgumentParser(description="Run a simple HTTP server")
        # parser.add_argument(
        #    "-l",
        #    "--listen",
        #    # default="localhost",
        #    default=listen_address,
        #    help="Specify the IP address on which the server listens",
        # )
        # parser.add_argument(
        #    "-p",
        #    "--port",
        #    type=int,
        #    default=listen_port,
        #    help="Specify the port on which the server listens",
        # )
        # args = parser.parse_args()
        # listen_address,
        # listen_port,

        # run(addr=args.listen, port=args.port)
        # server_class=HTTPServer,
        # handler_class=S,

        run(
            server_class=HTTPServer,
            handler_class=S,
            addr=listen_address,
            port=listen_port,
        )


def main():
    """
    Document
    """
    settings = get_settings_from_argv()
    print("SETTINGS ARE")
    print(settings)
    posts = get_db_posts(
        mongo_address=settings["mongo_address"], mongo_port=settings["mongo_port"]
    )
    # fire.Fire(interact_model)
    # fire.Fire(
    #    lambda: interact_model(
    #        posts=posts,
    #        gpu_flag=settings["gpu_flag"],
    #        listen_address=settings["listen_address"],
    #        listen_port=settings["listen_port"],
    #    )
    # )
    interact_model(
        posts=posts,
        gpu_flag=settings["gpu_flag"],
        listen_address=settings["listen_address"],
        listen_port=settings["listen_port"],
    )


if __name__ == "__main__":
    main()
