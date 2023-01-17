from time import sleep
import json
import os



def save_path():
    config_file = 'config.json'
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
            path = config['path']
            print(f"Caminho atual: {path}")
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        path = '../'
        path.rstrip("/").replace('\\','/')
        config = {'path': path}
        with open(config_file, 'w') as f:
            json.dump(config, f)
        print(f"Caminho salvo: {path}")
    return path


def change_path():
    config_file = 'config.json'
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
            path = config['path']
            os.system('cls')
            print(f"Caminho atual: {path}")
            print('')
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        os.system('cls')
        print("Não há caminho salvo.")
        print('')
        sleep(1)
        save_path()
        return
    new_path = input("Insira o novo caminho: ")
    new_path = new_path.rstrip("/").replace('\\','/')
    config = {'path': new_path}
    with open(config_file, 'w') as f:
        json.dump(config, f)
    print(f"Caminho salvo: {new_path}")