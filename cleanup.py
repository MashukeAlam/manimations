import os
import shutil

LOGS_DIR = os.path.join(os.path.dirname(__file__), "logs")
MEDIA_DIR = os.path.join(os.path.dirname(__file__), "media")
COMBINED_LOG = os.path.join(LOGS_DIR, "combined_logs.txt")

def get_log_files():
    return [
        f for f in os.listdir(LOGS_DIR)
        if f.endswith(".txt") and f != "combined_logs.txt"
    ]

def append_and_cleanup():
    log_files = get_log_files()
    if not log_files:
        print("No new log files to append.")
        return
    with open(COMBINED_LOG, "a", encoding="utf-8") as combined:
        for log_file in log_files:
            log_path = os.path.join(LOGS_DIR, log_file)
            with open(log_path, "r", encoding="utf-8") as lf:
                combined.write(f"\n--- {log_file} ---\n")
                combined.write(lf.read())
            os.remove(log_path)
            print(f"Appended and deleted: {log_file}")
    print(f"All new logs appended to {COMBINED_LOG}.")

def cleanup_media_directory():
    """Deletes all files and subdirectories in the media directory."""
    print(f"Cleaning up media directory: {MEDIA_DIR}")
    if not os.path.exists(MEDIA_DIR):
        print("Media directory not found.")
        return

    for item in os.listdir(MEDIA_DIR):
        item_path = os.path.join(MEDIA_DIR, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
                print(f"Deleted file: {item_path}")
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"Deleted directory: {item_path}")
        except Exception as e:
            print(f"Failed to delete {item_path}. Reason: {e}")
    print("Media directory cleanup complete.")

if __name__ == "__main__":
    append_and_cleanup()
    cleanup_media_directory()
