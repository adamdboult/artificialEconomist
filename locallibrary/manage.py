#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Django's command-line utility for administrative tasks."""
import os
import sys

import fire
import json
#import os
import numpy as np
import tensorflow as tf

import model, sample, encoder


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'locallibrary.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc





    #model_name='myModel'
    model_name='117M'
    seed=None
    nsamples=1
    batch_size=1
    length=None
    temperature=1
    top_k=0
    top_p=0
    #raw_text="Placeholder text"



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
    with tf.Session(graph=tf.Graph()) as sess:
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
        saver.restore(sess, ckpt)

        #while True:
        #print ("Using:")
        #print (raw_text)

        if 0==1:
            #raw_text = input("Model prompt >>> ")
            #while not raw_text:
            #    print('Prompt should not be empty!')
            #    raw_text = input("Model prompt >>> ")
            print ("!!!6")
            context_tokens = enc.encode(raw_text)
            generated = 0
            print ("!!!7")
            for _ in range(nsamples // batch_size):
                print ("!!!8")
                out = sess.run(output, feed_dict={
                    context: [context_tokens for _ in range(batch_size)]
                })[:, len(context_tokens):]
                print ("!!!9")
                for i in range(batch_size):
                    generated += 1
                    text = enc.decode(out[i])
                    #print("=" * 40 + " SAMPLE " + str(generated) + " " + "=" * 40)
                    print(text)
            #print("=" * 80)





        execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
