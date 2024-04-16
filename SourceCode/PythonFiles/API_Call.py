import requests
import json

# This Code Gets 10 TV Shows and Adds them to a List of Shows

listOfShows = []

class tvShow:
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
        return f"{self.showName} - {self.showYear} - {self.showRating}"


for i in range(1, 10):
    url = f"https://api.tvmaze.com/shows/{i}"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    show = json.loads(response.text)

    testShow = tvShow(show["name"], show["premiered"], show["rating"], show["genres"], show["image"], show["status"], show["summary"], show["network"])

    listOfShows.append(testShow)

for show in listOfShows:
    print(show)
