
from dash import html, dcc
from dash.dependencies import Input, Output 
from pages.elements import navbar, footer
from processes import update_data

# Timing variables in minutes
T_DATAFETCH = 180 # 180 minutes, 3 hours

from app import app
from app import server

# Connect to your app pages
from pages import overview, prediction

app.layout = html.Div([
    # -- Top
    dcc.Location(id='url', refresh=False), 
    navbar,

    # -- Content
    html.Div(id='page-content', children=[]),
    # -- Bottom
    html.Div(style={'padding': '10px'}),
    footer,

    # Refresh data timer 
    dcc.Interval(id='interval-component',interval=(T_DATAFETCH)*(60*1000)),         
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname'), Input('url', 'href')])
def display_page(pathname,href):
    pathname = str(pathname)

    # Change layout with navigation to a new url
    if pathname == '/':  
        return overview.layout 
    if pathname == '/overview':  
        return overview.layout 
    if pathname == '/insight':  
        return prediction.layout 
    if pathname == '/robots.txt':
        # Has to be in assets file 
        return  dcc.Location(pathname="assets/robots.txt", id="a123") 
    if pathname == '/sitemap.xml':
        # Has to be in assets file
        return dcc.Location(pathname="assets/sitemap.xml", id="b123")
    else:
        return overview.layout 
         

@app.callback(Output('page-content', 'n_clicks'),
                Input('interval-component', 'n_intervals'))
def update_backend(n): 
    print('Run')
    update_data()

if __name__ == '__main__':
    app.run_server(debug=True)

