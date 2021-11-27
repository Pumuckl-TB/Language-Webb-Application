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
                    html.A("Admin Page", href='https://plot.ly', style={'color': 'white'}), #replace the link!
                    #html.link('''''',style={'color': 'white'}),
                    html.Br(),
                    html.A("Exercise", href='https://plot.ly', style={'color': 'white'}), #replace the link!
                    html.Br(),
                    html.A("Dashboard", href='https://plot.ly', style={'color': 'white'}), #replace the link!
                ],
                style={'backgroundColor': '#1E1E1E'}),
            
            html.Div(className='nine columns div-user-controls bg-grey', # Define the right element
                children = [
                    html.
                            
            ])
        ])
])



if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
    # app.run_server(host = '0.0.0.0', port = 8050, debug = True)