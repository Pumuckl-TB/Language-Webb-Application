import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output, State, MATCH, ALL
import pandas as pd
import dash_bootstrap_components as dbc
import base64
import io
import pandas as pd


######################## Initialise app  ########################
df = pd.DataFrame()
app = dash.Dash() 

######################## Dash App Layout  ########################

app.layout = html.Div(style={'backgroundColor':'#FFFFFF'}, children=[
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
    html.Div(
        children=[
            html.Div(className='two columns div-for-charts', style={'background':'#393C3D'},
                children = [
                html.H2('Teacher View', style={'color': '#FFD6A0','margin-left':'15px'}),
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
        ]),
    html.Div(className='ten columns div-charts', # Define the right element
        style = { 'display': 'flex', 'flex-direction': 'column', 'height': '100vh','width': '60%'},
        children = [
            html.H1('Welcome to the upload page'),
            html.P(id='dataframe-storage', hidden=True), # Create dataframe storage placeholder
            html.Br(),
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
])


################## CALLBACKS AND FUNCTIONS #################
upload_type = 'None'
def parse_contents(contents, filename):
    '''
    This function takes the files uploaded and concatenates them and parses them.
    The resulting info is saved in a pandas dataframe (df), as well as in a json
    format (json_file).
    The function returns a Dash table with some extra info to visualize the uploaded
    data, however, this is not necessary, just helpful for debugging and visualization.
    '''
    _, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    if 'csv' in filename:
        try:
            df = pd.read_csv(
                io.StringIO(decoded.decode("ISO-8859-1")))
        except:
            df = pd.read_csv(
                io.StringIO(decoded.decode("utf-8")))

    elif 'xls' in filename:
        df = pd.read_excel(io.BytesIO(decoded))

    if 'word_instance' in df.columns:
        upload_type = 'exercise'
        json_file = df.to_json()
        print(json_file)
        # API CALL HERE

    else:
        upload_type = 'word info'
        json_file = df.to_json()
        print(json_file)
        # API CALL HERE

    return html.Div([
        html.H5(f'The following {upload_type} file was uploaded: {filename}'),
        dt.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),
    ])

# update the table
@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'))
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n) for c, n in
            zip(list_of_contents, list_of_names)]
        return children


############# Running the app #############

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
    # app.run_server(host = '0.0.0.0', port = 8050, debug = True)


