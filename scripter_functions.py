"""
Helper functions for sql_scipter gui
oktl 14 Aug 2023
"""
import datetime
import webbrowser
from pathlib import Path

import PySimpleGUI as sg

# declare some sg aliases
B = sg.Button
T = sg.Text


def check_inputs(values: dict) -> str:
    """Loop through input values to see if any are empty.

    Args:
        values (dict): dictionary of keys: values for window inputs

    Returns:
        str: list formatted as string of keys for empty inputs.
    """
    # Get a dictionary of keys and empty values, if any are empty.
    no_values = {key: value for (key, value) in values.items() if value == ""}
    return ", \n\t".join(str(x) for x in no_values)


def update_if_empty(window, empty_input) -> None:
    """Update a PySimplGUI window Text element to warn user of any empty inputs.

    Args:
        window (sg.Window): the PySimple GUI window diplayed by the app.
        empty_input (list): list of empty inputs.
    """
    window["-INFO-"].update(f"Empty inputs:\n\t{empty_input}", text_color="yellow")


def confirm_file_exists(filename: str) -> bool:
    """Check to see if file exists.
    
    Args:
        filename (pathlib.Path): Path to file to check.
    
    Returns:
        bool: Either the file exists or it doesn't.    
    """
    return Path(filename).exists()


def confirm_file_does_not_exist(filename: Path) -> bool:
    """Check to see if file does not exist.
    
    Args:
        filename (pathlib.Path): Path to file to check.
    
    Returns:
        bool: Either the file exists or it doesn't.
    """
    return not filename.exists()
    # return not Path(filename).exists()


# TODO - change this to open the file in notepad++ or other application.
def open_file_in_browser(filename: Path) -> None:
    """Open a file in the os default web browser.
    
    Args:
        filename (pathlib.Path): Path to file to open
    """
    # file_to_open = Path(filename)
    # webbrowser.open_new(file_to_open)
    webbrowser.open_new(filename)
    


def open_text_file(file_to_open) -> str:
    """Open a file for reading.
    
    Args:
        file_to_open (_type_): text file

    Returns:
        str: contents of the file_to_open
    """
    # Using the 'with' keyword automatically closes file, no need to do it explicitly.
    # 'r' option opens file as read only.
    with open(file_to_open, "r") as file:
        contents = file.read()

    return contents


def convert_bytes(size: float) -> str:
    """
    Convert integer of whatever length of bytes
    to more human readable string in  KB, MB, GB or TB size.

    Args:
        size (float): size of file

    Returns:
        str: string, formatted, example: 10.72 MB
    """
    for x in ["bytes", "KB", "MB", "GB", "TB"]:
        if size < 1024.0:
            return f"{size: .2f} {x}"        
        size /= 1024.0


def get_file_attributes(filename: Path) -> tuple:
    """Get some attributes of a file  - for delete popup
    
    Args:
        filename (pathlib.Path): Path to file to get stats for.
    
    Returns:
        tuple: file size and file time strings.
    """
    file_stats = Path(filename).stat()
    file_size = file_stats.st_size
    file_size_str = convert_bytes(file_size)
    file_time = file_stats.st_mtime
    file_time_str = datetime.datetime.fromtimestamp(file_time).strftime(
        "%m/%d/%Y %H:%M"
    )

    return file_size_str, file_time_str


def delete_popup(title: str, text: str, filename: Path) -> None:
    """Custom popup to confirm delete.
    
    Args:
        title (str): title for PySimpleGUI window.
        text (str): text to show in PySimpleGUI Text element.
        filename (pathlib.Path): Path to filename to delete.
    """
    window = sg.Window(
        title,
        [
            [
                T("Are you sure you want to delete this file?"),
            ],
            [sg.Image(get_custom_icon()), T(text)],
            [sg.OK(), sg.Cancel()],
        ],
    )
    event, values = window.read()
    if event != "OK":
        ...
    else:
        filename.unlink()
    window.close()
    

def delete_file(filename: Path) -> None:
    """Delete a file with a popup to confirm.
    
    Args:
        filename (pathlib.Path): Path to file to delete.
    """
    file_size, file_time = get_file_attributes(filename)
    ask_lines = f"\n{filename}\nSize:  {file_size}\n Date modified:  {file_time}\n"
    delete_popup("Delete", ask_lines, filename)


