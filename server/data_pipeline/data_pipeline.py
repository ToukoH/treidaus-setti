import os
from pydantic import BaseModel

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from ..config import DIRECTORY
from ..stock_data_handling.request_handler import RequestHandler
from ..utils import format_request_filename, format_response_filename

class ConfigContents(BaseModel):
    """Class for holding the contents of the transmitted .json files"""
    str_contents: str


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
async def write_file(fn: str, contents: ConfigContents) -> ConfigContents:
    """
    **Write files into the server**

    Args:
        fn (str): Name of the file, must end with .json
        contents (ConfigContents): Contents of the file
    
    Returns:
        ConfigContents: Contents of the file
    """
    fn = format_request_filename(fn)
    filepath = os.path.join(DIRECTORY, "server_data/" + fn)
    # Write the contents of the request into a file with a _request suffix
    with open(filepath, "w") as f:
        f.write(contents.str_contents)
    # Notify the server that the new request file has been written
    success = manage_requests.data_received(filepath, fn)
    if not success:
        raise HTTPException(status_code=401, detail=(
            "valid request is of form {\"TICKER\":\"AAPL\", \"INTERVAL\":\"1d\", \"PERIOD\":\"1mo\"}")
        )
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
