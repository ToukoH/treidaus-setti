import os

from pydantic import BaseModel

from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

# Root directory of server
dir = os.path.dirname(os.path.dirname(__file__))


class ConfigContents(BaseModel):
    str_contents: str


@app.get("/")
async def root():
    return {"message": "blank"}


# Writes data to server
@app.post("/writeFile/{fn}")
async def write_file(fn: str, contents: ConfigContents):
    # Write files into servers data -folder
    filepath = os.path.join(dir, "data/" + fn)
    with open(filepath, "w") as f:
        f.write(contents.str_contents)
    return contents


# Retrieves .json files from server
@app.get("/getJsonFile/{fn}")
async def get_json_file(fn: str):
    filepath = os.path.join(dir, "data/" + fn)

    # Check if the file exists in the directory
    if os.path.exists(filepath):
        return FileResponse(filepath)
    else:
        return {"message": "File not found"}
