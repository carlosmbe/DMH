import requests
import json

### This Code Gets 10 TV Shows and Adds them to a List of Shows

listOfShows = []

class TvShow:
    ### This class represent a TV Show based on the information we get from the API
    def __init__(self, showName, showYear, showRating,showGenre, showImage, status, summary, network):
        self.showName = showName
        self.showYear = showYear
        self.showRating = showRating
        self.showImage = showImage
        self.genre = showGenre
        self.status = status
        self.summary = summary
        self.network = network

    def __str__(self):
        ### I created this for testing purposes.
        return f"{self.showName} - {self.showYear} - {self.showRating}"


for id in range(1, 10):
    #Call API. Each TV Show has an ID which is a number. By running a loop that we can change the ID and get the information for multiple shows.
    url = f"https://api.tvmaze.com/shows/{id}"

    # Here, we specify the format of the response
    headers = {"accept": "application/json"}

    # Actually doing the call
    response = requests.get(url, headers=headers)

    # Convert the Response to JSON
    show = json.loads(response.text)

    # Create a TvShow Object using the JSON we received
    testShow = TvShow(show["name"], show["premiered"], show["rating"], show["genres"], show["image"], show["status"], show["summary"], show["network"])

    # Add Show to the List of Shows
    listOfShows.append(testShow)


#TODO: John and Kenji. Instead of printing each show, upload them to the Firebase Database. Also change the For Loop to over a good number of shows. Maybe 20,100 or 500.

for show in listOfShows:
    print(show)
