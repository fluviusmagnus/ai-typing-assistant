import time
from openai import OpenAI
from dotenv import load_dotenv
from os import getenv
import pyperclip
from global_hotkeys import *
import PySimpleGUI as sg

TEMPLATES = {

"typo":"""Fix all typos and casing and punctuation in the text between the {LABEL1} and {LABEL2} label, preserve all new line characters.
Return only the corrected text in this form {LABEL1}text{LABEL2}, and don't include a preamble or add extra new line characters.
The text should remain in its original language, do not translate:

{LABEL1}{text}{LABEL2}

""",

"style":"""Improve the text between the {LABEL1} and {LABEL2} label in the style and quality of academic paper, preserve all new line characters.
Return only the improved text in this form {LABEL1}text{LABEL2}, and don't include a preamble or add extra new line characters.
The text should remain in its original language, do not translate:

{LABEL1}{text}{LABEL2}

""",

"translate2zh":"""You are a professional translator. Translate the text between the {LABEL1} and {LABEL2} label precisely to Simplified Chinese, preserve all new line characters.
Return only the translated text in this form {LABEL1}text{LABEL2}, and don't include a preamble or add extra new line characters:

{LABEL1}{text}{LABEL2}

""",

"translate2de":"""You are a professional translator. Translate the text between the {LABEL1} and {LABEL2} label precisely to German, preserve all new line characters.
Return only the translated text in this form {LABEL1}text{LABEL2}, and don't include a preamble or add extra new line characters:

{LABEL1}{text}{LABEL2}

""",

"translate2en":"""You are a professional translator. Translate the text between the {LABEL1} and {LABEL2} label precisely to English, preserve all new line characters.
Return only the translated text in this form {LABEL1}text{LABEL2}, and don't include a preamble or add extra new line characters:

{LABEL1}{text}{LABEL2}

""",

"translate2ja":"""You are a professional translator. Translate the text between the {LABEL1} and {LABEL2} label precisely to Japanese, preserve all new line characters.
Return only the translated text in this form {LABEL1}text{LABEL2}, and don't include a preamble or add extra new line characters:

{LABEL1}{text}{LABEL2}

""",

"translate2fr":"""You are a professional translator. Translate the text between the {LABEL1} and {LABEL2} label precisely to French, preserve all new line characters.
Return only the translated text in this form {LABEL1}text{LABEL2}, and don't include a preamble or add extra new line characters:

{LABEL1}{text}{LABEL2}

"""
}

LABEL1="<TEXT_BEGIN>"
LABEL2="<TEXT_END>"

print("Initializing...")

load_dotenv()
client = OpenAI(
  base_url=getenv("BASE_URL"),
  api_key=getenv("API_KEY"),
)


def fix_text(action, text):
    prompt = TEMPLATES[action].format(text=text,LABEL1=LABEL1,LABEL2=LABEL2)
    # print(prompt)
    completion = client.chat.completions.create(
      model=getenv("MODEL"),
      messages=[
        {
          "role": "user",
          "content": prompt,
        },
      ],
    )
    return completion.choices[0].message.content.strip()


def on_f9():
    print("Ctrl+F9 Pressed!")
    text = pyperclip.paste()
    if not text:
        sg.popup("Error: Nothing in clipboard!")
        return
    print("Orig:",text)

    layout = [[sg.Multiline(key="-EDIT-", default_text=text, size=(None, 5))],
              [sg.Text("Select an action: "),
               sg.OptionMenu(TEMPLATES.keys(),default_value=list(TEMPLATES.keys())[0], key='-OPTIONS-'),
               sg.Button("Execute"),
               sg.Button("Copy & Close"),
               sg.Button("Close")
              ]
    ]
    window = sg.Window("AI-Typing-Assistant", layout)

    while True:
        event, values = window.read()
        window["-EDIT-"].update(text)

        if event == sg.WIN_CLOSED or event == 'Close':
            break
        if event == "Copy & Close":
            pyperclip.copy(values["-EDIT-"])
            break
        if event == "Execute":
            action = values["-OPTIONS-"]
            result=""
            while not result:
                result=fix_text(action, values["-EDIT-"])
                if not result:
                    if sg.popup_yes_no("Error: Fail to get new text! Retry?") == "No":
                        break
                    else:
                        continue
                # print(new_text)
                if LABEL1 in result and LABEL2 in result:
                    result = "".join(result.split(LABEL1)[1].split(LABEL2)[0])
                    print("Rslt:",result)
                else:
                    if sg.popup_yes_no("Error: Bad format! Retry?") == "No":
                        break
                    else:
                        continue
                text = result
            window["-EDIT-"].update(text)
            

    window.close()

# Flag to indicate whether the program should continue running.
is_alive = True

# Declare some key bindings.
# Bindings take on the form of:
#   <binding>, on_press_callback, on_release_callback, actuate_on_partial_release_flag, callback_params
#
# *Note that callback_params will be passed to both press and release callback functions
bindings = [
    ["control + f9", None, on_f9, True],
]

# Register all of our keybindings
register_hotkeys(bindings)

# Finally, start listening for keypresses
start_checking_hotkeys()

print("Ready! You can hide this window now.")

# Keep waiting until the user presses the exit_application keybinding.
# Note that the hotkey listener will exit when the main thread does.
while is_alive:
    time.sleep(0.1)