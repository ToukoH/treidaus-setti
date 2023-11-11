import yfinance as yf
import os
import pandas as pd

from ..config import DIRECTORY


def get_stock_data_download(
    tickers: list = ["AAPL"], period: str = "1y", interval: str = "1d"
) -> pd.DataFrame:
    return yf.download(tickers, period=period, interval=interval)


class StockData:
    """
    Base class for all stock data classes

    Idk what useful could be added to here but maybe something...

    Args:
        ticker (str, optional): Ticker of the stock. Defaults to "AAPL".
    """

    def __init__(self, tickers: str = "AAPL"):
        self._data = pd.DataFrame()
        self._tickers = tickers

    def load_data(
        self, interval: str, period: str = None, start: str = None, end: str = None
    ):
        self._data = yf.download(
            self._tickers,
            period=period,
            interval=interval,
            start=start,
            end=end,
            group_by="ticker",
        )

    def create_json_file_from_stock_data(self, filename: str):
        try:
            self._data.to_json(
                path_or_buf=os.path.join(DIRECTORY, filename),
                orient="columns",
                date_format="iso",
            )
        finally:
            self._data = None
