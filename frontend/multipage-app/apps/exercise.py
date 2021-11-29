import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output, State, MATCH, ALL
import pandas as pd
import dash_bootstrap_components as dbc
import re
import time
import requests
from app import app


##################### Intialise Students ######################

url_backend = 'http://localhost:5000'
students = pd.read_json(f'{url_backend}/students')
students['fullname'] = students['name'] + ' ' +students['surname']
sutdents = students.to_dict(orient='list')

##################### Initialise Exercise #####################

# split the tasks into [beginning, solution, end]
def split_exercise(exercise):
    tasks = exercise.get('text_x')
    tasks_split = []

    for task in tasks:
        task_split = re.split('\[|\]', task)
        tasks_split.append(task_split)

    return tasks_split

name = None
surname = None
def create_task_block(name = None, surname = None, type = 'ML'):
    '''
    This function generates a line in the website which shows the task to do.

    Input: index of which task to take [0, 1, 2, 3, ...]

    Logic:
        1. Check StudentID
            a. If no Student is selected, return message to select student
            b. If Student is Selected, get Exercise from backend based on studentID (to be ammended with backend commands)
        2. Check type: if type = ml, the id's are called dynamic-input-ml, dynamic-solution-ml, and dynamic-output-ml, 
           otherwise the same is done but for .... -hottopic
            a. initialise output list
            b. add 1 line consisting of: 
                Start of task, blank, end of task (len <= 3)
                OR
                Start of task, blank, further text, blank, end of task (len >3)
            c. concatenate all lines
        3. Return finished "Exercise Block"

    Many of the values are updated via callbacks at the bottom
    '''
    # output = []
    # if name == None:
    #     return html.H1('Please select student')
    # else:
    #     tasks_split = None

    json_file = {'name': name,'surname': surname}
    
    if type == 'ML':
  
        response = requests.post(f'{url_backend}/ml', json=json_file)
        
        print(response.json())
        exercise = pd.DataFrame.from_dict(response.json()).to_dict(orient='list')
        print(exercise)
        tasks_split = split_exercise(exercise)
        task_ids = exercise.get("task_id")
        
        output = []
        for i in range(0,len(tasks_split)):
            if len(tasks_split[i])<3: # task has no blank
                task_line = html.Div(
                    children=[
                        html.P(tasks_split[i][0], style={'display': 'inline-block'}),
                    ])            
            if len(tasks_split[i])==3: # task has a maximum of 1 blank
                task_line = html.Div(
                    children=[
                        html.P(tasks_split[i][0], style={'display': 'inline-block'}),
                        dcc.Input(id={'type':'dynamic-input-ml0','index':i}, value='', type="text", className='input'),
                        html.P(id={'type':'dynamic-solution-ml0','index':i}, children = tasks_split[i][1], hidden=True), # stores the solution (needed for later) tasks_split[i][1]
                        html.P(tasks_split[i][2], style={'display': 'inline-block'}),
                        html.Div(id={'type':'dynamic-output-ml0','index':i}, style={'display': 'inline-block', 'color':'blue', 'font-family':'arial'})
                    ])
            if len(tasks_split[i])>3: # task has 2 blanks
                task_line = html.Div(
                    children=[
                        html.P(tasks_split[i][0], style={'display': 'inline-block'}),
                        dcc.Input(id={'type':'dynamic-input-ml0','index':i}, value='', type="text", className='input'),
                        html.P(id={'type':'dynamic-solution-ml0','index':i}, children = tasks_split[i][1], hidden=True), # stores the solution (needed for later)
                        html.P(tasks_split[i][2], style={'display': 'inline-block'}),
                        html.Div(id={'type':'dynamic-output-ml0','index':i}, style={'display': 'inline-block', 'color':'blue', 'font-family':'arial'}),
                        dcc.Input(id={'type':'dynamic-input-ml1','index':i}, value='', type="text", className='input'),
                        html.P(id={'type':'dynamic-solution-ml1','index':i}, children = tasks_split[i][3], hidden=True), # stores the solution (needed for later)
                        html.P(tasks_split[i][4], style={'display': 'inline-block'}),
                        html.Div(id={'type':'dynamic-output-ml1','index':i}, style={'display': 'inline-block', 'color':'blue', 'font-family':'arial'})
                    ])
            output.append(task_line)

    else:
        output = []
        response = requests.post(f'{url_backend}/ml', json=json_file)
        
        print(response.json())
        exercise = pd.DataFrame.from_dict(response.json()).to_dict(orient='list')
        tasks_split = split_exercise(exercise)
        print(tasks_split)
        task_ids = exercise.get("task_id")
        print(f'exercise taskid: {exercise.get("task_id")}')


        for i in range(0,len(tasks_split)):
            
            if len(tasks_split[i])<3: # task has no blank
                task_line = html.Div(
                    children=[
                        html.P(tasks_split[i][0], style={'display': 'inline-block'}),
                    ])            
            if len(tasks_split[i])==3: # task has a maximum of 1 blank
                task_line = html.Div(
                    children=[
                        html.P(tasks_split[i][0], style={'display': 'inline-block'}),
                        dcc.Input(id={'type':'dynamic-input-hottopic0','index':i}, value='', type="text", className='input'),
                        html.P(id={'type':'dynamic-solution-hottopic0','index':i}, children = tasks_split[i][1], hidden=True), # stores the solution (needed for later) tasks_split[i][1]
                        html.P(tasks_split[i][2], style={'display': 'inline-block'}),
                        html.Div(id={'type':'dynamic-output-hottopic0','index':i}, style={'display': 'inline-block', 'color':'blue', 'font-family':'arial'})
                    ])
            if len(tasks_split[i])>3: # task has 2 blanks
                task_line = html.Div(
                    children=[
                        html.P(tasks_split[i][0], style={'display': 'inline-block'}),
                        dcc.Input(id={'type':'dynamic-input-hottopic0','index':i}, value='', type="text", className='input'),
                        html.P(id={'type':'dynamic-solution-hottopic0','index':i}, children = tasks_split[i][1], hidden=True), # stores the solution (needed for later)
                        html.P(tasks_split[i][2], style={'display': 'inline-block'}),
                        html.Div(id={'type':'dynamic-output-hottopic0','index':i}, style={'display': 'inline-block', 'color':'blue', 'font-family':'arial'}),
                        dcc.Input(id={'type':'dynamic-input-hottopic1','index':i}, value='', type="text", className='input'),
                        html.P(id={'type':'dynamic-solution-hottopic1','index':i}, children = tasks_split[i][3], hidden=True), # stores the solution (needed for later)
                        html.P(tasks_split[i][4], style={'display': 'inline-block'}),
                        html.Div(id={'type':'dynamic-output-hottopic1','index':i}, style={'display': 'inline-block', 'color':'blue', 'font-family':'arial'})
                    ])
            output.append(task_line)
    
    return output, task_ids
    

