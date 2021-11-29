import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc
import requests


##################### Initialise Variables  #####################
url_backend = 'http://localhost:5000'
df = pd.read_json(f'{url_backend}/students')

# -> to be replaced with Backend GetProgressItems()
data_ht = {
    'item_id': [0,1,2,3,4,5], 
    'field': ['vocabulary','vocabulary','vocabulary','vocabulary','vocabulary','vocabulary'], 
    'area_name': ['General Concepts','General Concepts','General Concepts','General Concepts','General Concepts','General Concepts'],
    'area_order':[10,10,10,10,10,10],
    'section_name':['Time','Day and Week','Month and Year','Space','Numbers','Colors'],
    'section_order':[100,110,120,130,140,150]}
df_ht = pd.DataFrame(data=data_ht)

######################## Initialise app  ########################

app = dash.Dash() 

######################## Dash App Layout  ########################


app.layout = html.Div(style={'backgroundColor':'#FFFFFF'},
    children=[
    html.P(id='delete_student_placeholder', hidden=True), # Create placeholder for functions without callback
    html.P(id='add_student_placeholder', hidden=True), # Create placeholder for functions without callback
    html.P(id='assign-placeholder', hidden=True), # Create placeholder for functions without callback
    dcc.Store(id='student_firstname_lastname'), # Create storage value for get_row_info()
    dcc.Store(id='topic_id_temp'), # Create storage value for get_row_info()
            
    html.Div(className='row', style={'backgroundColor':'#FFD6A0'}, # Top Row and banner
        children=[
            html.H2('Personal German',style={'color': '#333331', 'text-align':'right', 'margin-right': '35px','padding-top': '15px', 'font-size': '30px', 'vertical-align':'center'}),
            html.H4('Learn Fluent German in 1 Year',style={'color': '#333331', 'text-align':'right', 'margin-right': '35px','font-size': '15px', 'vertical-align':'center'}),
      ]),
    html.Div(className='row', style={'backgroundColor':'#D52330'}, # Top red banner
        children=[
            html.Br(),
        ]
      ),

    html.Div(className='row',
        children=[
            html.Div(className='two columns div-for-charts', style={'background':'#393C3D'},
                 children = [
                    html.H2('Teacher View', style={'color': '#FFD6A0','margin-left':'15px'}),
                    html.Br(),
                    html.Br(),
                    dcc.Link('Admin Page', href='https://plot.ly', style={'color': 'white','font':'arial','margin-left':'35px'}), #replace the link!
                    html.Br(),
                    html.A('Exercise', href='https://plot.ly', style={'color': 'white','margin-left':'35px'}), #replace the link!
                    html.Br(),
                    html.A("Dashboard", href='https://plot.ly', style={'color': 'white','margin-left':'35px'}), #replace the link!
                    html.Br(),
                    html.H2('Student View', style={'color': '#FFD6A0','margin-left':'15px'}),
                    html.A("Solve Exercises", href='https://plot.ly', style={'color': 'white','margin-left':'35px'}), #replace the link!
                    html.Br()],
                    ),
            
        
            html.Div(className='ten columns div-charts', # Define the right element
                style = { 'display': 'flex', 'flex-direction': 'column', 'height': '100vh','width': '60%'},
                children = [
                    
                    html.Div(children=[

                    
                    html.H2('Enrolled Students',style={'color': 'black'}),
                   
                    # Students Table
                    dbc.Container([ 
                    dt.DataTable(
                    id='tbl', data=df.to_dict('records'),
                    columns=[{"name": i, "id": i} for i in df.columns],
                    style_header={
                        'backgroundColor': 'white',
                        'fontWeight': 'bold',
                        'color': 'black'
                    },
                    style_filter = {
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'color': 'black'
                    },
                    style_data={
                        'backgroundColor': 'rgb(245, 245, 245)',
                        'color': 'black'
                    },
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    row_selectable="single",
                    cell_selectable=False,
                    selected_columns=[],
                    selected_rows=[],
                    page_action="native",
                    page_current= 0,
                    page_size= 10,
                    ),
                    ]),
                
                html.H2('Tasks',style={'color': 'black'}),
                # Progress table
                dbc.Container([
                    dt.DataTable(
                    id='tbl-ht', data=df_ht.to_dict('records'),
                    columns=[{"name": i, "id": i} for i in df_ht.columns],
                    style_header={
                        'backgroundColor': 'white',
                        'fontWeight': 'bold',
                        'color': 'black'
                    },
                    style_filter = {
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'color': 'black'
                    },
                    style_data={
                        'backgroundColor': 'rgb(245, 245, 245)',
                        'color': 'black'
                    },
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    row_selectable="single",
                    cell_selectable=False,
                    selected_columns=[],
                    selected_rows=[],
                    page_action="native",
                    page_current= 0,
                    page_size= 10,
                    
                    ),
                ]),

                # Delete Button
                html.Div(
                    children = [
                        html.H2('Controls',style={'color': 'black'}),
                        html.P('''Select student in the table, then press the DELETE button''',style={'color': 'black'}),
                        html.Button('Delete', id='delete-button', n_clicks=0, className='button'),
                        html.P('',style={"margin-top": "15px"}),
                        
                        # Add Student Button
                        html.P('''To add a Student to the database, fill out the fields below and click "Add"''', style={'color': 'black'}),
                        html.Div([
                            dcc.Input(id='firstname', placeholder='Firstname...', type="text", className='input', style={'width':'15%','display': 'inline-block'}),
                            dcc.Input(id='lastname', placeholder='Lastname...', type="text", className='input', style={'width':'15%','display': 'inline-block'}),
                            dcc.Input(id='email', placeholder='Email...', type="text", className='input', style={'width':'35%','display': 'inline-block'}),
                            dcc.Input(id='exercise_duration', placeholder="Duration", type="number", className='input', style={'width':'15%','display': 'inline-block'}),
                            dcc.Input(id='objective', placeholder='Objective...', type="text", className='input', style={'width':'10%','display': 'inline-block'})
                            ]),
                        html.Button('Add', id='add-button', n_clicks=0, className='button'),
                    
                    # Assign Student an exercise

                    html.Br(),
                    html.P('''Select Student, exercise, and click "Assign"''', style={'display': 'inline-block', 'color':'black'}),
                    
                    # Assign Button
                    html.Button('Assign Item', id='assign-button', n_clicks=0, className='button'),

                    ]),
                    html.Br(),
                    html.Br(),
                    html.Br(),



                ]),
            ]),
        ]) 
])


