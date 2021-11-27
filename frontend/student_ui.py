import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output, State, MATCH, ALL
import pandas as pd
import dash_bootstrap_components as dbc
import re





##################### Initialise Exercise  #####################
# -> to be replaced with Backend: GetExercise()

exercise = {
    'grammar_section' : 'Grammar Section...',
    'block_name':'Exercise Title...',
    'tasks' : ['Die Heimatstadt des [Mann] ist Porto.',
        'Ich sehe den [schnellen] Mann.', 
        'Dieses seminar ist [zuviel] Arbeit.', 
        'Ich wünschte ich [hätte] es nie gewhält.']
    }

# split the tasks into [beginning, solution, end]
tasks = exercise.get('tasks')
tasks_split = []

for task in tasks:
    task_split = re.split('\[|\]', task)
    tasks_split.append(task_split)

num_tasks = len(tasks_split)


def generate_task_entry(i):
    '''
    This function generates a line in the website which shows the task to do
    '''
    output = html.Div(children=[
        html.P(tasks_split[i][0], style={'display': 'inline-block'}),
        dcc.Input(id={'type':'dynamic-input','index':i}, value='', type="text", className='input'),
        html.P(id={'type':'dynamic-solution','index':i}, children = tasks_split[i][1], hidden=True),
        html.P(tasks_split[i][2], style={'display': 'inline-block'}),
        html.Div(id={'type':'dynamic-output','index':i}, style={'display': 'inline-block', 'color':'red'})
        ])
    return output



######################## Initialise app  ########################

app = dash.Dash() 

######################## Dash App Layout  ########################

app.layout = html.Div(children=[

    html.H1('Student Exercise View'),
    html.Br(),
    html.H2('Section: ' + exercise.get('grammar_section')),
    html.Br(),
    html.H3('Exercise: ' + exercise.get('block_name')),
    html.Br(),

    # Task entries
    html.Div(children=[generate_task_entry(i) for i in range(0,num_tasks)])        
])



################## CALLBACKS AND FUNCTIONS #################

# Initialise range of 
i = range(0,num_tasks)

@app.callback(
    Output({'type': 'dynamic-output', 'index': MATCH}, 'children'),
    Input({'type': 'dynamic-input', 'index': MATCH}, 'value'),
    Input({'type': 'dynamic-solution', 'index': MATCH}, 'children'),
    State=State({'type': 'dynamic-input', 'index': MATCH}, 'value')
)

def update_taskinput(value,children):
    print(f'New Input Task: '+ value + '| Solution: ' + children)
    
    if value == str(children):
        return ' correct'
    else:
        return ' false'



############# Running the app #############

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
    # app.run_server(host = '0.0.0.0', port = 8050, debug = True)


