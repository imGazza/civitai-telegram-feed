import os
import subprocess
from pathlib import Path

def setup_cron():
    try:
        # Get absolute path of the script directory
        script_dir = Path(__file__).parent.absolute()
        shell_script = script_dir / "run_caitgfeed.sh"
        main_script = script_dir.parent / "main.py"  # Get main.py from parent directory
        
        # Create the shell script
        shell_content = f'''#!/bin/bash
python3 "../main.py"
'''
        
        with open(shell_script, 'w') as f:
            f.write(shell_content)
        
        # Make both scripts executable
        os.chmod(shell_script, 0o755)
        os.chmod(main_script, 0o755)
        
        # Create cron job
        cron_command = f"0 * * * * {shell_script}\n"
        
        try:
            # Try to get current crontab
            current_crontab = subprocess.check_output(['crontab', '-l']).decode()
        except subprocess.CalledProcessError:
            # If no crontab exists, start with empty one
            current_crontab = ""
        
        if str(shell_script) not in current_crontab:
            new_crontab = current_crontab + cron_command
            subprocess.run(['crontab', '-'], input=new_crontab.encode())
            print("✅ Cron job set up successfully!")
        else:
            print("Cron job already exists!")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    setup_cron()