import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output, State, MATCH, ALL
import pandas as pd
import dash_bootstrap_components as dbc

import base64
import datetime
import io
import pandas as pd


######################## Initialise app  ########################
df = pd.DataFrame()
app = dash.Dash() 

######################## Dash App Layout  ########################

app.layout = html.Div(children=[
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


################## CALLBACKS AND FUNCTIONS #################

def parse_contents(contents, filename):
    _, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)


    if 'csv' in filename:
        df = pd.read_csv(
            io.StringIO(decoded.decode('utf-8')))

    elif 'xls' in filename:
        df = pd.read_excel(io.BytesIO(decoded))

    print(df.head(5))

    json_file = df.to_json()
    print(json_file)
    # API CALL HERE

    return html.Div([
        html.P('The following file was uploaded:'),
        html.H5(filename),
        dt.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),
    ])

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


