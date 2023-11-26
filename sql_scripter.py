"""
Made this to make it easier to add the songs for an album
to my Musica database.
Created by oktl 14 August 2023.
GUI for helping write a sql file, could be amended for other
tables in the database.

VERSION: 1.00
"""
import sqlite3
from contextlib import chdir, closing, suppress
from os import chdir as cd
from pathlib import Path

import PySimpleGUI as sg

import scripter_functions as sf

# These lines are needed for the Help and About files,
# to change to the path with the Resources folder they are in.
# Change this path_to_app before doing auto-py-to-exe.
# path_to_app = Path('c:/Users/Tim/Documents/projects/scripter')
#? - add choose file buttons for path_to_app and path_to_db?
path_to_app = Path("A:/working_apps/scripter")
path_to_db = Path("A:/muse-test-many/musica")

keys_to_clear = [
    "-FOLDER-",
    "-INFO-",
    "-SCRIPT-",
    "-TITLE-",
    "-SONG-NUMBER-",
    "-SIDE-",
    "-STATUS-"
]  # '-RESULT
custom_icon = sf.get_custom_icon()  # Titlebar icon.
title_icon = "add32.png"

# For counting rows as they're added to script,
# to know when to disable Next Song button..
row_counter = 0

# Enter key clicks the button that has focus.
QT_ENTER_KEY1 = "special 16777220"
QT_ENTER_KEY2 = "special 16777221"


def show_message(key: str, message: str, color: str="white") -> None:
    """Updates the specified window element with the given message and color.

    Args:
        key (str): The key of the window element to update.
        message (str): The message to display.
        color (str, optional): The color of the text. Defaults to "white".
    """
    window[key].update(message, text_color=color)


def get_song_inputs() -> list:
    """Returns data from the song inputs"""
    album_id = values["-ALBUM-ID-"]
    song_title = values["-TITLE-"]
    song_number = int(values["-SONG-NUMBER-"])
    album_side = values["-SIDE-"]
    return [album_id, song_title, song_number, album_side]


def create_song_row() -> list:
    """Creates a list with values from database fields based on the song inputs.

    Returns:
        list: list with values for database fields.
    """
    album_id, song_title, song_number, album_side = get_song_inputs()
    if  not window["-RB-LP-"].get():
        return get_song_row(song_title, song_number, album_id)

    # Change song number to album side or cd# and orignal song number ie. "A-1", "A-2","A-3",
    return get_song_row(song_title, f'{album_side}-{song_number},', album_id)


def get_song_row(song_title, song_number, album_id) -> list:
    """Creates a list with values for database fields based on the song information.

    Args:
        song_title (str): The title of the song, from -SONG-TITLE- input
        song_number (int or str): the number of the song, from -SONG-NUMBER- input
        album_id (str): the album id for the song, from -ALBUM-ID- input

    Returns:
        list: list of fields to make a row for sql script.
    """
    song_row = [song_title, song_number, album_id]
    show_message("-INFO-", f"\nSong added to script: \n    {song_row}")
    return song_row


def show_script(script_name):
    """Show the script as rows are appended to it in the -SCRIPT- element"""
    sql_file = sf.open_text_file(script_name)
    window["-SCRIPT-"].update(sql_file)


# This is not doing what I hoped it would, only checks for closing semi-colon.
# Only a problem when editing a script.
def check_sql_script(script: str) -> bool:
    """Uses sqlite3 function to check script for unclosed string literals and closing semicolon.

    Args:
        script (str): sql script to check.

    Returns:
        bool: True if sting literals are closed and final statement has closing semicolon,
                otherwise False.
    """
    return sqlite3.complete_statement(script)


def commmit_sql(connection: sqlite3.Connection) -> None:
    """Commit the changes in the connection to the database.
    
    Args:
        connection (sqlite3.connection): connection to database
    """
    connection.commit()


def execute_sql_script(db_to_use: str, script: str) -> None:
    """Open a connection and cursor to database, execute script

    Args:
        db_to_use (str): database to connect to.
        script (str): script for connection to execute.
    """
    with closing(sqlite3.connect(db_to_use)) as connection:
        connection.execute(script)
        commmit_sql(connection)


def allow_edits() -> None:
    """Enables editing of the script in the window.

    Updates the necessary window elements to allow editing of the script.
    """
    window["-SCRIPT-"].update(disabled=False)
    window["-SCRIPT-"].set_focus()
    window["-SCRIPT-"].set_cursor(cursor=None, cursor_color="light green")
    window["-STATUS-"].update("Script open for editing.")
    window["Copy script"].update(disabled=False)


