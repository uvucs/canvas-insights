#! /bin/bash

# Simple script to automate data collection on mac and linux

echo "Before continuing this script, please ensure you have opened a branch and run this file in that branch"

read tmp

echo "Please go to the following url:"
echo "https://uvu.instructure.com/profile/settings"
echo "Click New Access Token, save the token generated, and then input it below"

read -p "Access Token (use ctrl+shift+v to paste): " token

python3 -m venv env
source env/bin/activate

pip install -r requirements.txt

python data_ingestion.py $token

echo "Please push changes and open a pull request"
