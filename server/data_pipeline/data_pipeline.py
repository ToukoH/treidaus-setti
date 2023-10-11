import os
from pydantic import BaseModel

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

app = FastAPI()

# Root directory of server
dir = os.path.dirname(os.path.dirname(__file__))

class ConfigContents(BaseModel):
    str_contents: str


@app.get("/")
async def root() -> dict:
    return {"message": "blank"}


@app.post("/writeFile/{fn}")
async def write_file(fn: str, contents: ConfigContents) -> ConfigContents:
    """
    **Write files into the server**

    Args:
        fn (str): Name of the file, must end with .json
    
    Returns:
        ConfigContents: Contents of the file
    """
    filepath = os.path.join(dir, "server_data/" + fn)
    with open(filepath, "w") as f:
        f.write(contents.str_contents)
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
    filepath = os.path.join(dir, "server_data/" + fn)
    if os.path.exists(filepath):
        return FileResponse(filepath)
    else:
        raise HTTPException(status_code=404, detail="File not found")