# Declare some sg aliases.
B = sg.Button
CB = sg.Checkbox
Frame = sg.Frame
In = sg.Input
RB = sg.Radio
T = sg.Text

# Make it whatever you want.
# sg.theme('DarkTeal6')
sg.theme("DarkGrey4")
# sg.theme('DarkGrey11')
sg.set_options(tooltip_font="Calibri 12")

# Custom titlebar.
titlebar = sg.Titlebar(title="SQL Song Scripter", text_color="#303030", icon=title_icon)

# Custom menu. Alt+key does not work with this one.
menu_layout = [
    ["&File", ["&Open     Ctrl-O", "&Save      Ctrl-S", "&Properties", "E&xit"]],
    ["&Edit", ["Edit Script", "Special", "Normal", ["Normal1", "Normal2"], "Undo"]],
    ["&Actions", ["C&opy script", "&Commit script", "C&lear", "&Delete", "&Next"]],
    ["&Help", ["&Help", "&About..."]]
]

information_frame = [
    Frame("Information",
        [
            [sg.Text("",
                    size=(48, 5),
                    justification="l",
                    background_color="#303030",
                    key="-INFO-",
                    )
            ]
        ],
        background_color="#303030",
        expand_x=True,
        relief="flat",
        font=("Calibri", 14, "bold"),
        pad=((0, 20), (20, 5)),
    )
]

# For showing the lines of the script.
multiline_frame = [
    Frame("Script \n",
        [
            [
                sg.Multiline(
                    default_text=".",
                    size=(47, 18),
                    disabled=True,
                    border_width=0,
                    autoscroll=True,
                    justification="l",
                    focus=False,
                    background_color="#303030",
                    text_color="#e9e8e4",
                    key="-SCRIPT-",
                    sbar_trough_color="#303030",
                    sbar_background_color="#303030",
                    sbar_arrow_color="#9a9b94",
                    sbar_frame_color="#303030",
                    sbar_relief="flat",
                ),
            ]
        ],
        background_color="#303030",
        font=("Calibri", 14, "bold"),
        relief="flat",
        expand_x=True,
        pad=((0, 20), (20, 15)),
    )
]

radio_frame = [
    Frame("Album Media",
        [
            [
                RB( "Single CD",
                    "media",
                    default=True,
                    enable_events=True,
                    key="-RB-CD-",
                    pad=((0, 30), (0, 0)),
                    background_color="#3a3a3a",
                ),
                RB("LP or multiple CDs",
                    "media",
                    enable_events=True,
                    key="-RB-LP-",
                    background_color="#3a3a3a",
                ),
            ],
        ],
        title_location=sg.TITLE_LOCATION_TOP,
        background_color="#3a3a3a",
        relief="flat",
        element_justification="center",
        expand_x=True,
        font=(
            "Calibri",
            14,
            "bold",
        ),
        pad=((20, 20), (0, 10)),
    )
]

# Input for filename and folder to save to.
filename_input_column = [
    [
        In("Filename...",
            disabled=True,
            use_readonly_for_disable=False,
            enable_events=True,
            key="-FOLDER-",
        ),
    ],
]

filename_button_column = [
    [
        sg.SaveAs(
            button_text="  Set Filename...   ",
            file_types=(("SQL", ".sql"),),
            enable_events=True,
            target="-FOLDER-",
            auto_size_button=False,
        )
    ],
]
filename_frame = [
    Frame("File Info \n",
        [
            [
                sg.Column(
                    filename_input_column,
                    element_justification="right",
                    pad=((20, 0), (0, 0)),
                    background_color="#3a3a3a",
                ),
                sg.Column(
                    filename_button_column,
                    element_justification="right",
                    pad=((0, 20), (0, 0)),
                    background_color="#3a3a3a",
                ),
            ],
            [
                B("Create Script",
                    expand_x=True,
                    enable_events=True,
                    pad=((20, 20), (20, 20)),
                )
            ],
            [
                T("",
                    background_color="#3a3a3a",
                )
            ],
            radio_frame,
        ],
        element_justification="center",
        relief="flat",
        background_color="#3a3a3a",
        expand_x=True,
        font=("Calibri", 14, "bold"),
        pad=((20, 20), (10, 10)),
    )
]

