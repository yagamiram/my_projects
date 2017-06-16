#!/bin/bash
VENV_DIR=venv
ACTIVATE=$VENV_DIR/bin/activate
REQS=requirements.txt
DEEP_REVERY_KERAS_CONFIG=etc/keras_theano.json
KERAS_HOME=~/.keras
KERAS_CONFIG=$KERAS_HOME/keras.json


virtualenv $VENV_DIR
source $ACTIVATE && pip install -e .
