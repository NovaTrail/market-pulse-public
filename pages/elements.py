import dash_bootstrap_components as dbc
from dash import dcc, html 

#logo = html.Img(src='/assets/logo.png', height="30px")
  

# Navigation bar 
navbar = dbc.NavbarSimple(
    children=[  
        dbc.NavItem(dbc.NavLink("Overview", href="/overview")),
        dbc.NavItem(dbc.NavLink("Predictions", href="/insight")),
        dbc.NavItem(dbc.NavLink("About", href="#about", external_link=True)),
    ],
    brand="Market Pulse",
    brand_href="#",
    color="light",
    dark=False,
)  

# Footer 
footer = html.Div([
            dbc.Card(
                dbc.CardBody([
                    dcc.Markdown("""
                        The Raw CPI and PPI Data is provided by the European Commission Eurostat API [© European Union 1995-2022](https://ec.europa.eu/info/legal-notice_en#copyright-notice). 

                    """,style={'font-size': '12px','text-align': 'center'}),
                    dcc.Markdown("""
                        This website provides all information and content 'as is', with no warranties or guarantee of any kind, including but not limited to completeness and accuracy. 
                        This content is for entertainment or general informational purposes only. No part of this website constitutes advice or financial advice. 
                    """,style={'font-size': '12px','text-align': 'justify'}), 
                    ]),
                color="info", 
                inverse=True,
                )
            ]) 
            
