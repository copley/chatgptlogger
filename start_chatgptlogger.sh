#!/bin/bash

# Kill all Chrome instances
pkill -f "Google Chrome"

# Start Chrome with remote debugging
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 &

# Wait a few seconds to ensure Chrome has started
sleep 3

# Activate the Python virtual environment
source ~/myenv/bin/activate

# Run the Python script
python3 chatgptlogger5.py