######################## Dash App Layout  ########################

layout = html.Div(style={'backgroundColor':'#FFFFFF'}, children=[
    html.Div(className='row', style={'backgroundColor':'#FFD6A0','top': '0', 'width':'100%'}, # Top Row and banner
        children=[
            html.H2('Personal German',style={'color': '#333331', 'text-align':'left', 'margin-top':'0px','padding-top':'12px','margin-right': '35px', 'font-size': '30px', 'vertical-align':'center','padding-left':'25px'}),
            html.H4('Learn fluent german in 1 year',style={'color': '#333331', 'text-align':'left', 'margin-right': '35px','font-size': '15px', 'vertical-align':'center','padding-left':'25px'}),
      ]),
    html.Div(className='row', style={'backgroundColor':'#D52330', 'height':'5px'}, # Top red banner
        children=[
            html.Br(),
        ]
      ),
    #Left Navigation Bar
    html.Div(children=[
        html.Div(className='two columns div-for-charts', style={'background':'#393C3D'},
                children = [
                html.H2('Teacher View', style={'color': '#FFD6A0','margin-left':'15px', 'margin-bottom':'7px'}),
                dcc.Link('Admin Page', href='/apps/admin', style={'color': 'white','margin-left':'30px'}), 
                html.A('Upload Data', href='/apps/upload', style={'color': 'white','margin-left':'30px', 'margin-top':'5px'}),
                html.A("Performance Dashboard", href='/apps/dashboard', style={'color': 'white','margin-left':'30px', 'margin-top':'5px'}), 
                html.H2('Student View', style={'color': '#FFD6A0','margin-left':'15px', 'margin-top':'15px', 'margin-bottom':'7px'}),
                html.A("Solve Exercises", href='/apps/exercise', style={'color': 'white','margin-left':'30px'})],
                ),
        ]),
    html.Div(className='ten columns div-charts', # Define the right element
                style = { 'display': 'flex', 'flex-direction': 'column', 'height': '100vh','width': '60%'},
                children = [
        html.Br(),
        html.H1('Student Exercise View'),
        html.P('Select your name below to solve exercises'),
        html.Div(dcc.Dropdown(
            id='student-selector',
            options = [{'label': label, 'value': value} for label, value in zip(students.get('fullname'),students.get('fullname'))],
            value='Select Student',
            clearable=False,
            ),
        style = {'width':'25%', 'font-family':'arial'}), 
        html.Div(id='output_temp'),
        html.H3('Machine Learning Exercise'),
        # ML block type
        html.Div(id = 'block-container-ml'),      # children = create_task_block(name, surname, type = 'ML')
        
        html.Br(),
        
        html.H3('Hot Topic Exercise'),
        # Hot Topic block type
        html.Div(id = 'block-container-hottopic'), # children = create_task_block(name, surname, type = 'Hot Topic')[0]
        html.Br(),
        html.Button('Click when finished', id='finish-button', n_clicks=0, className='button'),
        html.Div(id='time-elapsed-container'),
        html.Br(),
        html.Div(id='start-time',hidden=True)
                ])
])

