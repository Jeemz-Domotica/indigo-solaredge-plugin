#!/bin/bash

curl https://bootstrap.pypa.io/pip/2.7/get-pip.py -o ~/Downloads/get-pip.py
python --version

sudo python ~/Downloads/get-pip.py
python -m pip --version

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
pip install -r requirements.txt

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"



