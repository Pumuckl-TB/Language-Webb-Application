import dash
import dash_core_components as dcc
import dash import html
from dash.dependencies import Input, Output
import requests   

app = dash.Dash()

app.layout = html.Div([
    html.H1("Simple input example"),
    dcc.Input(
        id='input-num1',
        placeholder='Insert num1 value',
        type='number',
        value='4',
    ),
    dcc.Input(
        id='input-num2',
        placeholder='Insert num2 value',
        type='number',
        value='3',
    ),
    html.Br(),
    html.Br(),
    html.Div(id='result')
    ])


@app.callback(
    Output('result', 'children'),
    [Input('input-num1', 'value'),
     Input('input-num2', 'value')]
)

def update_result(num1, num2):
    sum_arguments = {'x': num1, 'y': num2}
    url ='http://35.228.247.229:5000/get_sum'
    response = requests.get(url = url,  params=sum_arguments)
    print(response.url)
    print(response.json())
    return "The sum is: {}".format(response.json())

if __name__ == '__main__':
     app.run_server(host = '0.0.0.0', port = 8050, debug = True)
