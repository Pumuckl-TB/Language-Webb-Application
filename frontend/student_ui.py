import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output, State, MATCH, ALL
import pandas as pd
import dash_bootstrap_components as dbc
import re
from itertools import repeat


##################### Intialise Students ######################

students = {
    'ID': [0,1,2,3,4,5], 
    'Firstname': ['Tatjana','Felix','Räto','Timon','Radu','Debora'], 
    'Lastname': ['Ferri','Jost','Kessler','Bodmer','Tanase','Costa']
}

##################### Initialise Exercise #####################
# -> to be replaced with Backend: GetExercise()

exercise1 = {
    'grammar_section' : 'Grammar Section...',
    'block_name' : 'Normal Exercise',
    'tasks' : ['Die Heimatstadt des [Mann] ist Porto.',
        'Ich sehe den [schnellen] Mann.', 
        'Dieses seminar ist [zuviel] Arbeit.', 
        'Ich wünschte ich [hätte] es nie gewhält.']
    }

exercise2 = {
    'grammar_section' : 'Grammar Section...',
    'block_name' : 'Tatjana Exercise',
    'tasks' : ['Die Heimatstadt der [Frau] ist Porto.',
        'Ich sehe die [schnelle] Frau.']
    }

exercise_default = {
    'grammar_section' : 'Please Select Student',
    'block_name' : 'Please Select Student',
    'tasks' : ['Please Select Student',
        'Ich sehe die [schnelle] Frau.']
    }


# split the tasks into [beginning, solution, end]
def split_exercise(exercise):
    tasks = exercise.get('tasks')
    tasks_split = []

    for task in tasks:
        task_split = re.split('\[|\]', task)
        tasks_split.append(task_split)

    return tasks_split

id = None
def create_task_block(id, type = 'ML'):
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
                i. start of task
                ii. task solution (saved as hidden html.P & add text entry form)
                iii. end of task 
                iv. Solution container showing if it is correct or not

    Many of the values are updated via callbacks at the bottom
    '''
    if id == None or id == 'Select Student':
        return html.H1('Please select student')
    if id == 0:
        tasks_split = split_exercise(exercise2)

    if id != 0:
        tasks_split = split_exercise(exercise1)

    if type == 'ML':

        output = []
        for i in range(0,len(tasks_split)):
            task_line = html.Div(
                children=[
                    html.P(tasks_split[i][0], style={'display': 'inline-block'}),
                    dcc.Input(id={'type':'dynamic-input-ml','index':i}, value='', type="text", className='input'),
                    html.P(id={'type':'dynamic-solution-ml','index':i}, children = tasks_split[i][1], hidden=True), # stores the solution (needed for later)
                    html.P(tasks_split[i][2], style={'display': 'inline-block'}),
                    html.Div(id={'type':'dynamic-output-ml','index':i}, style={'display': 'inline-block', 'color':'red'})
                ])
            output.append(task_line)

    elif type == 'Hot Topic':
        
        output = []
        for i in range(0,len(tasks_split)):
            task_line = html.Div(
                children=[
                    html.P(tasks_split[i][0], style={'display': 'inline-block'}),
                    dcc.Input(id={'type':'dynamic-input-hottopic','index':i}, value='', type="text", className='input'),
                    html.P(id={'type':'dynamic-solution-hottopic','index':i}, children = tasks_split[i][1], hidden=True), # stores the solution (needed for later)
                    html.P(tasks_split[i][2], style={'display': 'inline-block'}),
                    html.Div(id={'type':'dynamic-output-hottopic','index':i}, style={'display': 'inline-block', 'color':'red'})
                ])
            output.append(task_line)

    return output


######################## Initialise app  ########################

app = dash.Dash() 

######################## Dash App Layout  ########################

app.layout = html.Div(children=[

    html.H1('Student Exercise View'),
    html.Br(),
    html.Div(dcc.Dropdown(
        id='student-selector',
        options = [{'label': label, 'value': value} for label, value in zip(students.get('Firstname'),students.get('ID'))],
        value='Select Student',
        className='dropdown'    
    ),style={"width": "20%"}),
    html.Div(id='output_temp'),


    html.H3('Machine Learning Exercise'),
    # ML block type
    html.Div(children = create_task_block(id, type = 'ML'), id = 'block-container-ml'),      
    
    html.Br(),
    
    html.H3('Hot Topic Exercise'),
    # Hot Topic block type
    html.Div(children = create_task_block(id, type = 'Hot Topic'), id = 'block-container-hottopic')      
])

################## CALLBACKS AND FUNCTIONS #################

# Initialise range of tasks


# Checking entries of first block
@app.callback(
    Output({'type': 'dynamic-output-ml', 'index': MATCH}, 'children'),
    Input({'type': 'dynamic-input-ml', 'index': MATCH}, 'value'),
    Input({'type': 'dynamic-solution-ml', 'index': MATCH}, 'children'),
    State=State({'type': 'dynamic-input-ml', 'index': MATCH}, 'value')
)

def update_taskinput(value,children):
    print(f'New Input Task: '+ value + ' | Solution: ' + children)
    
    if value == str(children):
        return ' ✓ Korrekt'
    else:
        return ' ✗ Falsch'


# Checking entries of second block
@app.callback(
    Output({'type': 'dynamic-output-hottopic', 'index': MATCH}, 'children'),
    Input({'type': 'dynamic-input-hottopic', 'index': MATCH}, 'value'),
    Input({'type': 'dynamic-solution-hottopic', 'index': MATCH}, 'children'),
    State=State({'type': 'dynamic-input-hottopic', 'index': MATCH}, 'value')
)

def update_taskinput(value,children):
    print(f'New Input Task: '+ value + ' | Solution: ' + children)
    
    if value == str(children):
        return ' ✓ Korrekt'
    else:
        return ' ✗ Falsch'


# Callback of select student dropdown ML
@app.callback(
    Output('block-container-ml', 'children'),
    Input('student-selector', 'value'),
)

def update_taskblock_ml(value):
    print(f'New Student selected: {value}' )
    return create_task_block(value, type = 'ML')


# Callback of select student dropdown hot topic
@app.callback(
    Output('block-container-hottopic', 'children'),
    Input('student-selector', 'value'),
)

def update_taskblock_hottopic(value):
    print(f'New Student selected: {value}' )
    return create_task_block(value, type = 'Hot Topic')


############# Running the app #############

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
    # app.run_server(host = '0.0.0.0', port = 8050, debug = True)