################## CALLBACKS AND FUNCTIONS #################

# Callback of select student dropdown ML
@app.callback(
    Output('block-container-ml', 'children'),
    Input('student-selector', 'value'),
)

def update_taskblock_ml(value):
    print(f'New Student selected ml: {value}')
    name = value.split(' ')[0]
    surname = value.split(' ')[1]

    return create_task_block(name, surname, type = 'ML')[0]


# Callback of select student dropdown hot topic
@app.callback(
    Output('block-container-hottopic', 'children'),
    Input('student-selector', 'value'),
)
def update_taskblock_hottopic(value):
    print(f'New Student selected ht: {value}' )
    name = value.split(' ')[0]
    surname = value.split(' ')[1]
    return create_task_block(name, surname, type = 'Hot Topic')[0]

# Callback of select student to start timer
@app.callback(
    Output('start-time', 'children'),
    Input('student-selector', 'value'),
)

def start_timer(value):
    start = time.time()
    return start


# Checking entries of first block
@app.callback(
    Output({'type': 'dynamic-output-ml0', 'index': MATCH}, 'children'),
    Input({'type': 'dynamic-input-ml0', 'index': MATCH}, 'value'),
    Input({'type': 'dynamic-solution-ml0', 'index': MATCH}, 'children'),
    State=State({'type': 'dynamic-input-ml0', 'index': MATCH}, 'value')
)

def update_taskinput(value,children):
    print(f'New Input Task: '+ value + ' | Solution: ' + children)
    
    if value == str(children):
        return ' ✓ Korrekt'
    else:
        return ' ✗ Falsch'

# Checking entries of first block
@app.callback(
    Output({'type': 'dynamic-output-ml1', 'index': MATCH}, 'children'),
    Input({'type': 'dynamic-input-ml1', 'index': MATCH}, 'value'),
    Input({'type': 'dynamic-solution-ml1', 'index': MATCH}, 'children'),
    State=State({'type': 'dynamic-input-ml1', 'index': MATCH}, 'value')
)

def update_taskinput(value,children):
    print(f'New Input Task: '+ value + ' | Solution: ' + children)
    
    if value == str(children):
        return ' ✓ Korrekt'
    else:
        return ' ✗ Falsch'

# Checking entries of second block
@app.callback(
    Output({'type': 'dynamic-output-hottopic0', 'index': MATCH}, 'children'),
    Input({'type': 'dynamic-input-hottopic0', 'index': MATCH}, 'value'),
    Input({'type': 'dynamic-solution-hottopic0', 'index': MATCH}, 'children'),
    State=State({'type': 'dynamic-input-hottopic0', 'index': MATCH}, 'value')
)

def update_taskinput(value,children):
    print(f'New Input Task: '+ value + ' | Solution: ' + children)
    
    if value == str(children):
        return ' ✓ Korrekt'
    else:
        return ' ✗ Falsch'


@app.callback(
    Output({'type': 'dynamic-output-hottopic1', 'index': MATCH}, 'children'),
    Input({'type': 'dynamic-input-hottopic1', 'index': MATCH}, 'value'),
    Input({'type': 'dynamic-solution-hottopic1', 'index': MATCH}, 'children'),
    State=State({'type': 'dynamic-input-hottopic1', 'index': MATCH}, 'value')
)

def update_taskinput(value, children):
    print(f'New Input Task: '+ value + ' | Solution: ' + children)
    
    if value == str(children):
        return ' ✓ Korrekt'
    else:
        return ' ✗ Falsch'



@app.callback(
    Output('time-elapsed-container', 'children'),
    Input('finish-button', 'n_clicks'),
    Input('start-time', 'children'),
    Input('student-selector', 'value')

)
def finish_button_press(n_clicks, children, value):
    output = None 

    name = value.split(' ')[0]
    surname = value.split(' ')[1]

    # Check if button has been clicked
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'finish-button' in changed_id and n_clicks>0:
        end = time.time()
        start = children
        elapsed = (end - start)
        output = f'Time elapsed: {round(elapsed/60,2)} minutes'
        task_ids = create_task_block(name, surname, type = 'ML')[1]
        task_ids += create_task_block(name, surname, type = 'Hot Topic')[1]

        json_list = [[]]
        for task in task_ids:
            row = [name, surname, task, (elapsed)/len(task_ids)]
            json_list.append(row)
        json_output = pd.DataFrame(columns=['name','surname','task','elapsed'], data=json_list).dropna().to_json()
 
        print(json_output)
        
    else:
        pass

    return output

############# Running the app #############

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
    # app.run_server(host = '0.0.0.0', port = 8050, debug = True)