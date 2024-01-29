
import yaml
import pathlib
from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from src.components.layout import create_layout
from src.data.loader import load_transaction_data
from src.data.source import DataSource


DATA_PATH = "./data/transactions.csv"


def main() -> None:
    general = yaml.safe_load(pathlib.Path("config/general.yml").read_text())
    category = yaml.safe_load(pathlib.Path("config/category.yml").read_text())

    # load the data and create the data manager
    data = load_transaction_data(DATA_PATH, category)
    data = DataSource(data)

    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = general["app_title"]
    app.layout = create_layout(app, data, general)
    app.run()


if __name__ == "__main__":
    main()
