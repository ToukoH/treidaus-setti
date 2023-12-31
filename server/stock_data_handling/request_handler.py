import os
import json

from server.config import DIRECTORY
from server.stock_data_handling.stock_data import StockData
from server.utils import format_response_filename


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
        # Clears the server of any json
        if data.get("CLEAR"):
            for filename in os.listdir(DIRECTORY + "/server_data"):
                if filename.endswith(".json") and os.path.isfile(
                    os.path.join(DIRECTORY + "/server_data", filename)
                ):
                    os.remove(os.path.join(DIRECTORY + "/server_data", filename))
            return True

        # Check that the ticker is specified in the request
        if not data.get("TICKER"):
            return False

        # Create the response file
        stock_data = StockData(data.get("TICKER"))
        if data.get("PERIOD"):
            # Period is used
            stock_data.load_data(
                period=data.get("PERIOD"), interval=data.get("INTERVAL")
            )
        else:
            # Start and end date are used
            stock_data.load_data(
                start=data.get("START_DATE"),
                end=data.get("END_DATE"),
                interval=data.get("INTERVAL"),
            )

        filename = "server_data/" + format_response_filename(
            self._filepaths.get(filepath)
        )
        stock_data.create_json_file_from_stock_data(filename)
        return True
