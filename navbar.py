import dash_bootstrap_components as dbc

def Navbar():
     navbar = dbc.NavbarSimple(
           children=[
              dbc.NavItem(dbc.NavLink("Team", href="/apps/app1")),
              dbc.NavItem(dbc.NavLink("Perso", href="/apps/app2")),
              dbc.NavItem(dbc.NavLink("VS Time", href="/apps/app3")),
              dbc.DropdownMenu(
                 nav=True,
                 in_navbar=True,
                 label="Menu",
                 children=[
                    dbc.DropdownMenuItem("Stats Dybilal", href="/apps/app1"),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("Stats Indiv", href="/apps/app2"),
                    dbc.DropdownMenuItem("Stats vs Time", href="/apps/app3"),
                          ],
                      ),
                    ],
          brand="Home",
          brand_href="/home",
          sticky="top",
        )
     return navbar
