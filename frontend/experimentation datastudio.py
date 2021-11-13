import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash()

app.layout = html.Div(children=[
    html.Div(className='row',  # Define the row element
        children=[ # Define the left element
            html.Div(className='three columns div-user-controls',
                children = [
                    html.H2('Teacher View',style={'color': 'white'}),
                    html.Br(),
                    html.Br(),
                    html.P('''Admin Page''',style={'color': 'white'}),
                    html.Br(),
                    html.P('''Exercises''',style={'color': 'white'}),
                    html.Br(),
                    html.P('''Dashboard''',style={'color': 'white'}),
                ],
                style={'backgroundColor': '#1E1E1E'}),
            
            html.Div(className='nine columns div-user-controls bg-grey', # Define the right element
                children = [
                    html.H2('Right Side Element',style={'color': 'white'}),
                    html.P('''Data Studio Dashboard''',style={'color': 'white'}),
                    html.Iframe(src="https://datastudio.google.com/embed/reporting/864eff7d-2c84-4880-a0ee-4be8e203c449/page/zuQfC",
                        style={
                            'height' : '1067px', 'width' : '70%'}
                            ) 
                            
            ])
        ])
])



if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
    # app.run_server(host = '0.0.0.0', port = 8050, debug = True)