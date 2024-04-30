import requests
import json
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore


def initFirebase():
    try:
        # Fetch credentials from Streamlit's secrets
        firebase_credentials = {
            "type": st.secrets["type"],
            "project_id": st.secrets["project_id"],
            "private_key_id": st.secrets["private_key_id"],
            "private_key": st.secrets["private_key"].replace('\\n', '\n'),
            "client_email": st.secrets["client_email"],
            "client_id": st.secrets["client_id"],
            "auth_uri": st.secrets["auth_uri"],
            "token_uri": st.secrets["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["client_x509_cert_url"]
        }

        # Create a credential object with the fetched credentials
        cred = credentials.Certificate(firebase_credentials)

        # Initialize the Firebase app with the created credentials
        firebase_admin.initialize_app(cred)
        print("Firebase Initialized Successfully")
    except Exception as e:
        print(f"Failed to initialize Firebase: {e}")

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
        return f"{self.showName} - {self.showYear} - {self.showRating} - {self.showImage} - {self.genre} - {self.status} - {self.network}"


    def __hash__(self):
        return hash((self.showName, self.showYear, self.network))

    def __eq__(self, other):
        return self.showName == other.showName and self.showYear == other.showYear

def fetchTvShows(numberOfShows):
    for id in range(1, numberOfShows):
        #Call API. Each TV Show has an ID which is a number. By running a loop that we can change the ID and get the information for multiple shows.
        url = f"https://api.tvmaze.com/shows/{id}"

        # Here, we specify the format of the response
        headers = {"accept": "application/json"}

        # Actually doing the call
        response = requests.get(url, headers=headers)

        # Convert the Response to JSON
        show = json.loads(response.text)

        try: #added this try to address some shows not having a premiered date and causing an error
            # Create a TvShow Object using the JSON we received
            testShow = TvShow(show["name"], show["premiered"], show["rating"], show["genres"], show["image"], show["status"], show["summary"], show["network"])

            # Add Show to the List of Shows
            listOfShows.append(testShow)
        except:
            pass #just skips the show causing problems

if __name__ == "__main__":
    ##TODO: Cole, please pick a good number of shows you think the app should have
    ##TODO: MAKE SURE TO CHANGE PATH TO MATCH YOUR OWN

    initFirebase()
    db = firestore.client()
    fetchTvShows(100)
    for show in listOfShows:
        db.collection("Shows").document(show.showName).set({
            "showName": show.showName,
            "showYear": show.showYear,
            "showRating": show.showRating,
            "showImage": show.showImage,
            "genre": show.genre,
            "status": show.status,
            "summary": show.summary,
            "network": show.network
        })