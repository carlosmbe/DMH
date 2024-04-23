import streamlit as st
from copy import deepcopy
from API_Call import TvShow


# TODO: Cole Dubois. Instead of using all_shows as hardcoded TV Shows, fetch TV Shows from the FireBase Database
# TODO: Blake Ebner Fix the User Interface. Right now, after moving a show to a new list, the website does not refresh proper causing it to show incorrect


# Initialize shows with sample data
#Show creation in the form of (showName, showYear, showRating, showGenre, showImage, status, summary, network)
all_shows = [
    TvShow("Breaking Bad", 2008, "9.5", "Crime, Drama", None, "Ended", "A high school chemistry teacher turned meth kingpin.", "AMC"),
    TvShow("Sherlock", 2010, "9.1", "Crime, Drama, Mystery", None, "Ended", "A modern update finds the famous sleuth and his doctor partner solving crime in 21st century London.", "BBC One"),
]

def init_state():
    print("Initializing state...")  # Debug statement
    if 'all_shows' not in st.session_state:
        st.session_state['all_shows'] = deepcopy(all_shows)
        print("all_shows initialized")  # Debug statement
    if 'watch_list' not in st.session_state:
        st.session_state['watch_list'] = []
        print("watch_list initialized")  # Debug statement
    if 'watched_list' not in st.session_state:
        st.session_state['watched_list'] = []
        print("watched_list initialized")  # Debug statement

init_state()  # Ensure this is called before any UI components

def move_show(show, from_list, to_list):
    if show in from_list:
        from_list.remove(show)
        to_list.append(show)
        st.rerun() #reruns the page to make the show list update correctly

st.title("Show Tracker")

def display_shows_list(shows_list, list_name):
    for show in shows_list:
        with st.expander(f"{show}"):
            st.write(f"**Genre:** {show.genre}")
            st.write(f"**Status:** {show.status}")
            st.write(f"**Summary:** {show.summary}")
            st.write(f"**Network:** {show.network}")
            # Generate unique keys for each button action
            key_prefix = f"{list_name}_{id(show)}"
            if list_name == 'all_shows':
                if st.button("Add to Watch List", key=f"add_watch_{key_prefix}"):
                    move_show(show, st.session_state['all_shows'], st.session_state['watch_list'])
                if st.button("Add to Watched List", key=f"add_watched_{key_prefix}"):
                    move_show(show, st.session_state['all_shows'], st.session_state['watched_list'])
            elif list_name == 'watch_list':
                if st.button("Remove from Watch List", key=f"remove_watch_{key_prefix}"):
                    move_show(show, st.session_state['watch_list'], st.session_state['all_shows'])
                if st.button("Move to Watched List", key=f"move_watched_from_watch_{key_prefix}"):
                    move_show(show, st.session_state['watch_list'], st.session_state['watched_list'])
            elif list_name == 'watched_list':
                if st.button("Move to Watch List", key=f"move_watch_from_watched_{key_prefix}"):
                    move_show(show, st.session_state['watched_list'], st.session_state['watch_list'])
                if st.button("Move to All Shows", key=f"move_all_from_watched_{key_prefix}"):
                    move_show(show, st.session_state['watched_list'], st.session_state['all_shows'])

# Display each list with interactive components
st.write("## All Shows List")
display_shows_list(st.session_state['all_shows'], 'all_shows')
st.write("## Watch List")
display_shows_list(st.session_state['watch_list'], 'watch_list')
st.write("## Watched List")
display_shows_list(st.session_state['watched_list'], 'watched_list')
