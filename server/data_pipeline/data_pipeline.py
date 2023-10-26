import os
from pydantic import BaseModel

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from ..config import DIRECTORY
from ..stock_data_handling.request_handler import RequestHandler
from ..utils import format_request_filename, format_response_filename

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

class RequestContents(BaseModel):
    """
    **Class for holding the contents of the transmitted .json files**

    TICKER: The ticker of the stock which's data is to be fetched

    PERIOD: Supported values 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd or max,
        if not set, START_DATE and END_DATE are used

    INTERVAL: Supported values 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo or 3mo

    START_DATE: In format YYYY-MM-DD, used if PERIOD is not set

    END_DATE: In format YYYY-MM-DD, used if PERIOD is not set

    CLEAR: if True, all .json files on the server will be deleted and no data will be fetched

    """

    TICKER: str = "AAPL"
    PERIOD: str = None
    INTERVAL: str = "60m"
    START_DATE: str = None
    END_DATE: str = None
    CLEAR: bool = False
    ACTIONS: bool = False

    def format_request_params(self):
        """Formats the response"""

        if self.START_DATE or self.END_DATE:
            self.PERIOD = None

        if not self.PERIOD and not self.START_DATE:
            # TODO: make changes to interval so that some data is fetched
            # for example if interval is 1h, data can be fetched from max two years ago

            # if start date is set far back
            self.INTERVAL = "1d"
            print("Changed interval to", self.INTERVAL)


# Initialize the request handler
manage_requests = RequestHandler()

# Initialize the application
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://127.0.0.1:3000"],
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

    contents.format_request_params()

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
