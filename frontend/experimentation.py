import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash()

app.layout = html.Div(children=[
    html.Div(className='row',  # Define the row element
        children=[ # Define the left element
            html.Div(className='four columns div-user-controls',
                children = [
                    html.H2('Teacher View',style={'color': 'white'}),
                    html.P('''Select student to view''',style={'color': 'white'}),
                ],
                style={'backgroundColor': '#1E1E1E'}),
            
            html.Div(className='eight columns div-for-charts bg-grey', # Define the right element
                children = [
                    html.H2('Right Side Element',style={'color': 'white'}),
                    html.P('''Bla Bla Bla''',style={'color': 'white'}),
                    html.Img(src='https://raw.githubusercontent.com/feljost/Language-WebApp/main/frontend/pictures/Placeholder_studenttable.png',
                        style={
                            'height' : '50%',
                            'width' : '50%'}
                            ) 
            ])
        ])
])



if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
    # app.run_server(host = '0.0.0.0', port = 8050, debug = True)