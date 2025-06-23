#!/bin/bash

echo "Hello ! This file can only be run in Linux and MacOs ! Sorry Windows users :( )"

if [ -f call_api.py ] && [ -f crypto_tracker.py ] && [ -f requirements.txt ]; then
    echo "Starting the instalation !"
else
    echo "Missing files"
    exit 84
fi

clear

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

clear

echo "All installed ! To run the project please write: streamlit run crypto_tracker.py"
