# ----
from fasthtml.common import *
import pandas as pd
import numpy as np
import json

########################################
# READ DATABASE - FASTLITE
########################################
# https://answerdotai.github.io/fastlite/
db = database('data/TEST.db')
dbname = "todos"
qry = f"select * from {dbname};"
data = db.q(qry)
#data[0]
# {'index': 0,
# 'QAtype': 'question',
# 'QAcontent': 'Has the Japanese media accurately reported on the military tensions in East Asia since 2020, and do Chinese and Taiwanese media mirror this sentiment?',
# 'done': 'False'}

# ---
example_messages = []
for row in data:
    #print(f"--- NO: {row['index']} ---")
    #print(row['QAtype'])
    #print(row['QAcontent'])
    # ---
    example_messages.append({"role": row['QAtype'], "content": row['QAcontent']})
# ---
#print(example_messages[0])

##############################
# MAIN PROGRAM
##############################
# ----
app, rt = fast_app()

@app.get('/')
def homepage():
    return Div(*[create_chat_message(**msg, msg_num=i) for i, msg in enumerate(example_messages)])

def create_chat_message(role, content, msg_num):
    if role == 'system': color = '#8B5CF6'
    elif role == 'question': color = "#F000B8"
    else: color = "#37CDBE"
    text_color = '#1F2937'

    # msg 0 = left, msg 1 = right, msg 2 = left, etc.
    alignment = 'flex-end' if msg_num % 2 == 1 else 'flex-start'

    message = Div(Div(
            Div(# Shows the Role
                Strong(role.capitalize()),
                style=f"color: {text_color}; font-size: 0.9em; letter-spacing: 0.05em;"),
            Div(# Shows content and applies font color to stuff other than syntax highlighting
                Style(f".marked *:not(code):not([class^='hljs']) {{ color: {text_color} !important; }}"),
                Div(content),
                style=f"margin-top: 0.5em; color: {text_color} !important;"),
            # extra styling to make things look better
            style=f"""
                margin-bottom: 1em; padding: 1em; border-radius: 24px; background-color: {color};
                max-width: 70%; position: relative; color: {text_color} !important; """),
        style=f"display: flex; justify-content: {alignment};")

    return message

serve()