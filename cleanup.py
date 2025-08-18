import os

LOGS_DIR = os.path.join(os.path.dirname(__file__), "logs")
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

if __name__ == "__main__":
    append_and_cleanup()
