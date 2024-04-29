import requests
import json
from API_Call import TvShow

def test_API_Call_T1(id):
    # Call API. Each TV Show has an ID which is a number.
    url = f"https://api.tvmaze.com/shows/{id}"

    # Here, we specify the format of the response
    headers = {"accept": "application/json"}

    # Actually doing the call
    response = requests.get(url, headers=headers)

    # Convert the Response to JSON
    show = json.loads(response.text)

    # Create a TvShow Object using the JSON we received
    testShow = TvShow(show["name"], show["premiered"], show["rating"], show["genres"], show["image"], show["status"],
                      show["summary"], show["network"])

    # Add Show to the List of Shows
    print(f"The Test With ID = {id} Gave Us The Following Show")
    print(testShow)

test_API_Call_T1(1)
