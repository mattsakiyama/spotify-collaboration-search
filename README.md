CS50 Final Project

END CREDITS

Collaborators: Aaron Bradford, Matt Sakiyama

The aim of this webpage is to allow users to search for artists and view the songs and albums on which those artists have collaborated.

SETUP:

In order to use this webpage, there are some setup procedures that must be completed. First, you must create a Spotify Developer account and attain an API key. To do so, navigate to this link: https://developer.spotify.com/dashboard/login.

Then:

To install the library called spotipy that will make accessing the spotify API easier, run in the terminal:
pip install spotipy --upgrade

- Log in using your Spotify account, or create a new spotify account and use those credentials to log in.
- Once logged in, you should see a dashboard page. On this page, click "Create an app."
- You will be asked to enter an app name and an app description; input placeholders for those fields.
- On the left side of your screen, you will see a Client ID; copy this Client ID and save it someplace.
- Then, click "Show Client Secret", copy that text and save it someplace.
- In your terminal, navigate to the folder containing the project files
- Using "sqlite3 songs.db" in your terminal, run this SQL query:

CREATE TABLE users (id INTEGER, username TEXT NOT NULL UNIQUE, hash TEXT NOT NULL, PRIMARY KEY(id));

- You can then exit sqlite3

- Then enter these into your terminal, replacing the bracketed sections with the IDs you saved earlier (and remove the brackets before running)

export SPOTIPY_CLIENT_ID=[insert Client ID here]

export SPOTIPY_CLIENT_SECRET=[insert Client Secret here]

- Now, after moving into the directory containing your project, you should be able to run the "flask run" command to load the webpage preview

USAGE NOTES:

To use the webpage, you must first create an account. Click the reigster button. Then, create an account, ensuring that your password contains 8 characters, and contains at least 1 number. At this point, you should be taken to the search page.

On the search page, you can search for any number of artists in one line, without worrying about separating the artists.

For example, these are some examples of queries that will work:

"Drake" "drake" "Drake, 21 Savage" "Drake 21 Savage" "Drake 21 Savage Metro Boomin'"

Once you've entered your search, you will be shown a list of results. At the top will be the beginning of a list of songs on which the artists have collaborated, alongside their popularity. (This popularity is a value from 0-100 as determined by Spotify, based on the number of plays that song receives and how recent those plays have been.) At the end of the song section, a link to "See More" will take you to /songs, which displays a longer list of songs on which the artists have collaborated. Below the Songs section of the page, there is an Albums section, where any albums/singles that include collaborations by the artists are listed. As with the songs section, the "see more" link will take you to the full list of albums on which the artists have collaborated.

As a side note, you can also access the full lists of songs and albums by using the navbar at the top of the webpage instead of clicking "see more." And to create a new search, simply click "Search" in the navbar, which will allow you to initiate a new search with a different query. Clicking the title of the site "End Credits" will also take you back to the main page of the site, 

LIMITATIONS:

There are a few limitations with our current implementation of this project. Firstly, due to an inherent limitation of the Spotify API, every search through the Spotify library is limited to 50 results. This means that the maximum number of results this web app can return is 50 songs and 50 albums. Secondly, singles are classified as albums in Spotify. As a result, many album results will actually be singles. Finally, there are some occasions in which some of the results will simply be songs/albums that contain the names of the artists included in their titles instead of being songs/albums that those artists collaborated on. This is just a result of the way searches are made through the Spotipy python library that we used.

It should also be noted that we were overly ambitious in our proposal for this project; as a result, we were not able to complete every aspect of the project that we included in our proposal. However, reaching this level of functionality was a huge task in itself, and it was not for a lack of effort that we could not achieve everything we hoped to.
