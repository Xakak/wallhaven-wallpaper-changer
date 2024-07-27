import requests
import os
import datetime



# request
def change_wallpaper(query, directory, download_tool, wallpaper_setter):
    url = "https://wallhaven.cc/api/v1/search?ratios=16x9&sorting=random&page=1-50"
    params = {f"q": query}
   # directory = "/home/rayan/Pictures/wallhaven"

    resp = requests.get(url=url, params=params)
    resp_json = resp.json()
    #print(resp)
 
    # filter download url
    for output in resp_json["data"]:
        data = output
    img_path = data["path"]
    print(img_path)

    # download and set as wallpaper
    wallpaper_name = img_path[-20:]
    wallpaper_path = os.path.join(directory, wallpaper_name)
    #dont allow repeated wallpapers to download
    if os.path.exists(wallpaper_path):
        os.remove(wallpaper_path)

    #notify-user:
    os.system('notify-send "Changing Wallpaper..."')
    if download_tool == "curl" and wallpaper_setter == "swww":
        os.system(f'curl -o {img_path} swww img {wallpaper_path} --transition-type="grow" --transition-fps="120" --transition-duration="0.6"')
    elif download_tool == "curl" and wallpaper_setter == "feh":
        os.system(f'curl -o {img_path} && feh --bg-fill {wallpaper_path}')
    elif download_tool == "axel" and wallpaper_setter == "feh":
        os.system(f'axel --output={directory} {img_path} && feh --bg-fill {wallpaper_path}')
    else:
        os.system(
            f'axel --output={directory} {img_path} && swww img {wallpaper_path} --transition-type="grow" --transition-fps="120" --transition-duration="0.6"'
        )

    # remove wallpapers older than 3 days
    max_age = 3  # days
    current_date = datetime.datetime.now()
    for dirpath, dirnames, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(dirpath, file)
            stat = os.stat(file_path)
            c_time = stat.st_ctime
            file_c_time = datetime.datetime.fromtimestamp(c_time)
            days = (current_date - file_c_time).days
            # print(days)
            if days > max_age:
                print("Removing old wallpapers....")
                os.system(f"rm -rf {file_path}")