# Inputs for song fields.
text_column = [
    [
        T("Album ID:",
            background_color="#3a3a3a",
        ),
    ],
    [
        T("Song number:",
            background_color="#3a3a3a",
        ),
    ],
    [
        T("CD # or LP side:",
            background_color="#3a3a3a",
            text_color="#3a3a3a",
            key="-SIDE-TEXT-",
        )
    ],
    [
        T("Song Title:",
            background_color="#3a3a3a",
        ),
    ],
]
input_column = [
    [
        In("10", size=5, enable_events=True, justification="center", key="-ALBUM-ID-"),
        T("# of songs:", background_color="#3a3a3a", pad=((45, 15), (0, 0))),
        In("10", size=5, justification="center", enable_events=True, key="-NUMBER-"),
    ],
    [
        In(1,
            size=5,
            justification="center",
            disabled=True,
            use_readonly_for_disable=False,
            background_color="#3a3a3a",
            key="-SONG-NUMBER-",
        ),
        CB("Reset to 1",
            enable_events=True,
            visible=False,
            disabled=True,
            background_color="#3a3a3a",
            key="-CB-RESET-",
        ),
    ],
    [
        In("A",
            size=5,
            justification="center",
            key="-SIDE-",
            border_width=0,
            background_color="#3a3a3a",
            text_color="#3a3a3a",
        ),
    ],
    [
        In("The Song Name", 
            enable_events=True, 
            key="-TITLE-")
    ],
]
song_columns = (
    [
        sg.Column(
            text_column,
            element_justification="right",
            background_color="#3a3a3a",
            key="text_column",
        ),
        sg.Column(
            input_column,
            element_justification="left",
            background_color="#3a3a3a",
            key="input_column",
        ),
    ],
)
song_frame = [
    Frame("Song Info \n",
        [
            [sg.Column(
                    song_columns,
                    pad=((0, 0), (0, 30)),
                    background_color="#3a3a3a",
                    key="cd",
                )
            ],
            [B("Next Song",
                    expand_x=True,
                    disabled=True,
                    enable_events=True,
                    bind_return_key=True,
                    pad=((20, 20), (10, 10)),
                )
            ],
            [B("Last Song",
                    expand_x=True,
                    enable_events=True,
                    pad=((20, 20), (10, 20)),
                )
            ],
        ],
        relief="flat",
        element_justification="center",
        background_color="#3a3a3a",
        expand_x=True,
        font=("Calibri", 14, "bold"),
        pad=((20, 20), (20, 0)),
    )
]

input_frame = [
    Frame("",
        [
            filename_frame,
            song_frame,
        ],
        relief="flat",
        pad=((0, 0), (0, 0))        
    )
]

info_frame = [
    Frame("",
        [
            information_frame,
            multiline_frame,
        ],
        relief="flat",
        pad=((20, 20), (0, 0))
    )
]

# * Making the final two columns
file_column = sg.Column(
    [
        input_frame,
    ],
    pad=((20, 0), (0, 0)),
)

info_column = sg.Column(
    [
        info_frame
    ],
    pad=(0, 0),
)

whole_thing = [
    Frame("",
        [
            [file_column, info_column],
        ],
        relief="flat",
        pad=(0, 0),
    )
]

status_bar = (
        [T("",
            expand_x=True,
            pad=((40, 40), (0, 10)),
            background_color="#3a3a3a",
            text_color="light green",
            key="-STATUS-",
        ),
        sg.Checkbox("Edit script", 
            pad=((0, 45), (0, 0)), 
            enable_events=True, 
            key="-CB-EDIT-"
        ),
        ],
)

# The final layout is fairly simple.
# *Layout and window with custom titlebar and custom menu.
layout = [
    [titlebar],
    [sg.MenubarCustom(menu_layout, bar_background_color="#3a3a3a", k="-MENUBAR-")],
    [whole_thing],
    sf.action_buttons_frame("Actions"),
    [status_bar],
    # for testing, turn on and off when needed, remove when no longer needed.
    # [sg.Output(expand_x=True, size=(47, 15), echo_stdout_stderr = True,)],
]

window = sg.Window(
    "",
    layout,
    auto_size_buttons=False,
    default_button_element_size=(12, 1),
    button_color="#52524e",
    font="Calibri 14",
    return_keyboard_events=True,
    resizable=True,
    finalize=True,
)

# Alt key bindings
window.bind("<Alt_L><n>", "Alt-n")
window.bind("<Alt_R><n>", "Alt-n")
NEXT = window["Next Song"]
NEXT.Widget.configure(underline=0)

window.bind("<Alt_L><l>", "Alt-l")
window.bind("<Alt_R><l>", "Alt-l")
LAST = window["Last Song"]
LAST.Widget.configure(underline=0)

window.bind("<Alt_L><r>", "Alt-r")
window.bind("<Alt_R><r>", "Alt-r")
CREATE = window["Create Script"]
CREATE.Widget.configure(underline=1)

