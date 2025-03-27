import json
from datetime import datetime

OUTPUT_FILE = ""

def change_output_file(filename):
    global OUTPUT_FILE
    OUTPUT_FILE = filename

def log(message):
    # human readable now()
    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f'[{now}]{message}')
    # save to OUTPUT_FILE + ".log"
    with open(OUTPUT_FILE + ".log", "a") as f:
        f.write(f'[{now}]{message}' + "\n")

def save_json(data):
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)

