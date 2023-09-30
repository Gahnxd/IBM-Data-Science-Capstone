import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import html, dcc, Output, Input

spacex_df = pd.read_csv(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
)
max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 40},
        ),
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        dcc.Dropdown(
            id="site-dropdown",
            options=[{"label": "All Sites", "value": "ALL"}]
            + [
                {"label": site, "value": site}
                for site in spacex_df["Launch Site"].unique()
            ],
            value="ALL",
            placeholder="Select a Launch Site",
            searchable=True,
        ),
        html.Br(),
        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id="success-pie-chart")),
        html.Br(),
        html.P("Payload range (Kg):"),
        # TASK 3: Add a slider to select payload range
        dcc.RangeSlider(
            id="payload-slider",
            min=0,
            max=10000,
            step=1000,
            value=[min_payload, max_payload],
        ),
        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(dcc.Graph(id="success-payload-scatter-chart")),
    ]
)


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    Input(component_id="site-dropdown", component_property="value"),
)
def get_pie_chart(site):
    if site == "ALL":
        filtered_df = spacex_df.groupby("Launch Site").sum().reset_index()
        fig = px.pie(
            filtered_df,
            values="class",
            names="Launch Site",
            title="Total Success Launches By Site",
        )
        return fig
    else:
        filtered_df = (
            spacex_df[spacex_df["Launch Site"] == site]
            .groupby("class")
            .count()
            .reset_index()
        )
        fig = px.pie(
            filtered_df,
            values="Flight Number",
            names="class",
            title="Total Success Launches for Site " + site,
        )
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id="success-payload-scatter-chart", component_property="figure"),
    [
        Input(component_id="site-dropdown", component_property="value"),
        Input(component_id="payload-slider", component_property="value"),
    ],
)
def get_payload_scatter(site, payload):
    if site == "ALL":
        fig = px.scatter(
            spacex_df,
            x="Payload Mass (kg)",
            y="class",
            range_x=[payload[0], payload[1]],
            color="Booster Version Category",
            title="Correlation between Payload and Success for All Sites",
        )
        return fig
    else:
        filtered_df = spacex_df[spacex_df["Launch Site"] == site]
        fig = px.scatter(
            filtered_df,
            x="Payload Mass (kg)",
            y="class",
            range_x=[payload[0], payload[1]],
            color="Booster Version Category",
            title="Correlation between Payload and Success for Site " + site,
        )
        return fig


# Run the app
if __name__ == "__main__":
    app.run_server()
