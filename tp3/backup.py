import json
import shutil
import os
from datetime import datetime
import time
import random
import tarfile
import sys

#all variable
conf="/home/abel/Documents/B2-linux/tp3/conf.json"

with open(conf, 'r') as config_json:
    data = json.load(config_json)
    config_json.close()

max_backup = data["nmb_backup"]
dest = data["dest"]
to_save = data["saves"]
time_gap = data["time_gap"]
state_json = []
try:
    os.mkdir(f"{dest}/archives_backup")
    os.mkdir(dest)
except:
    pass
    
def copy_files(id: str):
    for files_path in to_save:
        file_name = files_path.split("/")
        try:
            shutil.copy(files_path, f"{dest}/{id}/{file_name[-1]}")
        except:
            shutil.copytree(files_path, f"{dest}/{id}/{file_name[-1]}")
    create_tarfile(f"{dest}/archives_backup/{id}.tar.gz", f"{dest}/{id}", id)

def create_tarfile(output_filename, source_dir, id: str):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname="test")
    shutil.rmtree(f"{dest}/{id}")

def write_json_state(id: str, state_json: list):
    now = datetime.now()
    state_json_update = {
            "id": id,
            "archive": f"{dest}/archives_backup/{id}.tar.gz",
            "datetime": now.strftime("%Y-%m-%d %H:%M:%S")
    }
    print(type(state_json))
    state_json.append(state_json_update)

    state_json_file = open(f"{dest}/archives_backup/state.json", "w")
    json_object = json.dump(state_json, state_json_file, separators=(',', ':'))
    state_json_file.close()

def get_state_json() -> list:
    with open(f"{dest}/archives_backup/state.json", "r") as json_state:
        data_state = json.loads(json_state.read())
    json_state.close()
    return data_state 

def create_folders():
    id = (str(abs(hash(str(random.randint(0, 10000)) + str(datetime.now())))))
    os.mkdir(f"{dest}/{id}")
    return id

def remove_first_backup():
    backup_delete = state_json.pop(0) 

    state_json_file = open(f"{dest}/archives_backup/state.json", "w")
    json_object = json.dump(state_json, state_json_file, separators=(',', ':'))
    state_json_file.close()

    backup_delete_name_archive = backup_delete["archive"]

    os.remove(backup_delete_name_archive)

def number_backup():
    with open(f"{dest}/archives_backup/state.json", "r") as json_state:
        data_state = json.loads(json_state.read())
    json_state.close()

    print(data_state)
    print(len(data_state))
    print()
    if len(data_state) > max_backup:
        remove_first_backup()

def list_backups():
    with open(f"{dest}/archives_backup/state.json", "r") as json_state:
        data_state = json.loads(json_state.read())
    json_state.close()

    for key in data_state:
        for value in key:
            print('\33[31m' + value + '\x1b[0m', end=": ")
            print(key[value])
        print()

def argv():
    args = sys.argv
    result = ""
    if (len(args)) == 2:
        if (args[1] == "--help" or args[1] == "-h"):
            result = "here is help"
        elif (args[1] == "backup"):
            result = "backup"
        elif (args[1] == "list"):
            list_backups()
            exit(0)
        else:
            result = "wrong arguments"
    elif (len(args)) == 3:
        if (args[1] == "restore" and args[2] == "id"):
            result = "restore backup"
        else:
            result = "wrong arguments"
    else:
        result = "wrong arguments"

    print(result)
    if result == "wrong arguments":
        exit(1)

def main():
    argv()
    state_json = get_state_json()
    while True:
        id = create_folders()
        copy_files(id)
        write_json_state(id, state_json)
        number_backup()
        print("done")
        time.sleep(6)
        #time.sleep(time_gap*60*60)

if __name__ == "__main__":
    main()
