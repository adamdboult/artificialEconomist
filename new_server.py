#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import fire
import json
import os
import numpy as np
import tensorflow as tf

from urllib.parse import unquote

#import http.server
#import socketserver

import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler


import model, sample, encoder


#file_path = os.path.dirname(os.path.abspath(__file__))
#dest_path = os.path.join(file_path, "..")
#print("4")
#print(dest_path)
#print("5")
#os.chdir(dest_path)
#os.chdir("./gpt-2")



def interact_model(
    model_name='117M',
    #model_name='myModel',
    seed=None,
    nsamples=1,
    batch_size=1,
    length=None,
    temperature=1,
    top_k=40,
#    top_k=0,
    top_p=0.0,
#    top_p=0.0,
    raw_text="t"
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

    if batch_size is None:
        batch_size = 1
    assert nsamples % batch_size == 0
    print ("here")

    enc = encoder.get_encoder(model_name)
    hparams = model.default_hparams()
    with open(os.path.join('models', model_name, 'hparams.json')) as f:
        hparams.override_from_dict(json.load(f))
    print ("step 2")
    if length is None:
        length = hparams.n_ctx // 2
    elif length > hparams.n_ctx:
        raise ValueError("Can't get samples longer than window size: %s" % hparams.n_ctx)
    print ("!!!3")

    # Keep this as 0 to force CPU.
    config = tf.ConfigProto(
        device_count = {'GPU': 0}
    )
    #sess = tf.Session(config=config)
    #with tf.Session(graph=tf.Graph()) as sess:
    with tf.Session(graph=tf.Graph(), config=config) as sess:
        print ("!!!4")
        context = tf.placeholder(tf.int32, [batch_size, None])
        np.random.seed(seed)
        tf.set_random_seed(seed)
        output = sample.sample_sequence(
            hparams=hparams, length=length,
            context=context,
            batch_size=batch_size,
            temperature=temperature, top_k=top_k, top_p=top_p
        )
        print ("!!!5")
        saver = tf.train.Saver()
        ckpt = tf.train.latest_checkpoint(os.path.join('models', model_name))
        print(saver)
        print(sess)
        print(ckpt)
        saver.restore(sess, ckpt)




        class S(BaseHTTPRequestHandler):
            def _set_headers(self):
                self.send_response(200)
                #self.send_header("Content-type", "text/html")
                self.send_header("Content-type", "application/json")
                self.end_headers()

            def _html(self, message):
                """This just generates an HTML document that includes `message`
                in the body. Override, or re-write this do do more interesting stuff.
                """
                content = f"<html><body><h1>{message}</h1></body></html>"
                return content.encode("utf8")  # NOTE: must return a bytes object!

            def do_GET(self):
                print("START")
                print(self.path)
                print("END")
                self._set_headers()

                raw_text = unquote(self.path[1:])
                print(raw_text)
                #response = self._html("hi!")
                response = "this is text: " + raw_text


                context_tokens = enc.encode(raw_text)
                generated = 0
                print ("!!!7")
                #for _ in range(nsamples // batch_size):
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

                #print ("!!!8")
                #output = sample.sample_sequence(
                #    hparams     = hparams, 
                #    length      = length,
                #    context     = context,
                #    batch_size  = batch_size,
                #    temperature = temperature, 
                #    top_k       = top_k, 
                #    top_p       = top_p
                #)

                out = sess.run(output, feed_dict={
                    context: [context_tokens for _ in range(batch_size)]
                })[:, len(context_tokens):]
                print ("!!!9")
                print(out)

                text = enc.decode(out[0])
                #print("=" * 40 + " SAMPLE " + str(generated) + " " + "=" * 40)
                #print(text)

                response = text
                print("Response is:")
                print(response)

                #self.wfile.write(self._html("hi!"))
                self.wfile.write(response.encode(encoding='utf_8'))
                print("---SENT!----\n\n")

            def do_HEAD(self):
                self._set_headers()

            def do_POST(self):
                # Doesn't do anything with posted data
                self._set_headers()
                self.wfile.write(self._html("POST!"))


        def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=8000):
            server_address = (addr, port)
            httpd = server_class(server_address, handler_class)

            print(f"Starting httpd server on {addr}:{port}")
            httpd.serve_forever()


        #if __name__ == "__main__":

        parser = argparse.ArgumentParser(description="Run a simple HTTP server")
        parser.add_argument(
            "-l",
            "--listen",
            default="localhost",
            help="Specify the IP address on which the server listens",
        )
        parser.add_argument(
            "-p",
            "--port",
            type=int,
            default=8000,
            help="Specify the port on which the server listens",
        )
        args = parser.parse_args()
        run(addr=args.listen, port=args.port)
	







if __name__ == '__main__':
    fire.Fire(interact_model)




