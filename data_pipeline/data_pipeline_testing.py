import requests
import json
import time


def dump_data(data, filename: str, server_url: str) -> None:
    url = server_url + "writeFile/" + filename
    response = requests.post(url, data=json.dumps({"str_contents": data}))
    print(response.text)


def get_data(filename: str, server_url: str) -> None:
    url = server_url + "getJsonFile/" + filename
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print("File downloaded successfully.")
    else:
        print("File not found or error occurred.")


if __name__ == '__main__':
    host_url = "http://localhost:8000/"
    contents = '{"one": 1, "two": 2}'
    filename = "some_data.json"

    dump_data(contents, filename, host_url)
    time.sleep(3)
    get_data(filename, host_url)
