import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from app import server
from apps import admin, dashboard, upload, exercise


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/admin':
        return admin.layout
    if pathname == '/apps/dashboard':
        return dashboard.layout
    if pathname == '/apps/upload':
        return upload.layout
    if pathname == '/apps/exercise':
        return exercise.layout
    if pathname == '/':
        return admin.layout
    else:
        return "404 Page Error!"



if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=False) #host='0.0.0.0'