#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CRON_EXPRESSION="${1:-"0 * * * *"}"  # Use first argument or default to hourly

# Check if requirements are already installed
echo "Checking dependencies..."
if ! pip3 freeze | grep -q -f "$SCRIPT_DIR/requirements.txt"; then
    echo "Installing dependencies..."
    pip3 install -r "$SCRIPT_DIR/requirements.txt"
else
    echo "Dependencies already installed"
fi

# Run the Python setup script with the provided cron expression
echo "Configuring cron job..."
python3 "$SCRIPT_DIR/linux/setup_linux.py" --cron "$CRON_EXPRESSION"