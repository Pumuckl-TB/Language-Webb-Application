import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash()

app.layout = html.Div(children=[
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
                    html.H1('''Data Studio Dashboard''', style={'padding-top':'17px'}),
                    html.Iframe(src="https://datastudio.google.com/embed/reporting/864eff7d-2c84-4880-a0ee-4be8e203c449/page/zuQfC",
                        style={
                            'height' : '1067px', 'width' : '70%'}
                            ) 
                            
            ])
        ])




if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
    # app.run_server(host = '0.0.0.0', port = 8050, debug = True)