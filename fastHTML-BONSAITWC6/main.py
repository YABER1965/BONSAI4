# ----
from fasthtml.common import *

########################################
# READ DATABASE - FASTLITE
########################################
# https://answerdotai.github.io/fastlite/
db = database('data/todos_qa.db')
dbname = "todos"

global example_messages
global str_goal
global str_step

# ---
def create_message(str_goal, str_step, str_language):
    qry = f'select * from {dbname} WHERE Goal LIKE "{str_goal}%" and Step LIKE "{str_step}%" and Language LIKE "{str_language}%";'
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
    
    return example_messages

# ---
# 初期絞り込み条件
str_goal = "A"
str_step = "1"
str_language = "English"
example_messages = create_message(str_goal, str_step, str_language)

##############################
# MAIN PROGRAM
##############################
# ----
app, rt = fast_app()

# ----
#str_step_show = "This is a step"
#str_goal_show = "This is a goal"

@app.get('/')
def homepage():

    global example_messages
    global str_goal
    global str_step

    # ----
    str_step_show = str_step
    str_goal_show = str_goal

    return Main(H1('Chat Messages'), 
    Div(cls="container")(H2(A("Link to Page 2 (to change sorting)", href="/page2")), Grid(
        P(str_step_show), P(str_goal_show))
    ),
    Div(*[create_chat_message(**msg, msg_num=i) for i, msg in enumerate(example_messages)]))

@app.get("/page2")
def page2():
    return Main(H1("Change sorting condition with the form below:"),
                Form(Select(Option('1'), Option('2'), name='step'),  Select(Option('A'), Option('B'), name='goal'), 
                     Button("Submit"),
                     action="/", method="post"))

@app.post("/")
def add_message(step:str, goal:str):

    global example_messages
    global str_goal
    global str_step

    # ---
    # 初期絞り込み条件
    str_goal = goal
    str_step = step
    str_language = "English"
    example_messages = create_message(str_goal, str_step, str_language)
    return homepage()

# ---
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