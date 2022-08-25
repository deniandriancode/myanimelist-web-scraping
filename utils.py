import os
import requests

def clear_console():
    command = "clear"
    # if the operating system is windows, most likely the terminal emulator is cmd, so use cls instead of clear command
    if os.name in ("nt", "dos"):
        command = "cls"
    # else use the default clear command
    os.system(command)


def get_additional_flag(review):
    # this will check if review has additional flag, such as Spoiler
    if len(review.find(class_='tags').find_all(class_='tag')) > 1:
        return ' '.join(map(lambda x: x.text.strip().replace('\n', ' '), review.find(class_='tags').find_all(class_='tag')[1:]))
    # if not then just add None
    return "None"
