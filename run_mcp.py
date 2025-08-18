from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Video Generation")

@mcp.tool("generate_video")
def generate_video(json_data: dict) -> str:
    """
    Generate a video from the given JSON object.
    
    Args:
        json_data (dict): Tutorial data as a JSON object.
        
    Returns:
        str: Path to the generated video file, PID of the Manim rendering process, and path to the log file.
    """
    import subprocess
    import json
    import datetime
    
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    filename = f"GeneratedVideo_{timestamp}.mp4"
    log_filename = f"manim_log_{timestamp}.txt"

    # Write the JSON object to test.json in the same directory
    with open("test.json", "w") as f:
        json.dump(json_data, f)

    print(f"Generating video from JSON object...")

    command = [
        "manim",
        "-pqh",
        "main.py",
        "Video",
        "-o",
        filename,
    ]

    # Run the command in the background using Popen
    print(f"Starting Manim rendering...")
    print(f"Output file will be: {filename}")
    print(f"Log file will be: {log_filename}")

    # Open the log file and start the subprocess (don't use 'with' for background processes)
    log_file = open(log_filename, "wb")  # Binary mode like the working version
    process = subprocess.Popen(command, stdout=log_file, stderr=log_file)
    
    print(f"Manim process started in the background with PID: {process.pid}")
    print(f"Check {log_filename} for rendering progress.")

    return f"Video: {filename}, PID: {process.pid}, Log: {log_filename}"


if __name__ == "__main__":
    mcp.run()
