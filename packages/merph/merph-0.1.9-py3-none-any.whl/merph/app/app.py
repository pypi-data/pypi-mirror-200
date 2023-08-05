import os
from faulthandler import disable
from math import floor
from turtle import color

import dash
import dash_bootstrap_components as dbc
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import callback_context  # type: ignore
from dash import dcc  # import dash_core_components as dcc
from dash import html  # import dash_html_components as html
from dash.dependencies import Input, Output, State
from numpy import abs, log10
from pandas import Categorical, DataFrame
from pandas.api.types import is_datetime64_any_dtype, is_numeric_dtype
from scipy.stats import truncnorm, uniform

from ..data import IVESPA, Aubry, Mastin, Sparks
from ..utilities.number_tools import (
    float_string,
    lin_levels,
    lin_steps,
    log_levels,
    log_steps,
    nice_round_down,
    nice_round_up,
    sci_string,
)
from ..utilities.string_tools import string_html, units_html


def build_app(local=True):
    app = dash.Dash(
        __name__,
        assets_url_path="merph/app/assets",
        external_stylesheets=[
            dbc.themes.BOOTSTRAP,
            dbc.icons.FONT_AWESOME,
        ],
        suppress_callback_exceptions=True,
        requests_pathname_prefix="/" if local else "/merph/",
    )

    available_datasets = {
        "Mastin": Mastin,
        "Sparks": Sparks,
        "Aubry": Aubry,
        "IVESPA": IVESPA,
    }

    ignored_columns = [
        "Name",
        "Alternative Volcano Names",
        "GVP volcano number",
        "GVP eruption number",
        "Date",
        "Event Year",
        "Event Name",
        "IVESPA ID",
        "Local start time",
        "Start time",
        "Date of onset",
        "Date start",
        "Date and Time",
    ]

    dataset_name = "Mastin"

    explore_tab = html.Div(
        className="pane",
        children=[
            html.Div(
                className="flex-container",
                children=[
                    html.Div(
                        id="dataset_selector",
                        className="column column-one",
                        children=[
                            html.Div(
                                className="flex-input-column",
                                children=[
                                    html.Label("Dataset:", className="Dropdown-label"),
                                    dcc.Dropdown(
                                        id="dataset-dropdown",
                                        options=[
                                            {"label": i, "value": i}
                                            for i in available_datasets.keys()
                                        ],
                                        value="Mastin",
                                        clearable=False,
                                        placeholder="Select a dataset",
                                        # optionHeight=20,
                                    ),
                                ],
                            )
                        ],
                    ),
                    html.Div(
                        id="color_selector",
                        className="column column-two",
                        children=[
                            html.Div(
                                className="flex-input-column",
                                children=[
                                    html.Label(
                                        "Marker colour:", className="Dropdown-label"
                                    ),
                                    dcc.Dropdown(
                                        id="color-column",
                                        placeholder="Select attribute for marker colour",
                                        optionHeight=20,
                                    ),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        id="size_selector",
                        className="column column-three",
                        children=[
                            html.Div(
                                className="flex-input-column",
                                children=[
                                    html.Label(
                                        "Marker size:", className="Dropdown-label"
                                    ),
                                    dcc.Dropdown(
                                        id="size-column",
                                        placeholder="Select attribute for marker size",
                                        optionHeight=20,
                                    ),
                                ],
                            )
                        ],
                    ),
                ],
            )
        ],
    )

    obs_discrete_div = html.Div(
        className="flex-container",
        style={"float": "inline-start"},
        children=[
            html.Div(
                className="column column-one",
                children=[
                    html.Label(children=["Observations: "], className="fl"),
                    dcc.Input(
                        id="pred_obs_discrete_vals",
                        name="pred_obs_discrete_vals",
                        className="textbox",
                        type="text",
                        placeholder="observations",
                        pattern="^[?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?,\s]+",
                        style={
                            "width": "120px",
                            "height": "25px",
                            "border": "1px solid rgb(170, 156, 143)",
                            "background-color": "rgb(255, 255, 255)",
                            "text-align": "center",
                        },
                    ),
                ],
            ),
        ],
    )

    obs_interval_div = html.Div(
        className="flex-container",
        style={"float": "inline-start"},
        children=[
            html.Div(
                className="column column-one",
                children=[
                    html.Label(children=["Lower bound:"], className="fl"),
                    dcc.Input(
                        id="pred_obs_lower",
                        name="pred_obs_lower",
                        className="textbox",
                        type="number",
                        placeholder="lower",
                        style={
                            "width": "60px",
                            "height": "25px",
                            "border": "1px solid rgb(170, 156, 143)",
                            "background-color": "rgb(255, 255, 255)",
                            "text-align": "center",
                        },
                    ),
                ],
            ),
            html.Div(
                className="column column-two",
                children=[
                    html.Label("Upper bound:", className="fl"),
                    dcc.Input(
                        id="pred_obs_upper",
                        name="pred_obs_upper",
                        className="textbox",
                        type="number",
                        placeholder="upper",
                        style={
                            "width": "60px",
                            "height": "25px",
                            "border": "1px solid rgb(170, 156, 143)",
                            "background-color": "rgb(255, 255, 255)",
                            "text-align": "center",
                        },
                    ),
                ],
            ),
        ],
    )

    regression_tab = html.Div(
        className="pane",
        children=[
            html.Div(
                className="flex-container",
                children=[
                    html.Div(
                        id="regression_selector",
                        className="column column-one",
                        children=[
                            html.Div(
                                className="flux-input-column",
                                children=[
                                    html.Label("Select observable variable:"),
                                    dcc.RadioItems(
                                        id="x-var",
                                        options=[
                                            {"label": "Column Height", "value": "H"},
                                            {
                                                "label": "Mass eruption rate",
                                                "value": "Q",
                                            },
                                        ],
                                        value="H",
                                        inputClassName="radioalign",
                                        labelClassName="radiolabel",
                                    ),
                                ],
                            )
                        ],
                    ),
                    html.Div(
                        id="regression_button",
                        className="column column-two",
                        children=[
                            html.Div(
                                className="row",
                                children=[
                                    html.Div(
                                        className="formfield",
                                        style={"width": "240px"},
                                        children=[
                                            html.Button(
                                                className="button",
                                                id="regression-submit",
                                                style={"width": "150px"},
                                                n_clicks=0,
                                                children=[
                                                    html.I(
                                                        className="fas fa-chart-line",
                                                        style={"margin-right": "10px"},
                                                    ),
                                                    html.Span(
                                                        "Perform Regression",
                                                        style={"font-size": "10pt"},
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                    html.Div(
                                        className="formfield",
                                        style={"width": "240px"},
                                        children=[
                                            html.Button(
                                                className="button",
                                                id="prediction-submit",
                                                style={"width": "150px"},
                                                n_clicks=0,
                                                children=[
                                                    html.I(
                                                        className="fas fa-dice",
                                                        style={"margin-right": "10px"},
                                                    ),
                                                    html.Span(
                                                        "Sample Posterior Predictive Distribution",
                                                        style={"font-size": "10pt"},
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                    html.Div(
                                        className="formfield",
                                        style={"width": "240px"},
                                        children=[
                                            html.Button(
                                                className="button",
                                                id="prediction-download-button",
                                                disabled="disabled",
                                                style={"width": "150px"},
                                                n_clicks=0,
                                                children=[
                                                    html.I(
                                                        className="fas fa-download",
                                                        style={"margin-right": "10px"},
                                                    ),
                                                    html.Span(
                                                        "Download Posterior Predictive Samples",
                                                        style={"font-size": "10pt"},
                                                    ),
                                                ],
                                            ),
                                            dcc.Download(id="prediction_download"),
                                        ],
                                    ),
                                    html.Div(
                                        className="formfield",
                                        style={"width": "240px"},
                                        children=[
                                            html.Label("Output format:"),
                                            dcc.Dropdown(
                                                id="download-format",
                                                options=[
                                                    {"label": "Excel", "value": "xlsx"},
                                                    {"label": "CSV", "value": "csv"},
                                                ],
                                                value="xlsx",
                                                clearable=False,
                                                multi=False,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        id="regression_prediction",
                        className="column column-three",
                        children=[
                            html.Span("Posterior prediction"),
                            html.Div(
                                className="formfield fflrg",
                                style={"width": "550px"},
                                children=[
                                    html.Label("Observations as:", className="fl"),
                                    dcc.RadioItems(
                                        id="pred_obs_type",
                                        options=[
                                            {
                                                "label": "Discrete values",
                                                "value": "discrete",
                                            },
                                            {
                                                "label": "Uncertain interval",
                                                "value": "interval",
                                            },
                                        ],
                                        value="discrete",
                                        inputClassName="radioalign",
                                        labelClassName="radiolabel",
                                        labelStyle={"display": "inline-block"},
                                    ),
                                ],
                            ),
                            html.Div(
                                className="formfield fflrg",
                                style={"width": "550px"},
                                children=[
                                    html.Span(
                                        id="pred_obs_span", children=["Observations"]
                                    ),
                                ],
                            ),
                            html.Div(
                                id="obs-input",
                                className="formfield fflrg",
                                style={"width": "550px"},
                                children=[],
                            ),
                            html.Div(
                                id="pred_interval_input",
                                className="formfield fflrg",
                                style={"width": "550px"},
                                children=[
                                    html.Div(
                                        className="column column-one",
                                        children=[
                                            html.Label(
                                                "Distribution between bounds:",
                                                className="fl",
                                            ),
                                            dcc.RadioItems(
                                                id="pred_obs_dist",
                                                options=[
                                                    {
                                                        "label": "Uniform",
                                                        "value": "unif",
                                                    },
                                                    {
                                                        "label": "Truncated Normal",
                                                        "value": "norm",
                                                    },
                                                ],
                                                value="unif",
                                                inputClassName="radioalign",
                                                labelClassName="radiolabel",
                                                labelStyle={"display": "inline-block"},
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                            html.Div(
                                id="norm-params",
                                className="formfield fflrg invisible",
                                style={"width": "550px"},
                                children=[
                                    html.Div(
                                        className="flex-container",
                                        style={"float": "inline-start"},
                                        children=[
                                            html.Div(
                                                className="column column-one",
                                                children=[
                                                    html.Label("Mean:", className="fl"),
                                                    dcc.Input(
                                                        id="pred_obs_norm_mean",
                                                        name="pred_obs_norm_mean",
                                                        className="textbox",
                                                        type="number",
                                                        placeholder="mean",
                                                        style={
                                                            "width": "60px",
                                                            "height": "25px",
                                                            "border": "1px solid rgb(170, 156, 143)",
                                                            "background-color": "rgb(255, 255, 255)",
                                                            "text-align": "center",
                                                        },
                                                    ),
                                                ],
                                            ),
                                            html.Div(
                                                className="column column-two",
                                                children=[
                                                    html.Label(
                                                        "Standard deviation:",
                                                        className="fl",
                                                    ),
                                                    dcc.Input(
                                                        id="pred_obs_norm_std",
                                                        name="pred_obs_norm_std",
                                                        className="textbox",
                                                        type="number",
                                                        placeholder="std. dev.",
                                                        style={
                                                            "width": "60px",
                                                            "height": "25px",
                                                            "border": "1px solid rgb(170, 156, 143)",
                                                            "background-color": "rgb(255, 255, 255)",
                                                            "text-align": "center",
                                                        },
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                            html.Div(
                                className="formfield fflrg",
                                style={"width": "550px"},
                                children=[
                                    html.Div(
                                        className="flex-container",
                                        children=[
                                            html.Div(
                                                className="column column-one",
                                                children=[
                                                    html.Label(
                                                        "Number of predictive samples:",
                                                        className="fl",
                                                    ),
                                                    dcc.Input(
                                                        id="pred_num_samples",
                                                        name="pred_num_samples",
                                                        className="textbox",
                                                        type="number",
                                                        placeholder="100",
                                                        value="100",
                                                        style={
                                                            "width": "60px",
                                                            "height": "25px",
                                                            "border": "1px solid rgb(170, 156, 143)",
                                                            "background-color": "rgb(255, 255, 255)",
                                                            "text-align": "center",
                                                        },
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            )
        ],
    )

    app.layout = html.Div(
        className="body",
        children=[
            dcc.Store(id="dataset", storage_type="session"),
            dcc.Store(id="color", storage_type="session"),
            dcc.Store(id="size", storage_type="session"),
            dcc.Store(id="pred_obs_type_store", storage_type="session"),
            dcc.Store(id="pred_obs_discrete_store", storage_type="session"),
            dcc.Store(id="pred_obs_dist_store", storage_type="session"),
            dcc.Store(id="pred_obs_lower_store", storage_type="session"),
            dcc.Store(id="pred_obs_upper_store", storage_type="session"),
            dcc.Store(id="pred_obs_norm_mean_store", storage_type="session"),
            dcc.Store(id="pred_obs_norm_std_store", storage_type="session"),
            dcc.Store(id="pred_num_samples_store", storage_type="session"),
            dcc.Store(id="pred_samples_store", storage_type="session"),
            html.Div(
                className="header",
                children=[
                    html.Img(
                        src=app.get_asset_url("uob_logo.png"),
                        style={"float": "left"},
                        alt="University of Bristol",
                        height=49,
                    ),
                    html.Div(
                        className="modelTitle",
                        children=[
                            html.Span("MERPH: Volcanic eruption Q\u2013H data analysis")
                        ],
                    ),
                ],
            ),
            html.Div(style={"clear": "both"}),
            html.Div(
                className="guipane",
                children=[
                    html.Div(
                        id="image-container",
                        className="imagepane",
                        children=[
                            html.Div(
                                className="imagehp", children=[dcc.Graph(id="QH-plot")]
                            ),
                        ],
                    ),
                    html.Div(style={"clear": "both", "margin-top": 10}),
                    html.Div(
                        dcc.Tabs(
                            id="outertabs",
                            className="tabs",
                            value="exploreTab",
                            children=[
                                dcc.Tab(
                                    label="Explore data",
                                    value="exploreTab",
                                    className="outertab",
                                    selected_className="outertab--selected",
                                    children=explore_tab,
                                ),
                                dcc.Tab(
                                    label="Bayesian regression",
                                    value="regressionTab",
                                    className="outertab",
                                    selected_className="outertab--selected",
                                    children=regression_tab,
                                ),
                            ],
                        )
                    ),
                    html.Div(style={"clear": "both"}),
                ],
            ),
            html.Div(
                id="footer",
                children=[
                    html.Div(
                        id="footertext",
                        children=[
                            "Copyright © University of Bristol 2022\u0020|\u0020",
                            html.A(
                                href="http://www.bristol.ac.uk/web/policies/terms-conditions.html",
                                target="_blank",
                                children=["Terms and conditions"],
                            ),
                            "\u0020|\u0020",
                            html.A(
                                href="http://www.bristol.ac.uk/web/policies/privacy-policy.html",
                                target="_blank",
                                children=["Privacy policy"],
                            ),
                        ],
                    )
                ],
            ),
        ],
    )

    @app.callback(
        Output("dataset", "data"),
        Input("dataset-dropdown", "value"),
    )
    def store_dataset(selected_dataset):
        return {"dataset": selected_dataset}  # type:ignore

    @app.callback(
        Output("color-column", "options"),
        Output("color-column", "value"),
        Output("color-column", "optionHeight"),
        Output("size-column", "options"),
        Output("size-column", "value"),
        Output("size-column", "optionHeight"),
        Input("dataset", "data"),
    )
    def set_dropdown_options(session_dataset):
        dataset_name = session_dataset["dataset"]
        available_columns = available_datasets[dataset_name].data_columns

        [
            available_columns.remove(ig)
            for ig in ignored_columns
            if ig in available_columns
        ]

        maxlabellen = max([len(c) for c in available_columns])
        option_height = 25 + 15 * (maxlabellen // 25)

        color_options = [{"label": i, "value": i} for i in available_columns]

        color_value = available_datasets[dataset_name].height_column

        numeric_columns = [
            i
            for i in available_columns
            if is_numeric_dtype(available_datasets[dataset_name].data.dtypes[i])
        ]
        if "Latitude" in numeric_columns:
            numeric_columns.remove("Latitude")
        if "Longitude" in numeric_columns:
            numeric_columns.remove("Longitude")
        size_options = [{"label": i, "value": i} for i in numeric_columns]

        size_value = available_datasets[dataset_name].height_column
        return (
            color_options,
            color_value,
            option_height,
            size_options,
            size_value,
            option_height,
        )
        # return {'options':color_options, 'value':color_value}, {'options':size_options, 'value':size_value}

    @app.callback(Output("color", "data"), Input("color-column", "value"))
    def set_color_column(color_value):
        return {"value": color_value}

    @app.callback(Output("size", "data"), Input("size-column", "value"))
    def set_size_column(size_value):
        return {"value": size_value}

    @app.callback(
        Output("norm-params", "className"),
        Input("pred_obs_dist", "value"),
        Input("pred_obs_type", "value"),
        prevent_initial_call=True,
    )
    def set_pred_obs_dist(obs_dist, obs_type):
        if obs_type == "discrete":
            className = "formfield fflrg invisible"
        elif obs_type == "interval":
            if obs_dist == "unif":
                className = "formfield fflrg invisible"
            elif obs_dist == "norm":
                className = "formfield fflrg"
        return className

    @app.callback(
        Output("pred_obs_discrete_vals", "value"),
        Input("x-var", "value"),
    )
    def clear_obs_discrete_vals(val):
        return ""

    @app.callback(
        Output("pred_obs_lower", "value"),
        Input("x-var", "value"),
    )
    def clear_obs_lower_vals(val):
        return ""

    @app.callback(
        Output("pred_obs_upper", "value"),
        Input("x-var", "value"),
    )
    def clear_obs_upper_vals(val):
        return ""

    @app.callback(
        Output("pred_obs_norm_mean", "value"),
        Input("x-var", "value"),
    )
    def clear_obs_mean_vals(val):
        return ""

    @app.callback(
        Output("pred_obs_norm_std", "value"),
        Input("x-var", "value"),
    )
    def clear_obs_std_vals(val):
        return ""

    @app.callback(
        Output("pred_obs_type_store", "data"),
        Input("pred_obs_type", "value"),
    )
    def set_pred_obs_dist(obs_type):
        return {"value": obs_type}

    @app.callback(
        Output("pred_obs_discrete_store", "data"),
        Input("pred_obs_discrete_vals", "value"),
        prevent_initial_call=True,
    )
    def set_pred_obs_dist(obs_value):
        return {"value": obs_value}

    @app.callback(
        Output("pred_obs_dist_store", "data"), Input("pred_obs_dist", "value")
    )
    def set_pred_obs_dist(obs_dist):
        return {"value": obs_dist}

    @app.callback(
        Output("pred_obs_lower_store", "data"), Input("pred_obs_lower", "value")
    )
    def set_pred_obs_dist(obs_lower):
        return {"value": obs_lower}

    @app.callback(
        Output("pred_obs_upper_store", "data"), Input("pred_obs_upper", "value")
    )
    def set_pred_obs_dist(obs_upper):
        return {"value": obs_upper}

    @app.callback(
        Output("pred_obs_norm_mean_store", "data"), Input("pred_obs_norm_mean", "value")
    )
    def set_pred_obs_dist(norm_mean):
        return {"value": norm_mean}

    @app.callback(
        Output("pred_obs_norm_std_store", "data"), Input("pred_obs_norm_std", "value")
    )
    def set_pred_obs_dist(norm_std):
        return {"value": norm_std}

    @app.callback(
        Output("pred_num_samples_store", "data"), Input("pred_num_samples", "value")
    )
    def set_pred_obs_dist(num_samples):
        return {"value": num_samples}

    @app.callback(Output("pred_obs_span", "children"), Input("x-var", "value"))
    def set_pred_obs_lower_label(xvar):
        if xvar == "H":
            return "Observed plume height (km):"
        elif xvar == "Q":
            return "Observed mass eruption rate (kg/s):"

    @app.callback(
        Output("pred_interval_input", "className"), Input("pred_obs_type", "value")
    )
    def set_pred_interval_input(obs_type):
        if obs_type == "discrete":
            className = "formfield fflrg invisible"
        elif obs_type == "interval":
            className = "formfield fflrg"
        return className

    @app.callback(
        Output("prediction-download-button", "disabled"),
        Output("download-format", "disabled"),
        Input("prediction-submit", "n_clicks"),
    )
    def activate_download_button(n_clicks):
        changed_id = [p["prop_id"] for p in callback_context.triggered][0]

        if changed_id == "prediction-submit.n_clicks":
            return False, False
        else:
            return True, True

    @app.callback(
        Output("prediction_download", "data"),
        Input("prediction-download-button", "n_clicks"),
        Input("pred_samples_store", "data"),
        Input("download-format", "value"),
    )
    def download_samples(n_clicks, prediction_samples, fmt):

        changed_id = [p["prop_id"] for p in callback_context.triggered][0]
        if "prediction-download-button" in changed_id:
            df = DataFrame(prediction_samples)

            if fmt == "xlsx":
                return dcc.send_data_frame(df.to_excel, "samples.xlsx")
            elif fmt == "csv":
                return dcc.send_data_frame(df.to_csv, "samples.csv")

    @app.callback(
        Output("prediction-submit", "disabled"),
        Input("pred_obs_type_store", "data"),
        Input("pred_obs_discrete_store", "data"),
        Input("pred_obs_dist_store", "data"),
        Input("pred_obs_lower_store", "data"),
        Input("pred_obs_upper_store", "data"),
        Input("pred_obs_norm_mean_store", "data"),
        Input("pred_obs_norm_std_store", "data"),
        Input("pred_num_samples_store", "data"),
    )
    def activate_regression_button(
        pred_obs_type,
        pred_obs_discrete,
        pred_obs_dist,
        pred_obs_lower,
        pred_obs_upper,
        pred_obs_norm_mean,
        pred_obs_norm_std,
        pred_num_samples,
    ):

        if int(pred_num_samples["value"]) < 1:
            disabled = True
            return disabled

        if pred_obs_type["value"] == "discrete":

            if pred_obs_discrete["value"] == "":
                disabled = True
                return disabled

        elif pred_obs_type["value"] == "interval":

            if pred_obs_lower["value"] == "":
                disabled = True
                return disabled

            if pred_obs_upper["value"] == "":
                disabled = True
                return disabled

            if pred_obs_dist["value"] == "norm":
                if pred_obs_norm_mean["value"] == "":
                    disabled = True
                    return disabled
                if pred_obs_norm_std["value"] == "":
                    disabled = True
                    return disabled

        disabled = False
        return disabled

    @app.callback(Output("obs-input", "children"), Input("pred_obs_type", "value"))
    def set_obs_input_form(obs_type):

        if obs_type == "discrete":
            return obs_discrete_div
        elif obs_type == "interval":
            return obs_interval_div

    @app.callback(
        Output("QH-plot", "figure"),
        Input("dataset", "data"),
        Input("color", "data"),
        Input("size", "data"),
    )
    def update_explore_plot(
        session_dataset, color_data, size_data
    ):  # , color_type, size_type):

        dataset_name = session_dataset["dataset"]
        color_column = color_data["value"]
        size_column = size_data["value"]

        data = available_datasets[dataset_name].data
        data_units = available_datasets[dataset_name].data_units
        H_column = available_datasets[dataset_name].height_column
        Q_column = available_datasets[dataset_name].mer_column

        available_columns = available_datasets[dataset_name].data_columns
        column_units = available_datasets[dataset_name].data_units

        numeric_columns = [
            i for i in available_columns if is_numeric_dtype(data.dtypes[i])
        ]
        categorical_columns = [
            i
            for i in available_columns
            if not is_numeric_dtype(data.dtypes[i]) or "Flag" in i
        ]

        if "VEI" in available_columns:
            categorical_columns.append("VEI")
        if "Latitude" in numeric_columns:
            numeric_columns.remove("Latitude")
        if "Longitude" in numeric_columns:
            numeric_columns.remove("Longitude")
        log_columns = []
        for col in numeric_columns:
            if data[col].min() > 0 and data[col].max() >= 50 * data[col].min():
                log_columns.append(col)
                data["log_" + col] = np.log10(data[col])
            # elif data[col].min() == 0 and data[col].max() > 100:
            #     log_columns.append(col)
            #     data["log_" + col] = np.log10(data[col])

        if size_column is not None:

            sizes = abs(data[size_column].values)

            size_min = np.nanmin(sizes)
            size_max = np.nanmax(sizes)

            if size_column in log_columns:
                if size_min > 0:
                    sizes = log10(sizes) - log10(size_min) + 1
                else:
                    sizes = log10(sizes + 1)

            if np.nanmax(sizes) == np.nanmin(sizes):
                sizes[~np.isnan(sizes)] = 2
            else:
                sizes = (sizes - np.nanmin(sizes)) / (
                    np.nanmax(sizes) - np.nanmin(sizes)
                ) * 4 + 1

            sizes[np.isnan(sizes)] = 0.5  # 0.5*np.nanmin(sizes))
        else:
            sizes = None

        color_discrete_sequence = px.colors.qualitative.Dark24
        color_discrete_map = None
        color_category_orders = None

        if color_column is None:
            colors = None
            color_continuous_scale = None
            tickvals = []
            ticktext = []
            range_color = None

        elif color_column in categorical_columns:

            if color_column == "Climate zone":
                data[color_column] = Categorical(
                    data[color_column], ["Tropical", "Subtropics", "Temperate", "Cold"]
                )
                color_discrete_map = {
                    "Tropical": "IndianRed",
                    "Subtropics": "Peru",
                    "Temperate": "ForestGreen",
                    "Cold": "CadetBlue",
                }
                color_category_orders = {
                    color_column: ["Tropical", "Subtropics", "Temperate", "Cold"]
                }
                colors = data[color_column].values
                color_continuous_scale = None
                tickvals = []
                ticktext = []
                range_color = None

            elif color_column == "Eruption style":
                data[color_column] = Categorical(
                    data[color_column],
                    ["magmatic", "phreatomagmatic", "phreatic", "Unknown"],
                )
                color_discrete_map = {
                    "Unknown": "lightslategray",
                    "magmatic": "darkred",
                    "phreatomagmatic": "darkmagenta",
                    "phreatic": "teal",
                }
                color_category_orders = {
                    color_column: ["Unknown", "magmatic", "phreatomagmatic", "phreatic"]
                }
                colors = data[color_column].values
                color_continuous_scale = None
                tickvals = []
                ticktext = []
                range_color = None

            elif color_column in ["Plume style", "Plume morphology"]:
                data[color_column] = Categorical(
                    data[color_column], ["Weak", "Distorted", "Strong", "Unknown"]
                )
                color_discrete_map = {
                    "Unknown": "lightslategray",
                    "Weak": "darkcyan",
                    "Distorted": "darkmagenta",
                    "Strong": "crimson",
                }
                color_category_orders = {
                    color_column: ["Unknown", "Weak", "Distorted", "Strong"]
                }
                colors = data[color_column].values
                color_continuous_scale = None
                tickvals = []
                ticktext = []
                range_color = None

            elif "Flag" in color_column:
                data[color_column] = data[color_column].astype(str)
                data[color_column] = Categorical(
                    data[color_column], ["0", "1", "2", "-1"]
                )
                data[color_column] = data[color_column].cat.rename_categories(
                    {"0": "Flag 0", "1": "Flag 1", "2": "Flag 2", "-1": "n/a"}
                )
                color_discrete_map = {
                    "Flag 2": "firebrick",
                    "Flag 1": "lightcoral",
                    "Flag 0": "steelblue",
                    "n/a": "lightslategray",
                }
                color_category_orders = {
                    color_column: ["Flag 2", "Flag 1", "Flag 0", "n/a"]
                }
                colors = data[color_column].values
                color_continuous_scale = None
                tickvals = []
                ticktext = []
                range_color = None

            else:
                if is_numeric_dtype(data[color_column]):
                    col_list = px.colors.sequential.Sunsetdark
                    cmax = data[color_column].max()
                    cmin = data[color_column].min()
                    N = int(np.ceil(cmax - cmin + 1))
                    cstep = (cmax - cmin) / N
                    color_continuous_scale = [
                        x
                        for i in range(N)
                        for x in (
                            (i / N, interp_rgb(col_list, i / N)),
                            ((i + 1) / N, interp_rgb(col_list, i / N)),
                        )
                    ]

                    colors = color_column
                    tickvals = [(cmin + cstep / 2) + i * cstep for i in range(N)]
                    ticktext = [cmin + i for i in range(N)]
                    if cmin == 0:
                        color_continuous_scale[0] = (0.0, "rgb(200,200,200)")
                        color_continuous_scale[1] = (1 / N, "rgb(200,200,200)")
                        ticktext[0] = "Unknown"
                    range_color = [cmin, cmax]

                else:
                    colors = data[color_column].values
                    color_continuous_scale = None
                    tickvals = []
                    ticktext = []
                    range_color = None

        elif color_column == "Latitude":
            # color_continuous_scale = px.colors.diverging.Tealrose
            color_continuous_scale = ["Azure", "Teal", "IndianRed", "SeaGreen", "Azure"]
            colors = data[color_column].values
            tickvals = np.linspace(-90, 90, 5)
            ticktext = np.linspace(-90, 90, 5)
            range_color = [-90, 90]

        elif color_column == "Longitude":
            color_continuous_scale = px.colors.cyclical.Twilight
            colors = data[color_column].values
            tickvals = np.linspace(-180, 180, 5)
            ticktext = np.linspace(-180, 180, 5)
            range_color = [-180, 180]

        elif color_column in log_columns:
            color_continuous_scale = px.colors.sequential.Sunsetdark
            colors = data["log_" + color_column].values
            cmin = nice_round_down(np.nanmin(data[color_column].values))
            cmax = nice_round_up(np.nanmax(data[color_column].values))
            if cmin == cmax:
                cmin = 0.1 * cmin
                cmax = 10 * cmax
            logcmin = np.log10(cmin)
            logcmax = np.log10(cmax)
            range_color = [logcmin, logcmax]
            ticklocs = log_steps(cmin, cmax)
            if cmax > 4 or cmin < -4:
                ticktext = [sci_string(x) for x in ticklocs]
            else:
                ticktext = ticklocs
            tickvals = np.log10(ticklocs)

        else:
            color_continuous_scale = px.colors.sequential.Sunsetdark
            colors = abs(data[color_column].values)
            if np.nanmin(colors) == np.nanmax(colors):
                cmin = nice_round_down(0.5 * np.nanmin(colors))
                cmax = nice_round_up(1.5 * np.nanmax(colors))
            else:
                cmin = nice_round_down(np.nanmin(colors))
                cmax = nice_round_up(np.nanmax(colors))
            range_color = [cmin, cmax]

            step = 10 ** floor(np.log10(cmax - cmin))

            tickvals = lin_steps(cmin, cmax, step=step)
            ticktext = tickvals

        if color_column in categorical_columns:
            data["color_value"] = data[color_column].values
        else:
            if color_column in log_columns:
                data["color_value"] = data[color_column].apply(
                    lambda x: sci_string(x, precision=2, start_sci=2)
                )
            else:
                data["color_value"] = data[color_column].apply(
                    lambda x: float_string(x, precision=2)
                )
            data["color_value"] = data["color_value"].apply(
                lambda x: add_units(x, data_units[color_column])
            )

        if size_column in log_columns:
            data["size_value"] = data[size_column].apply(
                lambda x: sci_string(x, precision=2, start_sci=2)
            )
        else:
            data["size_value"] = data[size_column].apply(
                lambda x: float_string(x, precision=2)
            )
        data["symbol"] = data["size_value"].apply(
            lambda x: "x" if x == "No data" else "circle"
        )
        data["size_value"] = data["size_value"].apply(
            lambda x: add_units(x, data_units[size_column])
        )

        data["Q_value"] = data[Q_column].apply(
            lambda x: sci_string(x, precision=2, start_sci=2)
        )
        data["Q_value"] = data["Q_value"].apply(
            lambda x: add_units(x, data_units[Q_column])
        )
        data["H_value"] = data[H_column].apply(lambda x: float_string(x, precision=2))
        data["H_value"] = data["H_value"].apply(
            lambda x: add_units(x, data_units[H_column])
        )

        if "Name" in available_columns:
            hovertitle = "Name"
        else:
            hovertitle = "Volcano"
        fig = px.scatter(
            data,
            x=Q_column,
            y=H_column,
            labels={
                Q_column: f"{Q_column} ({data_units[Q_column]})",
                H_column: f"{H_column} ({data_units[H_column]})",
            },
            log_x=True,
            opacity=0.5,
            color=colors,
            size=sizes,
            category_orders=color_category_orders,
            color_discrete_sequence=color_discrete_sequence,
            color_discrete_map=color_discrete_map,
            color_continuous_scale=color_continuous_scale,
            range_color=range_color,
            symbol="symbol",
            symbol_map="identity",
            hover_name="Name",  # if 'Name' in available_columns else 'Volcano',
            hover_data=["Volcano", "Q_value", "H_value", "color_value", "size_value"],
        )

        fig.layout.coloraxis.colorbar.title = color_column
        hvtmp = "<b>%{hovertext}</b><br><br>"
        hvtmp += f"{Q_column}" + " = %{customdata[1]}<br>"
        hvtmp += f"{H_column}" + " = %{customdata[2]}<br>"

        if (
            size_column is not None
            and size_column != Q_column
            and size_column != H_column
        ):

            hvtmp += size_column + " = %{customdata[4]} " + "<br>"
        if (
            color_column is not None
            and color_column != size_column
            and color_column != Q_column
            and color_column != H_column
        ):
            hvtmp += color_column + ": %{customdata[3]}"
            # if color_column in categorical_columns:
            #     hvtmp += color_column+': %{customdata[1]}'
            # else:
            #     if color_column in log_columns:
            #         hvtmp += color_column+' = %{customdata[1]:.2e}'
            #     else:
            #         hvtmp += color_column+' = %{customdata[1]:.2f}'
        hvtmp += "<extra></extra>"
        fig.update_traces(hovertemplate=hvtmp)

        if color_column in categorical_columns:
            if data[color_column].dtype == np.int64:
                fig.update_layout(
                    coloraxis_colorbar=dict(
                        title=color_column,
                        tickmode="array",
                        tickvals=tickvals,
                        ticktext=ticktext,
                    )
                )
            else:
                fig.update_layout(
                    legend=dict(
                        title=color_column,
                        itemwidth=30,
                        itemclick="toggleothers",
                        itemdoubleclick="toggle",
                    )
                )
        else:
            fig.update_layout(
                coloraxis_colorbar=dict(
                    title=string_html(
                        add_units(color_column, data_units[color_column], bracket=True)
                    ),
                    tickmode="array",
                    tickvals=tickvals,
                    ticktext=ticktext,
                )
            )
        # fig.update_coloraxes(dict(
        #     colorbar_title = dict(
        #         text=color_column,
        #     ),
        #     colorbar_tickmode = 'array',
        #     colorbar_tickvals = tickvals,
        #     colorbar_ticktext = ticktext,
        # ))

        fig.update_layout(
            plot_bgcolor="#f8f6f4",
            paper_bgcolor="#f8f6f4",
            height=500,
            margin={"l": 20, "r": 20, "t": 40, "b": 20},
        )

        fig.update_xaxes(
            showgrid=True,
            gridcolor="LightGrey",
            zerolinecolor="DarkGrey",
            exponentformat="power",
        )
        fig.update_yaxes(
            showgrid=True,
            gridcolor="LightGrey",
            zerolinecolor="DarkGrey",
            exponentformat="power",
        )

        # fig.update_layout(
        #     font_family="Rockwell",
        #     colorbar={'title': color_column}
        # )

        return fig

    def make_regression_fig(xvar, dataset):
        if xvar == "Q":
            yvar = "H"
        elif xvar == "H":
            yvar = "Q"

        dataset_name = dataset["dataset"]
        dataset = available_datasets[dataset_name]
        H_column = available_datasets[dataset_name].height_column
        Q_column = available_datasets[dataset_name].mer_column

        dataset.set_vars(xvar=xvar, yvar=yvar)

        data = dataset.data.copy()
        data.dropna(
            axis=0,
            how="any",
            subset=[H_column, Q_column],
            inplace=True,
        )

        data["mle_residuals"] = dataset.residual

        mle = dataset.mle_trace()

        data_fig = px.scatter(
            data,
            x=Q_column,
            y=H_column,
            labels={
                "MER": f"{Q_column} ({dataset.data_units[Q_column]})",
                "Plume height": f"{H_column} ({dataset.data_units[H_column]})",
            },
            log_x=True,
            opacity=0.75,
            hover_name="Name",  # if 'Name' in available_columns else 'Volcano',
            hover_data=["Volcano", "mle_residuals"],
        )
        hvtmp = (
            "<b>%{hovertext}</b><br><br>"
            + f"{Q_column} ({dataset.data_units[Q_column]})"
            + " = %{x}"
        )
        hvtmp += "<br>" + f"{H_column} ({dataset.data_units[H_column]})" + " = %{y}<br>"
        hvtmp += "Linear regression residual = %{customdata[1]:.3f}<br><extra></extra>"
        data_fig.update_traces(hovertemplate=hvtmp)
        data_fig.update_traces(
            marker=dict(
                size=15,
                color="lightslategrey",
                line=dict(
                    color="slategrey",
                    width=2,
                ),
            ),
        )
        # data_fig.update_traces(marker={
        #     'size': 15,
        #     'color':'lightslategrey',
        #     line=dict(
        #         color='#042945',
        #         width=1
        #     )
        #     }
        # )

        mle_fig = go.Figure(
            go.Scatter(
                x=mle[Q_column].values,
                y=mle[H_column].values,
                name="Regression<br>curve",
            )
        )
        mle_fig.update_xaxes(type="log")
        hvtmp = "<b>Regression curve</b><br><br>Mass eruption rate (kg/s) = %{x:.4}<br>Column height (km a.v.l.) = %{y:.2f}<br><extra></extra>"
        mle_fig.update_traces(hovertemplate=hvtmp)
        mle_fig.update_traces(line_color="darkred")
        mle_fig.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.5, xanchor="right", x=1)
        )

        bayes_posterior = dataset.posterior_data()
        print(np.amin(bayes_posterior["logp"]), np.amax(bayes_posterior["logp"]))

        sci_string_vec = np.vectorize(sci_string, excluded=["precision", "start_sci"])
        bayes_posterior["p_str"] = sci_string_vec(
            bayes_posterior["p"], precision=2, start_sci=2
        )

        tickvals = np.arange(-6, int(np.ceil(np.nanmax(bayes_posterior["logp"]))) + 1)
        ticktext = ["10<sup>" + str(x) + "</sup>" for x in tickvals]

        # color_start = -5 if xvar == "H" else -7
        # color_end = 2 if xvar == "H" else 2
        # clip_low = np.where(bayes_posterior["logp"] < color_start)
        # bayes_posterior["logp"][clip_low] = np.NaN

        # colorscale = px.colors.sequential.PuBu
        colorscale = px.colors.sequential.Purpor
        # colorscale[0] = colorscale[0].replace("rgb", "rgba")
        # colorscale[0] = colorscale[0].replace(")", ",0)")
        colorscale[0] = "rgba(255,247,251,0)"

        print(colorscale)

        cntr_fig = go.Figure(
            data=go.Contour(
                z=bayes_posterior["logp"],
                x=bayes_posterior["Q"],  # horizontal axis
                y=bayes_posterior["H"],  # vertical axis
                customdata=bayes_posterior["p_str"],
                # colorscale="BuPu",
                colorscale=colorscale,
                contours=dict(
                    start=-6,
                    end=0,
                    size=1,
                ),
                colorbar=dict(
                    title="Posterior<br>probability<br>density",
                    tickmode="array",
                    tickvals=tickvals,
                    ticktext=ticktext,
                    len=0.6,
                    ypad=0,
                    yanchor="top",
                ),
                hovertemplate="<b>Posterior probability</b><br><br>Mass eruption rate (kg/s) = %{x:.4}<br>Column height (km a.v.l.) = %{y:.2f}<br>"
                + "Posterior probability density = %{customdata}<br><extra></extra>",
            )
        )

        fig = go.Figure(data=cntr_fig.data + mle_fig.data + data_fig.data)

        fig.update_layout(
            plot_bgcolor="#f8f6f4",
            paper_bgcolor="#f8f6f4",
            height=500,
            margin={"l": 20, "r": 20, "t": 40, "b": 20},
            hoverdistance=1,
        )

        fig.update_xaxes(
            showgrid=True,
            gridcolor="LightGrey",
            zerolinecolor="DarkGrey",
            exponentformat="power",
            type="log",
            range=data_fig.full_figure_for_development().layout.xaxis.range,
            dtick=1,
            title="Mass eruption rate (kg/s)",
        )
        fig.update_yaxes(
            showgrid=True,
            gridcolor="LightGrey",
            zerolinecolor="DarkGrey",
            exponentformat="power",
            range=data_fig.full_figure_for_development().layout.yaxis.range,
            title="Column height (km a.v.l.)",
        )
        return fig

    def get_discrete_predictions(dataset, xvar, xvals, Nsamples):

        if xvar == "Q":
            yvar = "H"
        elif xvar == "H":
            yvar = "Q"

        dataset_name = dataset["dataset"]
        dataset = available_datasets[dataset_name]
        H_column = available_datasets[dataset_name].height_column
        Q_column = available_datasets[dataset_name].mer_column

        dataset.set_vars(xvar=xvar, yvar=yvar)

        xvals = xvals.split(",")
        xvals = [float(x) for x in xvals]

        dataset.set_obs(xvals, logscale=False)

        ypred = dataset.posterior_simulate(
            Nsamples, plot=False, split_x=True, as_dataframe=True
        )

        return ypred

    def get_interval_predictions(
        dataset, xvar, dist, lower, upper, mean, std, Nsamples
    ):

        if xvar == "Q":
            yvar = "H"
        elif xvar == "H":
            yvar = "Q"

        dataset_name = dataset["dataset"]
        dataset = available_datasets[dataset_name]
        H_column = available_datasets[dataset_name].height_column
        Q_column = available_datasets[dataset_name].mer_column

        dataset.set_vars(xvar=xvar, yvar=yvar)

        if dist == "unif":
            xvals = uniform(loc=lower, scale=upper - lower).rvs(Nsamples)
        elif dist == "norm":
            a = (lower - mean) / std
            b = (upper - mean) / std
            xvals = truncnorm(a, b, loc=mean, scale=std).rvs(Nsamples)

        dataset.set_obs(xvals, logscale=False)

        ypred = dataset.posterior_simulate(
            1, plot=False, split_x=False, as_dataframe=True
        )

        return ypred

    def make_discrete_prediction_plot(df, xvar):

        df["Q_label"] = df["Q"].apply(lambda x: sci_string(x, precision=2, start_sci=2))
        df["H_label"] = df["H"].apply(lambda x: sci_string(x, precision=2, start_sci=2))

        xvals = df[xvar].unique()

        pred_fig = go.Figure()

        for j, x in enumerate(xvals):
            marker_fill_color = px.colors.sequential.Sunsetdark[j]
            marker_line_color = shade_rgb_color(marker_fill_color, 0.5)
            pred_fig.add_trace(
                go.Scattergl(
                    x=df.loc[df[xvar] == x, "Q"],
                    y=df.loc[df[xvar] == x, "H"],
                    mode="markers",
                    marker=dict(
                        size=15,
                        color=marker_fill_color,
                        line=dict(color=marker_line_color, width=1),
                    ),
                    name=xvar + " = {:.2f}".format(x),
                    opacity=0.25,
                    customdata=np.stack(
                        (
                            df.loc[df[xvar] == x, "Q_label"],
                            df.loc[df[xvar] == x, "H_label"],
                        ),
                        axis=-1,
                    ),
                    hovertemplate=(
                        "<b>Posterior prediction</b><br>Mass eruption rate = %{customdata[0]} kg/s | Column height = %{customdata[1]} km a.v.l.<br><extra></extra>"
                        if xvar == "H"
                        else "<b>Posterior prediction</b><br>Column height = %{customdata[1]} km a.v.l. | Mass eruption rate = %{customdata[0]} kg/s <br><extra></extra>"
                    ),
                )
            )

        pred_fig.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=0, xanchor="right", x=1),
        )

        pred_fig.update_layout(legend_title_text="Posterior<br>prediction")

        return pred_fig

    def make_interval_prediction_plot(df, xvar):

        df["Q_label"] = df["Q"].apply(lambda x: sci_string(x, precision=2, start_sci=2))
        df["H_label"] = df["H"].apply(lambda x: sci_string(x, precision=2, start_sci=2))

        pred_fig = go.Figure()

        pred_fig.add_trace(
            go.Scattergl(
                x=df["Q"],
                y=df["H"],
                mode="markers",
                marker=dict(
                    size=10, color="#246290", line=dict(color="#042945", width=1)
                ),
                name="Posterior<br>prediction",
                opacity=0.4,
                customdata=np.stack((df["Q_label"], df["H_label"]), axis=-1),
                hovertemplate=(
                    "<b>Posterior prediction</b><br>Mass eruption rate = %{customdata[0]} kg/s | Column height = %{customdata[1]} km a.v.l.<br><extra></extra>"
                    if xvar == "H"
                    else "<b>Posterior prediction</b><br>Column height = %{customdata[1]} km a.v.l. | Mass eruption rate = %{customdata[0]} kg/s <br><extra></extra>"
                ),
            )
        )

        pred_fig.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=0, xanchor="right", x=1),
        )

        return pred_fig

    @app.callback(
        Output("image-container", "children"),
        Output("pred_samples_store", "data"),
        Input("regression-submit", "n_clicks"),
        Input("prediction-submit", "n_clicks"),
        Input("dataset", "data"),
        State("x-var", "value"),
        Input("pred_obs_type_store", "data"),
        Input("pred_obs_discrete_store", "data"),
        Input("pred_obs_dist_store", "data"),
        Input("pred_obs_lower_store", "data"),
        Input("pred_obs_upper_store", "data"),
        Input("pred_obs_norm_mean_store", "data"),
        Input("pred_obs_norm_std_store", "data"),
        Input("pred_num_samples_store", "data"),
        Input("pred_samples_store", "data"),
        State("image-container", "children"),
        prevent_initial_call=True,
    )
    def update_regression_plot(
        regression_submit_clicks,
        prediction_submit_clicks,
        dataset,
        xvar,
        pred_obs_type,
        pred_obs_discrete,
        pred_obs_dist,
        pred_obs_lower,
        pred_obs_upper,
        pred_obs_norm_mean,
        pred_obs_norm_std,
        pred_num_samples,
        prediction_samples,
        images,
    ):

        changed_id = [p["prop_id"] for p in callback_context.triggered][0]

        if changed_id not in [
            "regression-submit.n_clicks",
            "prediction-submit.n_clicks",
        ]:
            return images, prediction_samples

        if "regression-submit" in changed_id:
            images = [images[0]]

            fig = make_regression_fig(xvar, dataset)

            images.append(
                html.Div(
                    id="regression-plot",
                    className="imagehp",
                    children=[dcc.Graph(id="QH-regression-plot", figure=fig)],
                )
            )

            return images, prediction_samples

        if "prediction-submit" in changed_id:
            images = [images[0]]

            reg_fig = make_regression_fig(xvar, dataset)

            if pred_obs_type["value"] == "discrete":
                ypred = get_discrete_predictions(
                    dataset,
                    xvar,
                    pred_obs_discrete["value"],
                    int(pred_num_samples["value"]),
                )

                pred_fig = make_discrete_prediction_plot(ypred, xvar)

            if pred_obs_type["value"] == "interval":

                ypred = get_interval_predictions(
                    dataset,
                    xvar,
                    pred_obs_dist["value"],
                    pred_obs_lower["value"],
                    pred_obs_upper["value"],
                    pred_obs_norm_mean["value"],
                    pred_obs_norm_std["value"],
                    int(pred_num_samples["value"]),
                )

                pred_fig = make_interval_prediction_plot(ypred, xvar)

            fig = go.Figure(data=reg_fig.data + pred_fig.data)

            fig.update_layout(
                plot_bgcolor="#f8f6f4",
                paper_bgcolor="#f8f6f4",
                height=500,
                margin={"l": 20, "r": 20, "t": 40, "b": 20},
                hoverdistance=5,
            )

            fig.update_xaxes(
                showgrid=True,
                gridcolor="LightGrey",
                zerolinecolor="DarkGrey",
                exponentformat="power",
                type="log",
                range=reg_fig.full_figure_for_development().layout.xaxis.range,
                dtick=1,
                title="Mass eruption rate (kg/s)",
            )

            fig.update_yaxes(
                showgrid=True,
                gridcolor="LightGrey",
                zerolinecolor="DarkGrey",
                exponentformat="power",
                range=reg_fig.full_figure_for_development().layout.yaxis.range,
                title="Column height (km a.v.l.)",
            )

            images.append(
                html.Div(
                    id="regression-plot",
                    className="imagehp",
                    children=[dcc.Graph(id="QH-regression-plot", figure=fig)],
                )
            )

            ypred_store = ypred.drop(columns=[c for c in ypred.columns if "label" in c])

            if xvar == "Q":
                yvar = "H"
            elif xvar == "H":
                yvar = "Q"
            ypred_store.rename(columns={xvar: xvar + " (observed)"}, inplace=True)
            ypred_store.rename(columns={yvar: yvar + " (predicted)"}, inplace=True)

            return images, ypred_store.to_dict(orient="records")

    return app


def make_local_dashboard():
    application = build_app()
    application.run_server(host="127.0.0.1", debug=True)


def interp_rgb(col_list, j):
    assert j >= 0, "in interp_rgb must have j>0"
    assert j < len(col_list), "in interp_rgb must have j<len(col_list)"
    N = len(col_list)

    clow = np.array(
        col_list[int(np.floor(j)) * (N - 1)].strip("rgb(").strip(")").split(","),
        dtype=float,
    )
    chigh = np.array(
        col_list[int(np.ceil(j)) * (N - 1)].strip("rgb(").strip(")").split(","),
        dtype=float,
    )

    inc = j - np.floor(j)

    cinterp = clow + inc * (chigh - clow)

    return "rgb({r},{g},{b})".format(r=cinterp[0], g=cinterp[1], b=cinterp[2])


def shade_rgb_color(color, p):

    r, g, b = color.strip("rgb(").strip(")").split(",")
    r = int(r)
    g = int(g)
    b = int(b)

    if p < 0:
        t = 0
    else:
        t = 255

    if p < 0:
        p = 0
    elif p > 1:
        p = 1

    r = int((t - r) * p) + r
    g = int((t - g) * p) + g
    b = int((t - b) * p) + b

    return "rgb({r:d},{g:d},{b:d})".format(r=r, g=g, b=b)


def add_units(x, units, bracket=False):
    if x != "No data":
        unit_str = units_html(units)
        if unit_str == "":
            return x
        if bracket:
            unit_str = "(" + unit_str + ")"
        return x + " " + unit_str
    else:
        return x