window.bind("<Alt_L><o>", "Alt-o")
window.bind("<Alt_R><o>", "Alt-o")
COPY = window["Copy script"]
COPY.Widget.configure(underline=1)

window.bind("<Alt_L><c>", "Alt-c")
window.bind("<Alt_R><c>", "Alt-c")
COMMIT = window["Commit script"]
COMMIT.Widget.configure(underline=0)

window.bind("<Alt_L><l>", "Alt-e")
window.bind("<Alt_R><l>", "Alt-e")
CLEAR = window['Clear inputs']
CLEAR.Widget.configure(underline=2)

# Ctrl key bindings
window.bind("<Control-KeyPress-o>", "CTRL-O")  # Open.
window.bind("<Control-KeyPress-s>", "CTRL-S")  # Save .
window.bind("<Control-KeyPress-x>", "CTRL-X")  # Exit app.

while True:  # event Loop
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "Exit", "CTRL-X", "F4:115"):
        break

    # sf.print_inputs(values)  # for testing, remove when done.

    # Use enter or return key for any button that has focus.
    if event in ("\r", QT_ENTER_KEY1, QT_ENTER_KEY2):  # Check for ENTER key.
        # go find element with Focus
        elem = window.find_element_with_focus()
        if (elem is not None and elem.Type == sg.ELEM_TYPE_BUTTON):
            # If it's a button element, click it
            elem.Click()

    if event == "-FOLDER-":
        show_message("-INFO-", "\nCreate the script")

    # Radio button events:
    if event == "-RB-CD-":
        window["-SIDE-TEXT-"].update(
            text_color="#3a3a3a",
        )
        window["-SIDE-"].update(
            background_color="#3a3a3a",
            text_color="#3a3a3a",
        )
        window["-CB-RESET-"].update(
            visible=False,
            disabled=True,
        )

    if event == "-RB-LP-":
        window["-SIDE-TEXT-"].update(text_color="white")
        window["-SIDE-"].update(background_color="#d4d6c8")
        window["-SIDE-"].set_focus()
        window["-CB-RESET-"].update(
            visible=True, 
            disabled=False
        )

    #  Checkbox events:
    elif event == "-CB-RESET-":
        window["-SONG-NUMBER-"].update(disabled=False)
        window["-SONG-NUMBER-"].update(1)
        window["-SONG-NUMBER-"].update(disabled=True)
        window["-SIDE-"].set_focus()
        window["-SIDE-"].update(select=True)
        window["-CB-RESET-"].update(value=False)

    # Button events:
    if event in ["Create Script", "Alt-r"]:
        # Catch blank inputs, uses named expression (walrus) assignment. This is not working now.
        if empty_input := sf.check_inputs(values):
            sf.update_if_empty(window, empty_input)
        else:
            script_path = Path(values["-FOLDER-"])
            script_folder = script_path.parent
            script_name = script_path.name

            cd(script_folder)
            # Write the necessary first lines for the script.
            with open(script_name, "w") as file:
                file.write(
                    "INSERT INTO catalog_song (song_title, song_number, album_id)"
                )
                file.write("\n\nVALUES")
            show_message("-INFO-", 
                f'"{script_name}"  script created.\n\nUpdate Album ID number and # of songs.\nEnter Song Title.',)
            window["-ALBUM-ID-"].set_focus()
            window["-ALBUM-ID-"].update(select=True, background_color="lightgrey")
            window["Next Song"].update(disabled=False)
            show_script(script_name)

    if event in ("Next Song", "Next", "Alt-n"):
        # Catch blank inputs, uses named expression (walrus) assignment.
        if empty_input := sf.check_inputs(values):
            sf.update_if_empty(window, empty_input)
        else:
            song_number = get_song_inputs()[2]
            song_row = create_song_row()
            # Put double quotes around each part of the row and a comma at the end,
            # for a format an sql database can recognize.
            song_row = '("' + '", "'.join(map(str, song_row)) + '"),'
            # Append the new row to the file.
            with open(script_name, "a") as file:
                file.write(f"\n {song_row}")
            # Add 1 to the song_number.
            song_number += 1
            song_rows = int(values["-NUMBER-"])
            row_counter += 1
            print(f"Current row number is: {row_counter}")

            window["-SONG-NUMBER-"].update(song_number)
            window["-TITLE-"].set_focus()
            window["-TITLE-"].update(select=True, background_color="lightgrey")

            if row_counter == song_rows - 1:
                window["Next Song"].update(disabled=True)
                window["Last Song"].update(disabled=False)
                # window['Last Song'].set_focus()

            show_script(script_name)

    elif event in ("Last Song", "Alt-l"):
        # Catch empty inputs.
        if empty_input := sf.check_inputs(values):
            sf.update_if_empty(window, empty_input)
        else:
            song_number = get_song_inputs()[2]
            song_row = create_song_row()
            # Put the semicolon at end of string to complete the sql script.
            song_row = '("' + '", "'.join(map(str, song_row)) + '");'
            with open(script_name, "a") as file:
                file.write(f"\n {song_row}")
            show_message("-INFO-", f"The last row is: \n   {song_row}")
            window["Copy script"].update(disabled=False)
            show_script(script_name)

    elif event in ("Copy script", "Alt-o"):
        # Copy the text of the script to the clipboard.
        script = sg.clipboard_set(values["-SCRIPT-"])
        # Get the script from the clipboard.
        script = sg.clipboard_get()
        # Do a simple check of the script.
        # if check_sql_script(script) == False:
        if check_sql_script(script) is False:
            show_message("-INFO-",
                "\nScript is missing unclosed quotes \nand/or \nclosing semicolon",
                "orange")
        else:
            show_message("-STATUS-", 
                "Script - checked and copied to clipboard, ready to commit.")
            window["-INFO-"].update("", text_color="white")
            window["Commit script"].update(disabled=False)
            window["-CB-EDIT-"].update(visible=True)
            window["-SCRIPT-"].update(disabled=True)

    elif event in ["Commit script", "Alt-c"]:
        script = sg.clipboard_get()
        with chdir(path_to_db):
            execute_sql_script("db.sqlite3", script)
            show_message("-STATUS-", "Script committed to database.")
            # window["-STATUS-"].update("Script committed to database.")

    elif event in ("Clear inputs", "Clear", "Alt-l"):
        values.clear()
        row_counter = 0
        for key in keys_to_clear:
            window[key].update("")
        window["Copy script"].update(disabled=True)
        window["Commit script"].update(disabled=True)
        window["Next Song"].update(disabled=True)
        window["-SONG-NUMBER-"].update(1)
        window["-SIDE-"].update("A")
        window["-CB-EDIT-"].update(visible=False)
        window["-SCRIPT-"].update(value=".")
        window['-STATUS-'].update("")
        
    # Menu events:
    elif event.startswith("Open") or event == "CTRL-O":
        script_name = Path(sg.popup_get_file("file to open", no_window=True))
        show_message("-INFO-", f"File opened: \n{script_name}")
        # window["-INFO-"].update(f"File opened: \n{script_name}")
        show_script(script_name)
        print(script_name)
        window["Copy script"].update(disabled=False)

    elif event in ("Edit Script", "-CB-EDIT-"):
        allow_edits()

    elif event.startswith("Save") or event == "CTRL-S":
        # if check_sql_script(script) == False:
        if check_sql_script(script) is False:
            show_message("-INFO-", 
                "\nScript is missing unclosed quotes \nand/or \nclosing semicolon",
                text_color="orange",)
        else:
            text = values["-SCRIPT-"]
            with open(script_name, "w") as file:
                file.write(text)
            show_message("-STATUS-", f"\tScript saved as: {script_name}.", 
                    text_color="light green")

    elif event in ("Delete",):
        with suppress(NameError):
            script_name

            file_to_delete = Path(script_name)
            if Path(file_to_delete).exists():
                sf.delete_file(file_to_delete)
            else:
                sg.Popup(
                    "Nothing to delete",
                    text_color="yellow",
                    font=("Calibri", 14),
                    no_titlebar=True,
                    keep_on_top=True,
                    relative_location=(0, 200),
                )
                show_message("-INFO-", "Nothing to delete", text_color="dark orange" )

            if deleted := sf.confirm_file_does_not_exist(file_to_delete):
                show_message("-INFO-", f'\nThe file  "{script_name}"  was deleted',
                    text_color="dark orange",)
            else:
                show_message("-INFO-", f'\n"{script_name}"  not deleted')

    # Show a popup with some information about the app.
    if event in ("About...", "F2:113"):
        with chdir(path_to_app):
            about = sf.open_text_file(Path("Resources\\about.txt"))
            window.disappear()
            sg.popup(
                "About SQL Scripter",
                "Version 1.0",
                "PySimpleGUI Version:",
                sg.version,
                about,
                no_titlebar=True,
                image=title_icon,
            )
            window.reappear()

    # # Use the Help menu item or press F1.
    if event in ('Help', 'F1:112'):
        with chdir(path_to_app):
            print(f'Help folder is: {path_to_app}')
            help_file = Path('Resources\\help.html')
            help = sf.open_file_in_browser(help_file)

window.close()
