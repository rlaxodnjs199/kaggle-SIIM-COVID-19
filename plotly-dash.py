import dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request

import os
from dotenv import load_dotenv

load_dotenv()

PGSQL_DB = os.getenv("PGSQL_DB")
PGSQL_USER = os.getenv("PGSQL_USER")
PGSQL_PW = os.getenv("PGSQL_PW")

server = Flask(__name__)
app = dash.Dash(__name__, server=server, suppress_callback_exceptions=True)
app.server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.server.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://{PGSQL_USER}:{PGSQL_PW}@localhost/{PGSQL_DB}"

db = SQLAlchemy(app.server)


class TestResult(db.Model):
    __tablename__ = "train_result"

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    server_name = db.Column(db.String(10))
    model_name = db.Column(db.String(30))
    epoch = db.Column(db.Integer)
    batch_size = db.Column(db.Integer)
    optimizer = db.Column(db.String(30))
    learning_rate = db.Column(db.Float)
    drop_out = db.Column(db.Integer)
    train_loss = db.Column(db.Float)
    train_accuracy = db.Column(db.Float)
    validate_loss = db.Column(db.Float)
    validate_accuracy = db.Column(db.Float)


# ------------------------------------------------------------------------------------------------


app.layout = html.Div(
    [
        # activated once/week or when page refreshed
        dcc.Interval(id="interval_pg", interval=86400000 * 7, n_intervals=0),
        html.Div(id="postgres_datatable"),
        html.Button("Add Row", id="editing-rows-button", n_clicks=0),
        html.Button("Save to PostgreSQL", id="save_to_postgres", n_clicks=0),
        # Create notification when saving to excel
        html.Div(id="placeholder", children=[]),
        dcc.Store(id="store", data=0),
        dcc.Interval(id="interval", interval=1000),
        dcc.Graph(id="my_graph"),
    ]
)


# ------------------------------------------------------------------------------------------------


@server.route("/train-result", methods=["POST"])
def add_train_result():
    request_data = request.get_json()
    print(request_data)
    return request_data


@app.callback(
    Output("postgres_datatable", "children"), [Input("interval_pg", "n_intervals")]
)
def populate_datatable(n_intervals):
    df = pd.read_sql_table("train_result", con=db.engine)
    return [
        dash_table.DataTable(
            id="our-table",
            columns=[
                {
                    "name": str(x),
                    "id": str(x),
                    "deletable": False,
                }
                for x in df.columns
            ],
            data=df.to_dict("records"),
            editable=True,
            row_deletable=True,
            filter_action="native",
            sort_action="native",  # give user capability to sort columns
            sort_mode="single",  # sort across 'multi' or 'single' columns
            page_action="none",  # render all of the data at once. No paging.
            style_table={"height": "300px", "overflowY": "auto"},
            style_cell={
                "textAlign": "left",
                "minWidth": "100px",
                "width": "100px",
                "maxWidth": "100px",
            },
        ),
    ]


@app.callback(
    Output("our-table", "columns"),
    [Input("adding-columns-button", "n_clicks")],
    [State("adding-rows-name", "value"), State("our-table", "columns")],
    prevent_initial_call=True,
)
def add_columns(n_clicks, value, existing_columns):
    if n_clicks > 0:
        existing_columns.append(
            {"name": value, "id": value, "renamable": True, "deletable": True}
        )
    return existing_columns


@app.callback(
    Output("our-table", "data"),
    [Input("editing-rows-button", "n_clicks")],
    [State("our-table", "data"), State("our-table", "columns")],
    prevent_initial_call=True,
)
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c["id"]: "" for c in columns})
    return rows


if __name__ == "__main__":
    app.run_server(debug=True)
