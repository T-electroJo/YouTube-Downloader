import json
from colorama import Fore, init
from pytube import YouTube
import os
import atexit
from art import text2art
import re
import time
from easygui import filesavebox
import importlib


def main():
    try:
        clear()
        link = input(Fore.CYAN + "\n\n  Enter the YouTube-URL: " + Fore.RED)
        while True:
            mode = input(Fore.CYAN + "\n  Download as audio or video file? [a|v]: " + Fore.RED)
            if mode.lower() in ["a", "v"]:
                if mode == "a":
                    _video = False
                else:
                    _video = True
                break
            else:
                clear()
                print(Fore.CYAN + "\n\n  Enter the YouTube-URL: " + Fore.RED + link)
        print(Fore.YELLOW + "\n  Checking if link is valid...", end="\r")
        for index, value in enumerate("Checking if link is valid..."):
            if value == " ":
                continue
            _str = Fore.GREEN + "Checking if link is valid..."[:index+1]
            _str += Fore.YELLOW + "Checking if link is valid..."[index+1:]
            print(f"  {_str}", end="\r")
            time.sleep(0.1)
        time.sleep(0.2)
        if re.match(json.load(open("config.json"))["REGEX-FILTER"], link) is None:
            print(Fore.RED + "  The given link is not a valid YouTube URL. Please ensure to enter the right URL.")
            for i in range(6):
                print(Fore.RED + f"  This program will exit in {6-(i+1)} second{'.' if i == 4 else 's.'}.. ", end="\r")
                time.sleep(1)
            print(Fore.RED + "  Exiting...                            ")
            time.sleep(0.5)
            exit()
        print(Fore.GREEN + "  Link is a valid YouTube link. Moving on...", end="\r")
        time.sleep(1)
        print(Fore.YELLOW + "  Fetching information of the video...      ", end="\r")
        time.sleep(0.5)
        try:
            obj = YouTube(link)
            obj.register_on_progress_callback(update_callback)
        except Exception as e:
            print(Fore.RED + f"Error: {e}")
            for i in range(6):
                print(Fore.RED + f"  This program will exit in {6-(i+1)} second{'.' if i == 4 else 's.'}.. ", end="\r")
                time.sleep(1)
            print(Fore.RED + "  Exiting...                            ")
            time.sleep(0.5)
            exit()
        time.sleep(1)
        print(Fore.GREEN + "  Fetching information of the video...      ", end="\r")
        time.sleep(1)
        print(
            Fore.CYAN + "  Video information:                           \n" +
            Fore.BLUE + f"\n    Title:  \t{Fore.MAGENTA + obj.title}" +
            Fore.BLUE + f"\n    Author: \t{Fore.MAGENTA + obj.author}" +
            Fore.BLUE + f"\n    Length: \t{Fore.MAGENTA + time.strftime('%H:%M:%S', time.gmtime(obj.length))}" +
            Fore.BLUE + f"\n    Views:  \t{Fore.MAGENTA + str('{0:,}'.format(obj.views))}\n"
        )
        print(Fore.YELLOW + "  Save location: operation pending...", end="\r")
        mode = "mp4" if mode == "v" else "mp3"
        full_path = filesavebox(
            f"Save '{obj.title}.{mode}' as...",
            default=f"{obj.title}.{mode}",
            filetypes=[f"*.{mode}"]
        )
        save_path = os.path.split(full_path)
        if not save_path[0]:
            print(Fore.RED + f"  Save location: operation pending...", end="\r")
            time.sleep(1)
            print(Fore.RED + "  Save operation cancelled.          ")
            for i in range(6):
                print(Fore.RED + f"  This program will exit in {6 - (i + 1)} second{'.' if i == 4 else 's.'}.. ",
                      end="\r")
                time.sleep(1)
            print(Fore.RED + "  Exiting...                            ")
            time.sleep(0.5)
            exit()
        print("                                     ", end="\r")
        print(Fore.GREEN + f"  Save location operation pending...", end="\r")
        time.sleep(0.5)
        print(Fore.GREEN + f"  Save location confirmed: '{Fore.CYAN + save_path[1] + Fore.GREEN}'\n")
        time.sleep(0.2)
        print(Fore.GREEN + "  Moving on...", end="\r")
        time.sleep(0.5)
        print(Fore.YELLOW + f"  Preparing to download '{obj.title}.mp4'...", end="\r")
        time.sleep(2)
        print(Fore.YELLOW + f"  Downloading '{obj.title}.mp4'...                                 ", end="\r")
        obj.streams.get_highest_resolution().download(
            output_path="./temp/",
            filename=save_path[1][:-3]+"mp4"
        )
        if mode == "mp3":
            print(Fore.YELLOW + "\n  Converting downloaded video to '.mp3'...", end="\r")
            video = importlib.import_module("moviepy.editor").VideoFileClip(f"./temp/{save_path[1][:-4]}.mp4")
            video.audio.write_audiofile(full_path, verbose=False, logger=None)
            video.close()
            print(Fore.GREEN + "  Converting downloaded video to '.mp3'...", end="\r")
            time.sleep(0.5)
            print(Fore.YELLOW + "  Done, saving converted video to desired location...", end="\r")
            time.sleep(1)
            print(Fore.GREEN + "  Done, saving converted video to desired location...  ", end="\r")
            time.sleep(0.5)
            print(Fore.YELLOW + "  Done, deleting temporary files...                     ", end="\r")
            for _file in os.listdir("./temp/"):
                os.remove("./temp/" + _file)
            time.sleep(0.5)
            print(Fore.GREEN + "  Done, deleting temporary files...    ", end="\r")
        else:
            print()
        time.sleep(0.5)
        print(Fore.GREEN + "  All tasks successfully finished.   ")
        time.sleep(0.75)
        print(Fore.GREEN + "\n  Clear screen or exit? [c|e]: ", end="")
        msg = input(Fore.RED)
        if not msg.lower() == "c":
            print(Fore.RED + "\n  Exiting by user in 2 seconds...", end="\r")
            time.sleep(2)
            print(Fore.RED + "  Exiting...                      ")
            time.sleep(0.5)
            exit()
        else:
            clear()
            return True
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print(f"\n\n{Fore.RED}{e}")
        os.system("pause")


