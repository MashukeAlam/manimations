
import os
import json
import datetime
from mcp.server.fastmcp import FastMCP

# Create the 'scripts' directory if it doesn't exist
os.makedirs("scripts", exist_ok=True)

mcp = FastMCP("Save JSON Tool")

@mcp.tool("save_json")
def save_json(json_data: dict) -> str:
    """
    Saves a JSON object to a new file in the 'scripts' directory.

    The filename will be based on the current timestamp to ensure uniqueness.

    Args:
        json_data (dict): The JSON object to be saved.

    Returns:
        str: A message indicating the path to the newly created file.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{timestamp}.json"
    filepath = os.path.join("scripts", filename)

    try:
        with open(filepath, 'w') as f:
            json.dump(json_data, f, indent=4)
        
        message = f"Successfully saved JSON data to {filepath}"
        print(message)
        return message
    except Exception as e:
        error_message = f"Error saving JSON data: {e}"
        print(error_message)
        return error_message

if __name__ == "__main__":
    mcp.run()
