import argparse
import os
import configparser
from wallhaven import change_wallpaper


CONFIG_FILE = os.path.expanduser('~/.wallhaven_config.ini')

def save_config(query, directory, download_tool, wallpaper_setter):
    config = configparser.ConfigParser()
    config['SETTINGS'] = {
        'query': query,
        'directory': directory,
        'download_tool': download_tool,
        'wallpaper_setter': wallpaper_setter
    }
    
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def load_config():
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        return config['SETTINGS']
    return None

def main():
    parser = argparse.ArgumentParser(description='Change wallpaper by fetching it from an API.')
    parser.add_argument('--configure', action='store_true', help='Configure the wallpaper changer settings')

    args = parser.parse_args()

    if args.configure:
        print("One-Time Configuration....")
        query = input("Enter Query for wallpapers [e.g : 4k,nature,sunset]: ")
        directory = input("Enter the path to save the wallpaper [should be proper path!]: ")
        download_tool = input("Enter the tool for downloading wallpaper [axel or curl]: ")
        wallpaper_setter = input("Enter the wallpaper setter [feh or swww]:")
        save_config(query, directory, download_tool, wallpaper_setter)
        print("Configuration saved.")
    else:
        config = load_config()
        if config:
            change_wallpaper(config['query'], config['directory'], config['download_tool'], config['wallpaper_setter'])
        else:
            print("Configuration not found. Please run with --configure to set up.")

if __name__ == '__main__':
    main()
