import subprocess
from pathlib import Path

def run_caitgfeed():
    try:
        script_dir = Path(__file__).parent.parent
        main_script = script_dir / "main.py"
        
        print("Running CivitAI Telegram Feed...")
        subprocess.run(['python3', str(main_script)])
        print("✅ Execution completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_caitgfeed()