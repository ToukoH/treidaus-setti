import os


class RequestHandler():
    """Class for handling the requests to the server"""

    def __init__(self):
        self._filepaths = set()

    def data_received(self, filepath: os.path):
        """Saves the filepath of the loaded data and handles other things."""
        self._filepaths.add(filepath)
        self._do_amazing_things()

    def _do_amazing_things(self):
        print()
        print(self._filepaths)
        print()
