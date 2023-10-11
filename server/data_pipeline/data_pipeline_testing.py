import requests
import json
import time
import os


def dump_data(data: str, filename: str, server_url: str) -> None:
    """
    **Dumps data to the server**

    Args:
        data (str): Data to dump as a json string
        filename (str): Name of the file
        server_url (str): URL of the server

    """
    url = server_url + "writeFile/" + filename
    response = requests.post(url, data=json.dumps({"str_contents": data}))
    print(response.text)


def get_data(filename: str, server_url: str, client_url: os.path) -> None:
    """
    **Retrieves data from the server**
    
    Args:
        filename (str): Name of the file that is to be retrieved
        server_url (str): URL of the server
        client_url (os.path): Full file path of the file that will be written to the client
    """
    url = server_url + "getJsonFile/" + filename
    response = requests.get(url)
    if response.status_code == 200:
        with open(client_url, "wb") as f:
            f.write(response.content)
        print("File downloaded successfully.")
    else:
        print("File not found or error occurred.")


if __name__ == '__main__':
    host_url = "http://localhost:8000/"
    dir = os.path.dirname(os.path.dirname(__file__))

    # Define the contents and name of the json file that will be written to the server.
    contents = '{"one": 1, "two": 2}'
    filename = "test.json"

    # For this to work, a folder named client§_data_for_testing needs to be created in the server directory.
    filepath = os.path.join(dir, "client_data_for_testing/" + filename)

    dump_data(contents, filename, host_url)
    time.sleep(3)
    get_data(filename, host_url, filepath)
