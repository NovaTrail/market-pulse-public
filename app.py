import dash
import dash_bootstrap_components as dbc

my_meta_tags = [
                    {
                    'name': 'title',
                    'content': 'Market Pulse'
                    },
                    {
                    'name': 'description',
                    'content': 'Compare Inflation metrics'
                    },
                    {
                    'name': 'og:description',
                    'content': 'Economic Insights'
                    },
                    {
                    'http-equiv': 'X-UA-Compatible', 
                    'content': 'IE=edge'
                    },
                    {
                    'name': 'viewport', # this meta_tags are required for the app layout to be mobile responsive 
                    'content': 'width=device-width, initial-scale=1.0',}]

app = dash.Dash(__name__, 
                    suppress_callback_exceptions=True,
                    meta_tags=my_meta_tags,
                    external_stylesheets=[dbc.themes.LUX],
                    update_title=None,
                    eager_loading=True,
                )

# # How to use custom js and html in dash app 
# header_scripts =  " "

# app.index_string = '''
# <!DOCTYPE html>
# <html>
#     <head>
#         {%metas%}
#         <title>{%title%}</title>
#         {%favicon%}
#         {%css%}
# ''' + f'''
#     {header_scripts}
# ''' + '''
#     </head>
#     <body>
#         <div></div>
#         {%app_entry%}
#         <footer>
#             {%config%}
#             {%scripts%}
#             {%renderer%}
#         </footer>
#     </body>
# </html>
# '''

app.title = "Market Pulse"

server = app.server 

