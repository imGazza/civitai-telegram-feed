# CivitAi Telegram Feed

Periodically retrieves images posted by designated users via the CivitAi API and sends them through a configurable Telegram bot.

## Common Setup Steps

 - Be sure to have Python installed and pip in your PATH.
 - Open `script_config_example.yaml` file and fill the configuration details as needed.
 - **IMPORTANT** Rename the file to `script_config.yaml`.

## Setup Windows

 - Run `setup_windows.bat` to install required dependencies and configure execution environment.
 - Create a Task Scheduler task to run the script periodically as desired for file `run_caitgfeed.vbs`.

## Setup Linux

 - Make the setup script executable: `chmod +x setup_linux.sh`.
 - Run the setup script: `./setup_linux.sh`. It already creates a cron job to run the script periodically. Default is once per hour. It's possible to customize it by adding the cron expression as parameter. (e.g. `./setup_linux.sh "*/30 * * * *"`)

## Uninstall for Linux

 - Make the uninstall script executable: `chmod +x uninstall_linux.sh`.
 - Run the uninstall script: `./uninstall_linux.sh`. It removes the cron job created by the setup script.