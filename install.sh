#!/usr/bin/env bash
rm -r build/
python setup.py build
sudo python setup.py install
