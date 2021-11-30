import base64
import datetime
import io
import sys
import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
from dash import dash_table
import requests
import plotly.express as px
from dash import callback_context
import pandas as pd
import json


website = 'http://127.0.0.1:5000/adduser'
external_stylesheets = [dbc.themes.BOOTSTRAP, "https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions=True

journey_check = pd.read_csv("progress_items+(Confidential).csv")
#journey_request = requests.post("http://127.0.0.1:5000/get_data_by_item_id", json={0:0})
#journey_check = pd.read_json(journey_request.text)

# Select Student
request = requests.post(url="http://127.0.0.1:5000/getusers", json=0)
student_df = pd.read_json(request.text)
student_df["value"] = student_df["user_id"]
student_df["label"] = student_df["name"] + " " + student_df["surname"]

student_df = student_df[["value","label"]].to_dict("records")
#print(student_df[0])


# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Menu", className="display-4"),
        html.Hr(),
        html.P("Teacher Module", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("Admin", href="/admin", active="exact"),
                dbc.NavLink("Upload Data", href="/upload", active="exact"),
                dbc.NavLink("Track Performance", href="/performance", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

# Graph Data
fig = {'data': [{'x': [0, 0, 0], 'y': [0,0,0], 'type': 'bar', 'name': 'Please select a student first'}]}

# Set up the layout
app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])


# Sidebar Function
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/admin":
        return [
                html.H1('Add / Remove Student',
                        style={'textAlign':'center'}),
                html.Div([
                    html.Div(dcc.Input(id='input-on-submit', type='text', placeholder='Name', size='25', autoFocus='autoFocus')),
                    html.Div(dcc.Input(id='input-on-submit2', type='text', placeholder='Surname', size='25')),
                    html.Div(dcc.Input(id='input-on-submit3', type='email', placeholder='Email', size='25')),
                    html.Div(dcc.Input(id='input-on-submit4', type='number', placeholder='Exercise Duration in minutes', size='25')),
                    html.Div(dcc.Input(id='input-on-submit5', type='text', placeholder='Objective', size='25')),
                    html.Button('Add', id='submit-val1', n_clicks=0,
                                style={'backgroundColor':'#0d6efd', 'color':'white', 'border':'1px black solid', 'width':'11%', 'height':'40px', 'text-align':'center', 'marginRight':'5px', 'marginTop':'5px'}),
                    html.Button('Remove', id='submit-val2', n_clicks=0,
                                style={'backgroundColor':'#fc0f22', 'color':'white', 'border':'1px black solid', 'width':'11%', 'height':'40px', 'text-align':'center', 'marginRight':'5px', 'marginTop':'5px'}),
                    html.Div(id='container-button-basic', children='Add or remove a Student'),
                ], style={'horizontalAlign': 'middle'}),
        ]
    elif pathname == "/upload":
        return [
                html.H1('Upload Data',
                        style={'textAlign':'center'}),
                html.Div([
                    dcc.Upload(
                        id='upload-data',
                        children=html.Div([
                            'Drag and Drop or ',
                            html.A('Select Files')
                        ]),
                        style={
                            'width': '100%',
                            'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin': '10px'
                        },
                        # Allow multiple files to be uploaded
                        multiple=True
                    ),
                    html.Div(id='output-data-upload'),
                ])
                ]
    elif pathname == "/performance":
        return [
                html.H1('Track Student Performance',
                        style={'textAlign':'center'}),
                html.Div([
                    dcc.Dropdown(
                        id='student-dropdown',
                        options=student_df,
                        placeholder="Select a student", className="mb-3",
                    ),
                    html.Div(id='dd-output-container'),
                    ]),
                html.Div([
                    dcc.Tabs(id="tabs", children=[
                        dcc.Tab(label='Journey', value='tab-journey'),
                        dcc.Tab(label='Performance', value='tab-performance'),
                        dcc.Tab(label='Recommendation', value='tab-recommendation'),
                    ]),
                    html.Div(id='tabs-content')
                ]),
                ]
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


# Upload Function
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8',errors="ignore")))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        return html.Div([
            'There was an error processing this file.'
        ])
    payload = df.to_json()
    request = requests.post('http://127.0.0.1:5000/importdata', json=payload)
    f = html.Div([
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),
        html.Hr(),  # horizontal line
        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])
    return f


# Upload Callback
@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


