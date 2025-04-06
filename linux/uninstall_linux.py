import subprocess
import os
from pathlib import Path

def remove_cron():
    try:
        script_dir = Path(__file__).parent.absolute()
        shell_script = script_dir / "run_caitgfeed.sh"
        
        # Get current crontab
        current_crontab = subprocess.check_output(['crontab', '-l']).decode()
        
        # Remove our specific cron job
        new_crontab = '\n'.join(line for line in current_crontab.splitlines() 
                               if str(shell_script) not in line)
        
        # Update crontab
        subprocess.run(['crontab', '-'], input=new_crontab.encode())
        
        # Remove the shell script if it exists
        if shell_script.exists():
            os.remove(shell_script)
            
        print("✅ Cron job removed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    remove_cron()