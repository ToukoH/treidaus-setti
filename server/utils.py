"""
Useful functions
"""

def format_request_filename(filename: str) -> str:
    """
    Adds a _request suffix to the filename just before the extension
    
    Example: some_file.json -> some_file_request.json

	Args:
    	filename (str): The filename in the reques
    
    Returns:
        str: The formatted filename
    """
    index = filename.find(".json")
    if index == -1:
        raise ValueError(f"Invalid filename: {filename}")
    return filename[:index] + "_request" + ".json"


def format_response_filename(filename: str) -> str:
    """
    Adds a _response suffix in place of the _request suffix on the filename
    or if no _request suffix is present, just adds the _response suffix to the filename.
      
    Example: some_file_request.json -> some_file_response.json
     
    Args:
        filename (str): The filename in the request
    
    Returns:
        str: The formatted filename
    """
    index = filename.find("request.json")
    if index == -1:
        index = filename.find(".json")
        if index == -1:
            raise ValueError(f"Invalid filename {filename}")
        return filename[:index] + "_response.json"
    return filename[:index] + "response.json"