# Select Student Callback
@app.callback(
    Output('dd-output-container', 'children'),
    Input('student-dropdown', 'value')
)
def update_output(value):
    json_userid = {"user_id": value}
    if value:
        request2 = requests.post(url="http://127.0.0.1:5000/returnuserperf", json=json_userid)
        ddf_performance2 = request2.text
        dict = json.loads(ddf_performance2)
        performance = dict["average_time"]
        request5 = requests.post(url="http://127.0.0.1:5000/recomandiation_duration", json=json_userid)
        ddf_duration = request5.text
        ddf_duration = json.loads(ddf_duration)
        global duration
        duration = ddf_duration["time_in_min"]
        request5 = requests.post(url="http://127.0.0.1:5000/weak_points", json=json_userid)
        ddf_weak_points = pd.read_json(request5.text)
        weak_points = json.loads(ddf_weak_points)
        weak_points = pd.read_json(weak_points)# here you get a pandas frame with the weak points

        '''
        request3 = requests.post(url="http://127.0.0.1:5000/recomandiation_hot", json=json_userid)
        ddf_hot_topics = pd.read_json(request3.text)
        request4 = requests.post(url="http://127.0.0.1:5000/recomandiation_ml", json=json_userid)
        ddf_weak_points = pd.read_json(request4.text)
        request5 = requests.post(url="http://127.0.0.1:5000/recomandiation_duration", json=json_userid)
        ddf_duration = pd.read_json(request5.text)
        global time_min
        time_min = ddf_duration["time_in_min"]
        '''
        global fig
        fig = {'data': [{'x': [2], 'y': [performance], 'type': 'bar', 'name': 'Duration'}]}

    return 'You have selected User {}'.format(value)

#def hot_topics(value2):
#    if value2:
#        str2 = str(value2)
#        splitted2 = str2.replace(" ", "")
#        splitted2 = splitted2.split(",")
#        item_ids = {"item_ids":splitted2}
#        request = requests.post(url="http://127.0.0.1:5000/item_ids", json=item_ids)
#        frame = request.text
#        global df
#        df = json.loads(frame)
#        df = pd.DataFrame(df)



#def looks_for_input():
#    x = 0
#    while x == 0:
#        try:
#            df
#            x = 1
#        except:







# Tabs Callback
@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-journey':
        #print(student_df)
        return html.Div([
            html.H3('Journey'),
            dash_table.DataTable(
                id='datatable-interactivity',
                columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in journey_check.columns],
                data=journey_check.to_dict('records'),
                editable=False,
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                column_selectable="single",
                row_selectable="multi",
                row_deletable=False,
                selected_columns=[],
                selected_rows=[],
                page_action="native",
                page_current=0,
                page_size=10,
            ),
        ])
    elif tab == 'tab-performance':
        #print(student_df)
        return html.Div([
            html.H3('Performance'),
            dcc.Graph(figure=fig),
        ])
    elif tab == 'tab-recommendation':
        #print(student_df)
        return html.Div([
            html.H3('Recommendation'),
            html.Div(children='Hot Topics: ', style={'color': '#0d6efd'}),
            dash_table.DataTable(
                id='datatable-interactivity',
                columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in journey_check.columns],
                data=journey_check.to_dict('records'),
                editable=False,
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                column_selectable="single",
                row_selectable="multi",
                row_deletable=False,
                selected_columns=[],
                selected_rows=[],
                page_action="native",
                page_current=0,
                page_size=10,
            ),
            html.Div(children='Weak Points: ', style={'color': '#0d6efd'}),
            dash_table.DataTable(
                id='datatable-interactivity',
                columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in journey_check.columns],
                data=journey_check.to_dict('records'),
                editable=False,
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                column_selectable="single",
                row_selectable="multi",
                row_deletable=False,
                selected_columns=[],
                selected_rows=[],
                page_action="native",
                page_current=0,
                page_size=10,
            ),
            html.Div(children='Duration: ', style={'color': '#0d6efd'}),
            html.H1(f'{duration}min of duration'),

        ])


# Checklist Datatable Callback
@app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    Input('datatable-interactivity', 'selected_columns')
)
def update_styles(selected_columns):
    return [{
        'if': {'column_id': i},
        'background_color': '#D2F3FF'
    } for i in selected_columns]


# Add/Remove Callback
@app.callback(
    Output('container-button-basic', 'children'),
    Input('submit-val1', 'n_clicks'),
    Input('submit-val2', 'n_clicks'),
    State('input-on-submit', 'value'),
    State('input-on-submit2', 'value'),
    State('input-on-submit3', 'value'),
    State('input-on-submit4', 'value'),
    State('input-on-submit5', 'value'),
)
def update_output(n_clicks1, n_clicks2, value, value2, value3, value4, value5):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'submit-val1' in changed_id:
        payload = {'name': value, "surname": value2, 'email': value3, "duration": value4, "objective": value5}
        request = requests.post('http://127.0.0.1:5000/adduser', json=payload)
        return 'Output: {}'.format(request.text)
    elif 'submit-val2' in changed_id:
        print(n_clicks2)
        payload = {'email': 'wasauch561immer'}
        request = requests.post('http://127.0.0.1:5000/remove', json=payload)
        return 'Output: {}'.format(request.text)

    #valuedict = {"name": value, "surname": value2, "email": value3, "time": value4, "objective": value5}
    #print(valuedict)
    #print(value2)
    #return 'Output: {}'.format(value)
#valuedict = {"name": "peter", "surname":"meier","email":"petermeier@watever", "time":"inte","objective":"jzhvuzvjzg"}

if __name__=='__main__':
    app.run_server(debug=True, port=5444)