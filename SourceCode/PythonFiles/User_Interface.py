import streamlit as st
from copy import deepcopy
from API_Call import TvShow
from data_collection import showList

# Initialize shows with sample data
all_shows = [
    TvShow("Breaking Bad", 2008, "9.5", "Crime, Drama", None, "Ended", "A high school chemistry teacher turned meth kingpin.", "AMC"),
    TvShow("Sherlock", 2010, "9.1", "Crime, Drama, Mystery", None, "Ended", "A modern update finds the famous sleuth and his doctor partner solving crime in 21st century London.", "BBC One"),
]

def init_state():
    print("Initializing state...")
    if 'all_shows' not in st.session_state:
        st.session_state['all_shows'] = set(deepcopy(all_shows))  # Convert list to set
        print("all_shows initialized")
    if 'watch_list' not in st.session_state:
        st.session_state['watch_list'] = set()  # Initialize as set
        print("watch_list initialized")
    if 'watched_list' not in st.session_state:
        st.session_state['watched_list'] = set()  # Initialize as set
        print("watched_list initialized")

init_state()  # Ensure this is called before any UI components

def move_show(show, from_set, to_set):
    if show in from_set and show not in to_set:
        from_set.remove(show)
        to_set.add(show)
        st.rerun() # Rerun the page to update the show lists

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
                    if show not in st.session_state['watch_list'] and show not in st.session_state['watched_list']:
                        move_show(show, st.session_state['all_shows'], st.session_state['watch_list'])
                    else:
                        st.warning("Show is already in a list.")


                if st.button("Add to Watched List", key=f"add_watched_{key_prefix}"):
                    if show not in st.session_state['watched_list'] and show not in st.session_state['watched_list']:
                        move_show(show, st.session_state['all_shows'], st.session_state['watched_list'])
                    else:
                        st.warning("Show is already in a list.")


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

# Search function
def search_shows(query):
    filtered_shows = [show for show in all_shows if query.lower() in show.showName.lower()]
    return filtered_shows

def display_search_results(filtered_shows):
    if filtered_shows:
        st.write('Search results:')
        for show in filtered_shows:
            with st.expander(f"{show.showName} ({show.showYear})"):
                st.write(f"**Genre:** {show.genre}")
                st.write(f"**Status:** {show.status}")
                st.write(f"**Summary:** {show.summary}")
                st.write(f"**Network:** {show.network}")
                # Generate unique keys for each button action
                key_prefix = f"{show.showName}_{show.showYear}"

                # Check conditions for adding to Watch List
                if show not in st.session_state['watch_list'] and show not in st.session_state['watched_list']:
                    if st.button("Add to Watch List", key=f"add_watch_{key_prefix}"):
                        move_show(show, filtered_shows, st.session_state['watch_list'])
                        # Optionally, remove the show from search results after adding to watch list
                        filtered_shows.remove(show)

                # Check conditions for adding to Watched List
                if show not in st.session_state['watched_list'] and show not in st.session_state['watch_list']:
                    if st.button("Add to Watched List", key=f"add_watched_{key_prefix}"):
                        move_show(show, filtered_shows, st.session_state['watched_list'])
                        # Optionally, remove the show from search results after adding to watched list
                        filtered_shows.remove(show)


st.write("##  Search All Shows")
search_query = st.text_input('Search all shows:', '')
if search_query:
    filtered_shows = search_shows(search_query)
    display_search_results(filtered_shows)
else:
    st.write("Enter a search query above to find a TV show.")

tab1, tab2, tab3 = st.tabs(["All Shows", "Watch List", "Watched List"])
with tab1:
    display_shows_list(st.session_state['all_shows'], 'all_shows')
with tab2:
    display_shows_list(st.session_state['watch_list'], 'watch_list')
with tab3:
    display_shows_list(st.session_state['watched_list'], 'watched_list')
