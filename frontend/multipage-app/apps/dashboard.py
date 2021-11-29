import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app

layout = html.Div(children=[
    html.Div(className='row', style={'backgroundColor':'#FFD6A0'}, # Top Row and banner
        children=[
            html.H2('Personal German',style={'color': '#333331', 'text-align':'left', 'margin-top':'0px','padding-top':'12px','margin-right': '35px', 'font-size': '30px', 'vertical-align':'center','padding-left':'25px'}),
            html.H4('Speak fluent german in 1 year',style={'color': '#333331', 'text-align':'left', 'margin-right': '35px','font-size': '15px', 'vertical-align':'center','padding-left':'25px'}),
      ]),
    html.Div(className='row', style={'backgroundColor':'#D52330', 'height':'5px'}, # Top red banner
        children=[
            html.Br(),
        ]
      ),
    #Left Navigation Bar
    html.Div(children=[
        html.Div(className='two columns div-for-charts', style={'background':'#393C3D'},
                children = [
                html.H2('Teacher View', style={'color': '#FFD6A0','margin-left':'15px', 'margin-bottom':'7px'}),
                dcc.Link('Admin Page', href='/apps/admin', style={'color': 'white','margin-left':'30px'}), 
                html.A('Upload Data', href='/apps/upload', style={'color': 'white','margin-left':'30px', 'margin-top':'5px'}),
                html.A("Performance Dashboard", href='/apps/dashboard', style={'color': 'white','margin-left':'30px', 'margin-top':'5px'}), 
                html.H2('Student View', style={'color': '#FFD6A0','margin-left':'15px', 'margin-top':'15px', 'margin-bottom':'7px'}),
                html.A("Solve Exercises", href='/apps/exercise', style={'color': 'white','margin-left':'30px'})],
                ),
        ]),
            
            html.Div(className='ten columns div-charts', # Define the right element
                style = { 'display': 'flex', 'flex-direction': 'column', 'height': '100vh','width': '60%'},
                children = [
                    html.H1('Performance Dashboard', style={'padding-top':'20px'}),
                    html.Iframe(src="https://datastudio.google.com/embed/reporting/864eff7d-2c84-4880-a0ee-4be8e203c449/page/zuQfC",
                        style={
                            'height' : '1900px', 'width' : '100%'}
                            ) 
                            
            ])
        ])




if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
    # app.run_server(host = '0.0.0.0', port = 8050, debug = True)