import subprocess
import datetime
import json
import os
import glob

def run_manim_foreground():
    """
    Runs the Manim command in the foreground for each JSON script in the scripts folder.
    """
    all_script_files = glob.glob(os.path.join("scripts", "*.json"))

    done_file = os.path.join("scripts", "done.txt")
    processed_files = []
    if os.path.exists(done_file):
        with open(done_file, 'r') as f:
            processed_files = [os.path.join("scripts", line.strip()) for line in f.readlines()]

    # Normalize paths for comparison
    processed_files = [os.path.normpath(p) for p in processed_files]
    all_script_files = [os.path.normpath(p) for p in all_script_files]

    script_files = sorted([f for f in all_script_files if f not in processed_files])
    
    if not script_files:
        print("No new JSON script files found to process.")
        return

    for script_file in script_files:
        print(f"--- Processing script: {script_file} ---")

        # Load the content of the script file and dump it into test.json
        try:
            with open(script_file, 'r') as f_in:
                data = json.load(f_in)
            with open('test.json', 'w') as f_out:
                json.dump(data, f_out, indent=2)
            print(f"Successfully dumped content from {script_file} to test.json")
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error processing {script_file}: {e}")
            continue

        # Generate a timestamp and a script-specific filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        script_name = os.path.splitext(os.path.basename(script_file))[0]
        video_filename = f"{script_name}.mp4"
        log_filename = os.path.join("logs", f"manim_log_{script_name}_{timestamp}.txt")

        # Construct the Manim command
        command = [
            "manim",
            "-ql",
            "main.py",
            "Video",
            "-o",
            video_filename,
        ]

        # Run the command in the foreground
        print(f"Starting Manim rendering...")
        print(f"Output file: {video_filename}")
        print(f"Log file: {log_filename}")
        print(f"Command: {' '.join(command)}")
        
        try:
            with open(log_filename, "w", encoding="utf-8") as log_file:
                result = subprocess.run(command, stdout=log_file, stderr=subprocess.STDOUT, text=True, check=False)
            
            if result.returncode == 0:
                print(f"Manim rendering for {script_file} completed successfully.")
            else:
                print(f"Manim rendering for {script_file} failed. See {log_filename} for details.")
        except FileNotFoundError:
            print("Error: 'manim' command not found. Make sure Manim is installed and in your PATH.")
            break # Stop processing if manim is not found
        except Exception as e:
            print(f"An error occurred while running Manim: {e}")

        # Add the processed file to done.txt
        with open(done_file, 'a') as f:
            f.write(os.path.basename(script_file) + '\n')
        
        print("-" * 50 + "\n")

if __name__ == "__main__":
    run_manim_foreground()
