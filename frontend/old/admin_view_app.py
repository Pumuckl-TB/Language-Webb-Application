import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc

##################### Initialise Dataframe  #####################
# -> to be replaced with Backend: GetAllStudentData()
data = {
    'ID': [0,1,2,3,4,5], 
    'Firstname': ['Tatjana','Felix','Räto','Timon','Radu','Debora'], 
    'Lastname': ['Ferri','Jost','Kessler','Bodmer','Tanase','Costa'],
    'Email':['tatjan.ferri@uzh.ch','felix.jost@uzh.ch','raeto.kessler@uzh.ch','timon.bodmer@uzh.ch','radu.tanase@uzh.ch','debora.costa@uzh.ch'],
    'Exercise Durations':['10','15','20','10','20','10'],
    'Goal':['A2','C1','B1','B2','C2','B1']}
df = pd.DataFrame(data=data)


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
    html.P(id='add_student_placeholder',hidden=True), # Create placeholder for functions without callback
    html.P(id='assign-placeholder',hidden=True), # Create placeholder for functions without callback
    dcc.Store(id='student_id_temp'), # Create storage value for get_row_info()
    dcc.Store(id='topic_id_temp'), # Create storage value for get_row_info()
            
    html.Div(className='row', style={'backgroundColor':'#FFD6A0','top': '0', 'width':'100%'}, # Top Row and banner
        children=[
            html.H2('Personal German',style={'color': '#333331', 'text-align':'left', 'margin-top':'0px','padding-top':'12px','margin-right': '35px', 'font-size': '30px', 'vertical-align':'center','padding-left':'25px'}),
            html.H4('Learn Fluent German in 1 Year',style={'color': '#333331', 'text-align':'left', 'margin-right': '35px','font-size': '15px', 'vertical-align':'center','padding-left':'25px'}),
      ]),
    html.Div(className='row', style={'backgroundColor':'#D52330', 'height':'5px'}, # Top red banner
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
                            dcc.Input(id='firstname', value='Firstname...', type="text", className='input', style={'width':'15%','display': 'inline-block'}),
                            dcc.Input(id='lastname', value='Lastname...', type="text", className='input', style={'width':'15%','display': 'inline-block'}),
                            dcc.Input(id='email', value='Email...', type="text", className='input', style={'width':'35%','display': 'inline-block'}),
                            dcc.Input(id='exercise_duration', value='Exercise Duration...', type="text", className='input', style={'width':'15%','display': 'inline-block'}),
                            dcc.Input(id='goal', value='Goal...', type="text", className='input', style={'width':'10%','display': 'inline-block'})
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

def update_table(delete_student_placeholder,add_student_placeholder):
    '''
   This function retrieves the new Dataframe when either the delete or 
   add button are clicked.
    '''
    return df.to_dict('records')


@app.callback(
    Output('student_id_temp', 'data'), # student_id_temp is used to save studentID in dcc.Store
    Input('tbl', 'selected_rows'),
    Input('tbl','data'),
    )

def get_row_info(selected_rows, data):
    '''
    Function which retrieves the info of the selected row.
    '''
    print(selected_rows)

    row = df.loc[selected_rows]
    id = df.loc[selected_rows,'ID']

    print("Student selected:" + str(row))

    return id

#### Delete button
@app.callback(
    Output('delete_student_placeholder', 'children'),
    Input('delete-button', 'n_clicks'),
    Input('student_id_temp', 'data')
)
def delete_button_press(n_clicks, student_id_temp):
    '''
    This function deletes the student out of the dataframe when the delete 
    button is pressed.
    Process:
        1. Check if delete_button has been clicked 
            (-> has n_clicks changed and is it > 0) 
        2. Drop student with the respective ID.
            (-> to be replaced with DeleteStudent() later)
    '''
    
    # 1. Check if delete button has been clicked
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'delete-button' in changed_id and n_clicks>0:

        # 2. Drop student with the respective ID
        print("deleting: student " + str(student_id_temp))
        
        df.drop(df.loc[df['ID']==student_id_temp[0]].index, inplace=True) 
        df.reset_index(inplace=True, drop=True)

        print("new Dataframe")
        print(df)
    
    else:
        print("delet_button_press has passed")
        pass

    return None

#### Add student button
@app.callback(
    Output(component_id='add_student_placeholder', component_property='children'),
    [Input('add-button', 'n_clicks'),
    Input('firstname', 'value'),
    Input('lastname', 'value'),
    Input('email', 'value'),
    Input('exercise_duration', 'value'),
    Input('goal', 'value')],
    State=[State('firstname','value'),
            State('lastname', 'value'),
            State('email','value'),
            State('exercise_duration','value'),
            State('goal','value')]
)

def add_button_press(n_clicks, firstname, lastname, email, exercise_duration, goal):
    '''
    This function adds the student to of the dataframe when the delete 
    button is pressed. The Info (firstname, lastname) is written into
    the textboxes (firstname, lastname).
    Process:
        1. Check if add-button has been clicked 
            (-> has n_clicks changed and is it > 0)  
        3. Write a new row into the dataframe with the student
            (the student firstname and lastname are given as inputs 
            from the State of the textboxes)
            (-> in future call AddStudent() function)
    '''
   
    # 1. Check if delete button has been clicked 
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'add-button' in changed_id and n_clicks>0:

        # 3. Write a new row into the dataframe with the student
        print(f" Adding {firstname},{lastname},{email},{exercise_duration},{goal}.")
        
        id = df.ID.max() + n_clicks
        new_row = df.shape[0]

        df.loc[new_row] = [id,firstname,lastname,email,exercise_duration,goal]

    return None

### functionality for ht datatable
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
    Input('student_id_temp', 'data'),
    Input('topic_id_temp', 'data')
)

def assign_button_press(n_clicks, student_id_temp, topic_id_temp):
    
    # 1. Check if assign button has been clicked
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'assign-button' in changed_id and n_clicks>0:
        print('click registered')
        # 2. Drop student with the respective ID
        print(f"assigning  exercise {topic_id_temp} to student {student_id_temp}")
        # API CALL here
    
    else:
        print("assign button press has passed")
        pass

    return None



############# Running the app #############

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
    # app.run_server(host = '0.0.0.0', port = 8050, debug = True)

