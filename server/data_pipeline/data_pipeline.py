import os
from pydantic import BaseModel

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from typing import Optional

from ..config import DIRECTORY
from ..stock_data_handling.request_handler import RequestHandler
from ..utils import format_request_filename, format_response_filename


class RequestContents(BaseModel):
    """
    **Class for holding the contents of the transmitted .json files**

    TICKER: The ticker of the stock which's data is to be fetched

    PERIOD: Supported values 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd or max,
        if not set START_DATE and END_DATE is used

    INTERVAL: Supported values 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo or 3mo,
        if not set START_DATE and END_DATE is used

    START_DATE: In format YYYY-MM-DD, if not set PERIOD and INTERVAL is used

    END_DATE: In format YYYY-MM-DD, if not set PERIOD and INTERVAL is used

    CLEAR: if True, all .json files on the server will be deleted

    """

    TICKER: str = "AAPL"
    PERIOD: Optional[str] = None
    INTERVAL: str = "90m"
    START_DATE: str = None
    END_DATE: str = None
    CLEAR: bool = False
    ACTIONS: bool = False


# Initialize the request handler
manage_requests = RequestHandler()

# Initialize the application
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000', 'https://127.0.0.1:3000'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> dict:
    return {"message": "Welcome!"}


@app.post("/writeFile/{fn}")
async def write_file(fn: str, contents: RequestContents) -> RequestContents:
    """
    **Write files into the server**

    Args:

        fn (str): Name of the file, must end with .json

        contents (RequestContents): Contents of the file

    Returns:
        RequestContents: Contents of the file
    """
    if contents.START_DATE and contents.END_DATE:
        contents.PERIOD = None
    
    fn = format_request_filename(fn)
    filepath = os.path.join(DIRECTORY, "server_data/" + fn)
    
    with open(filepath, "w") as f:
        f.write(contents.model_dump_json())
    
    success = manage_requests.data_received(filepath, fn)
    if not success:
        raise HTTPException(status_code=401, detail=("Error while handling request"))
    return contents


@app.get("/getJsonFile/{fn}")
async def get_json_file(fn: str) -> FileResponse:
    """
    **Retrieve files from the server**

    If the file does not exist, return a 404 *File not found* -error.

    Args:

        fn (str): Name of the file, must end with .json

    Returns:
        FileResponse: FileResponse object with the specified filepath
    """
    filename = format_response_filename(fn)
    filepath = os.path.join(DIRECTORY, "server_data/" + filename)
    if os.path.exists(filepath):
        manage_requests.data_sent(filepath)
        return FileResponse(filepath)
    else:
        raise HTTPException(status_code=404, detail="File not found")
