# Import packages
from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
from app import db


def create_dashboard(server):
    dash_app = Dash(
        server=server,
        routes_pathname_prefix="/dashboard/",
        external_stylesheets=["styles.css"],
    )

    # Incorporate data
    precipitation = pd.read_sql("precipitation", db.engine)

    dash_app.layout = html.Div(
        id="dash-container",
        children=[
            html.Div(children="WaterMan Dashboard"),
            dcc.Graph(px.scatter(precipitation, x="time", y="pr")),
        ],
    )

    return dash_app.server