################## CALLBACKS AND FUNCTIONS #################

@app.callback(
    Output('tbl', 'data'),
    Input('delete_student_placeholder', 'children'),
    Input('add_student_placeholder', 'children')
    )

def update_table(children1, children2):
    '''
    This function retrieves the new Dataframe when there is an update.
    '''

    print('updating table')
    df = pd.read_json(f'{url_backend}/students')
    return df.to_dict('records')


@app.callback(
    Output('student_firstname_lastname', 'data'), # student_firstname_lastname is used to save studentID in dcc.Store
    Input('tbl', 'selected_rows'),
    Input('tbl','data'),
    )

def get_row_info(selected_rows, data):
    '''
    Function which retrieves the info of the selected row.
    '''
    print(f'selected row: {selected_rows}')

    name = df.loc[selected_rows,'name'].values
    surname = df.loc[selected_rows,'surname'].values
    try:
        json_text = {'name': name[0], 'surname': surname[0]}
    except:
        json_text = None
    print(f'selected student: {json_text}')

    return json_text

#### Delete button
@app.callback(
    Output('delete_student_placeholder', 'children'),
    Input('delete-button', 'n_clicks'),
    Input('student_firstname_lastname', 'data')
)
def delete_button_press(n_clicks, student_firstname_lastname):
    '''
    This function deletes the student out of the dataframe when the delete 
    button is pressed.
    Process:
        1. Check if delete_button has been clicked 
            (-> has n_clicks changed and is it > 0) 
        2. Delete student with API call
        3. return student_firstname_lastname to 
            delete_student_placeholder, to initiate table update
    '''
    
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'delete-button' in changed_id and n_clicks>0:

        print(f"deleting: student {student_firstname_lastname}")
        
        response = requests.post(f'{url_backend}/deletestudent', json=student_firstname_lastname)
        print(response.text)
        
        return str(student_firstname_lastname)
    
    else:
        print("delet_button_press has passed")
        pass

    return None

#### Add student button
@app.callback(
    Output('add_student_placeholder', 'children'),
    [Input('add-button', 'n_clicks'),
    Input('firstname', 'value'),
    Input('lastname', 'value'),
    Input('email', 'value'),
    Input('exercise_duration', 'value'),
    Input('objective', 'value')],
    State=[State('firstname','value'),
            State('lastname', 'value'),
            State('email','value'),
            State('exercise_duration','value'),
            State('objective','value')]
)

def add_button_press(n_clicks, firstname, lastname, email, exercise_duration, objective):
    '''
    This function adds the student to of the dataframe when the delete 
    button is pressed. The Info (firstname, lastname) is written into
    the textboxes (firstname, lastname).
    Process:
        1. Check if add-button has been clicked 
            (-> has n_clicks changed and is it > 0)  
        2. Create a json in the right format that it can be read by 
            the backend.
        3. Pass json to backend with /addstudent call.
    '''
   
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'add-button' in changed_id and n_clicks>0:

        print(f" Adding {firstname},{lastname},{email},{exercise_duration},{objective}.")

        student = {
            'name': [firstname],
            'surname': [lastname],
            'email': [email],
            'exercise_duration': [exercise_duration],
            'objective':[objective]}
        
        student_json = pd.DataFrame.from_dict(student).to_json()

        response = requests.post(f'{url_backend}/addstudent', json=student_json)
        print(response.text)

        return str(student)
    else:
        return None


### functionality for hot topic datatable
@app.callback(
    Output('topic_id_temp', 'data'), 
    Input('tbl-ht', 'selected_rows'),
    Input('tbl-ht','data'),
    )


def get_row_info_ht(selected_rows, data):
    '''
    Function which retrieves the info of the selected row for the Hot topic table.
    
    '''
    print(selected_rows)

    row = df_ht.loc[selected_rows]
    
    try:
        item_id = df_ht.loc[selected_rows,'item_id'].values[0]
    except:
        item_id = None

    print("Section selected:" + str(row))
    print("item_id selected:" + str(item_id))

    return item_id

# assign button
@app.callback(
    Output('assign-placeholder', 'children'),
    Input('assign-button', 'n_clicks'),
    Input('student_firstname_lastname', 'data'),
    Input('topic_id_temp', 'data')
)

def assign_button_press(n_clicks, student_firstname_lastname, topic_id_temp):
    
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'assign-button' in changed_id and n_clicks>0:
        print('click registered')
        # 2. Drop student with the respective ID
        print(f"assigning  exercise {topic_id_temp} to student {student_firstname_lastname}")
        # API CALL here
    
    else:
        print("assign button press has passed")
        pass

    return None


############# Running the app #############

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
    # app.run_server(host = '0.0.0.0', port = 8050, debug = True)


