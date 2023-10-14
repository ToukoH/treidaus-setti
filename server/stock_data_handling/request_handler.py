import os
import json

from server.config import DIRECTORY
from server.stock_data_handling.stock_data import StockData
from server.utils import format_response_filename


DATA_POINTS = [
    "TICKER",
    "PERIOD",
    "INTERVAL",
]


class RequestHandler:
    """Class for handling the requests to the server"""

    def __init__(self):
        self._filepaths = dict()

    def data_received(self, filepath: os.path, filename: str) -> bool:
        """Saves the filepath of the loaded data and handles other things."""
        self._filepaths.setdefault(filepath, filename)
        return self._create_response(filepath)

    def data_sent(self, filepath: os.path):
        """Wait for a new request"""
        pass

    def _create_response(self, filepath: os.path) -> bool:
        # Load the request data into a dictionary
        with open(filepath, "r") as file:
            data = json.load(file)
        # Check that all of the required data is in the request
        valid = all([x in DATA_POINTS for x in data.keys()])
        if not valid:
            return False
        # Create the response file
        stock_data = StockData(data.get("TICKER"))
        stock_data.get_stock_data_history(data.get("PERIOD"), data.get("INTERVAL"))
        filename = "server_data/" + format_response_filename(self._filepaths.get(filepath))
        stock_data.create_json_file_from_stock_data(filename)
        return True