# User defined layout elements
# Shortcut for the information frames. Not using in thi app.y
def information_frame(title: str, key: str) -> sg.Frame:
    """User defined custom frame element for displaying information.
    
    Args:
        title (str): title for PySimpleGUI Frame element.
        key (str): PySimpleGUI key for the Frame element.
        
    Returns:
        sg.Frame: PySimpleGUI Frame element with a Text element.
    """
    return [
        sg.Frame(
            layout=[
                [sg.Text("", size=(47, 3), justification="c", key=key)]
            ],
            title=title,
            title_location=sg.TITLE_LOCATION_TOP,
            expand_x=True,
            font="Calibri 10",
            pad=((0, 0), (5, 15)),
        )
    ]


# Shortcut for the buttons frame. Make them whatever they neee to be.
def action_buttons_frame(title: str) -> sg.Frame:
    """User defined custom frame element for placing buttons.
    
    Args:
        title (str): title for PySimpleGUI Frame.
    
    Returns:
        sg.Frame: PySimpleGUI Frame element with Button elements.
    """
    
    buttons = [
        [
            B("Copy script", 
                disabled=True, 
                pad=((0, 0), (20, 20)),
                key="Copy script"),
            B("Commit script",
                disabled=True,
                pad=((40, 0), (20, 20)),
                key="Commit script",
                ),
            B("Clear inputs",
                pad=((40, 40), (20, 20)),
                ),
            B("Exit")            
        ]        
    ]
    
    return [sg.Frame(title,
            buttons,
            title_location=sg.TITLE_LOCATION_TOP,
            expand_x=True,
            element_justification="center",
            font=("Calibri", 14, "bold"),
            background_color="#3a3a3a",
            relief="flat",
            pad=((40, 45), (20, 30)),
        )
    ]


def open_about_window(title: str, text_file) -> None:
    """User defined custom window to show a text file.
        Open a new window, show text_file in the Text element.
    # TODO - add the args and return parts of the doc.
    Args:
        title (str): title for the window
        text_file (_type_) ?:
    """
    layout = [
        [sg.Image("add32.png"), T(title, font="Calibri 12 bold")],
        [T(text_file, 
            auto_size_text=True, 
            font="Calibri 9")],
        [B("OK", 
            enable_events=True, 
            bind_return_key=True, 
            focus=True)],
    ]
    window = sg.Window(
        title,
        layout,
        no_titlebar=True,
        text_justification="c",
        element_justification="c",
        finalize=True,
    )
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "OK",):
            break
    window.close()


# Icon for titlebar.
def get_custom_icon() -> bytes:
    """Return a base 64 representation of an image.
    
    Returns:
        bytes: _description_
    """
    return b"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"


def get_delete_icon() -> bytes:
    """Return a base 64 representation of an image.
    
    Returns:
        bytes: _description_
    """
    return b"iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAMAAADXqc3KAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAA4VBMVEX//////v7+/v7+/Pz++/v42trsmZnfVFTWJyfSEhL+/f3me3vUGxvQBwfaPDzhYWHlc3PUHBzldnb42dnvra3XKCjSDQ3ja2v1zc376urSDg7XKSnxtrbrmZnRDAzZODj1y8vSERHtoKDvq6veT0/77e3eTk7wtLTaOTn65+fXKirmenr0yMj88vLxurr87+/319fjamrxubnQBgbleHjmeXn32Njsmpr99vbQBQXleXn99fX1ycn66enld3fhYGDmfHzTEhLkcXHkcnL0x8f65ub77OzZNzf1ysr76enjbGysa4tLAAAAAWJLR0QAiAUdSAAAAAd0SU1FB+cGFBQYHW2cS94AAAE8SURBVCjPdVKJVsIwEJzuprQNttAicohAUe5LubQKVEVF/f8PMsGLpzTv5eVldmd2MxvAADEJM2XZjmNbKVOQBBnY4TDTR66XyWYznusHOUjSsMKP8yeFYokBLhUL5dMKBBEgcVat1XWWVBoS9VrYUCAY59WLJlhIUksKRrMVthUMM9/pqlMxFF8xGN1OzwTQLw9Aw9FY0yXGoyFhUA6AS/9KJU2mM2gpzKcTdS34C1y7RTDdzKNbyUzzaHanAks3BctbQdftT9fMOqzrrDwLdoaxK7qO+ulovesAIrbhZDVBR+7DhzRpP9R+dOBsEgJ2LA5LJRZPbHeR9EAE/y150pbA7P018bmmTWS0w9bLj+38a7tEI9zuDep1+zkoIoFKr/w12rfl+/doDZ2VC3zXizebeO8zwFAaB77PBybvJeRgmYXnAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDIzLTA2LTIwVDIwOjIzOjM0KzAwOjAwVPG1+QAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyMy0wNi0yMFQyMDoyMzozNCswMDowMCWsDUUAAAAASUVORK5CYII="