def clear():
    os.system("title -- YouTube-Downloader [v0.4] --") if os.name == "nt" else None
    os.system("cls" if os.name == "nt" else "clear")
    print("\n" + Fore.GREEN + text2art("  PY-YT-DL") + Fore.RED + "\t       Python - YouTube - Downloader")


def update_callback(stream, chunk, bytes_remaining):
    percent_remaining = round(((stream.filesize-bytes_remaining)/stream.filesize*100)/4, 2)
    print(
        Fore.RED +
        f"  ( {round((stream.filesize-bytes_remaining)/1048576, 2)}MB / {round(stream.filesize/1048576, 2)}MB ) - " +
        f"{percent_remaining*4}% - " +
        Fore.GREEN + "█"*(round(percent_remaining)) +
        Fore.YELLOW + "█"*(25-round(percent_remaining)) +
        "                           ",
        end="\r"
    )
    if percent_remaining*4 == 100.0:
        for _i in range(5):
            print(
                Fore.RED +
                f"  ( {round((stream.filesize - bytes_remaining) / 1048576, 2)}MB / "
                f"{round(stream.filesize / 1048576, 2)}MB ) - " +
                f"{percent_remaining*4}% - " +
                Fore.BLUE + "█"*25,
                end="\r"
            )
            time.sleep(0.075)
            print(
                Fore.RED +
                f"  ( {round((stream.filesize - bytes_remaining) / 1048576, 2)}MB / "
                f"{round(stream.filesize / 1048576, 2)}MB ) - " +
                f"{percent_remaining*4}% - " +
                Fore.GREEN + "█" * 25,
                end="\r"
            ) if not _i == 4 else print(
                Fore.RED +
                f"  ( {round((stream.filesize - bytes_remaining) / 1048576, 2)}MB / "
                f"{round(stream.filesize / 1048576, 2)}MB ) - " +
                f"{percent_remaining*4}% - " +
                Fore.GREEN + "█" * 25 +
                Fore.RED + " - done downloading"
            )
            time.sleep(0.075)


if __name__ == "__main__":
    init(autoreset=True)
    atexit.register(lambda: os.system("cls" if os.name == "nt" else "clear"))
    while True:
        if main():
            continue
