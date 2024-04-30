import firebase_admin
import re
from firebase_admin import  firestore
from API_Call import TvShow

def remove_html_tags(html):
    # Remove HTML tags using regular expressions
    clean = re.compile('<.*?>')
    return re.sub(clean, '', html)

showList = []

db = firestore.client()

# Get a reference to the database
doc_ref = db.collection("Shows").stream()

for ele in doc_ref:
    # Read data
    doc = ele.to_dict()

    #converts the list of genres into a string
    genre=", ".join([str(item) for item in doc["genre"]])

    #cleans the summary of html tags
    summary = remove_html_tags(doc["summary"])

    #Show creation in the form of (showName, showYear, showRating, showGenre, showImage, status, summary, network)
    try:
        show = TvShow(doc["showName"], doc["showYear"], doc["showRating"]["average"], genre, doc["showImage"]["medium"], doc["status"], summary, doc["network"]["name"])
        showList.append(show)
        print(show)
    except:
        pass
    