def get_header_icon() -> bytes:
    """Return a base 64 representation of the header icon

    Returns:
        bytes: _description_
    """
    return b"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAIAAAD8GO2jAAAE5klEQVR4nLVWbVBUVRh+zzl39y73wn6wu8CCuBmJAVrpIBE55lc241SWwhhiTk798UeglVI/a/rRODXN9PGnmqnID/B7RnCISQUmVxKQDwlGBw2dRNcFS8F2936ctx9XYXGvYDY8f+695773ec773Pe85xBEhOkEnVZ2ABDG7m7evBVoaQ2Hw4SQh6ZDjgmS7ZnCAqfDbowQw6JINFq1s7qosMDnS3t4egAAGLx2LRA4vXHDOpvNNp7B9euhpMSkuXk5/48cACA52XW2py8YDPn9meMCiEgZM+7rjjZ0dHZbrBbOkVKKHBEQAJwOe1lpia7rLpcTABRF+evvmx53MmNMVTVBYGPeCozxu7UjQBxaTreFw5EVy5/b8ekXWyo2t7d19l/44603X1cUZXf1/kuXLq9atTLF691Tc0CSEpSoUlZaUt9wrHjtaq/HfWe6gHDXaBOBGem+ru6elpZWf+aM9raOW7dGE2X5xInmpUsXJ9hsLpfL43b/tLumrLQkZ052W3tn1a5qQNA13dQxE4GiogK/PxMIWfRsoabrlBAj9+zZWU5H0oWLl2qP/kwJJYQEg9fb2jpsYkIk/I+ma4gYX4EmAo3NJ5ubAhardWwEARml27eVnwycHhq+sTB/fvbsrL37DnPO+y8OvPryqiuDV7/57sdFRU+vfH7Z1ALLlizOmZM99s8NcM5HR29vWF9CGbMnJQFA5baKkZFRSZY0TRNFMRKJWC2WB7Lo2PGmxqaT1pgMDCiK8n7lloL8BXe+FASjnESrFQASZTmeylxgxYoleXk5lLKJw4iIj87ym7JMAhOBhobjTc2B+Aw0TavcVu5xu890dtXsPWwRBAQgALrO09K8m94oM6ybWuCFlcvnzctllAJAbKdFxKysWQBwZfBaa2uHKI7PQDujDwxcfu+dtzMyfFML1Nf/0tgcEEUrIhJKAY12haqqfVBZ4S5IZpQ6XfZoRCGEMMZ0nSNC99m+XdX7tr9bPrXAa+vWLl22GABEq1VRlLGGCICP+GcCACJXVbWgYEE0qvT09Hm97tzcOY1Nv6qK9kAW+XypDof9s8+/2lC2Lufx7PgATdWfmJu7tXzzRx/vUFUtHAkXr3kpI93X338hPth8w+FcHxi4/P0PO03fChahq7u3uuagLMuc80RZPvVb25HaesZYfLC5gCzLOz75UJKk3dX7R0ZG7n1NiKIoBw/XtZ/pEkVrMBiqqqoZHr5BqQmbiUUAQAhxu5O3Vmw+Ulf/5dffRqJRUbRu2rg+Pd0HAJwj59xisSCirusAwBjVdY1z/qACBkRRLF6zOhyJHDpUGxoaDg0NGQIOe2Jaaopl4kJRVcXtSf5vAgYSbLb1pcWxI4uKCvMXzL8nDAHj1+YEAcHsF5mCUipJCZMECCyG1rgwxrp7ejXNpJAfAn3nzi/Mnz9BQBCErrO9gVOthBICYDSZWCACIgcgCEiAUHrfswdHlGVJEO4yj+ciMJtNND0Ucc5TUjxPPZl3e/S2JEmDV4O/954zLUoAQESBsbEuRmNYJjtDqqpGgFBGJUlKTfE47EmTxMfW650MnA57RnpqX995i9muBACh0NCRugYAQABKCKUUAYjZPq+qqn/mY06nw3gca2Tw55XBA4dqQ6Fhcn9/pwRy9HiT177yYuaMjHsFpgnTfrr+F5WG/e/Nwom4AAAAAElFTkSuQmCC"


# * For testing during development.
def print_inputs(window_values: dict) -> None:
    """Print all values by key.
    
    Args:
        values (dict): dictionary of values of PySimpleGUI window elements with keys.
    # TODO - add the args and return parts of the doc.
    """
    key_value_dict = dict(window_values)
    for key, value in key_value_dict.items():
        sg.Print(f'{key}: {value}')

