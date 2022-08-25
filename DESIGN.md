CS50 Final Project

END CREDITS

Collaborators: Aaron Bradford, Matt Sakiyama

The aim of this webpage is to allow users to search for artists and view the songs and albums on which those artists have collaborated.

DESIGN:

For this project we decided to use the Spotify API, accessed at https://developer.spotify.com/dashboard/login. In particular, we decided to use a library called Spotipy, documentation at https://spotipy.readthedocs.io/en/2.19.0/, because it allowed us to use python to ineract with the Spotify API. We chose the spotify API because spotify is a very large music streaming company and thus we trusted that the have vast amounts of music data that we would be able to access. Learning how to use this API and library required extensive effort from the both of us, but is not necessarily reflected in the volume of code required to use the library.

APP.PY:

Imports:
The main back end code of this site is contained in app.py. app.py initially starts by importing needed functions and libraries, many of which are adapted from the import statements needed for the Finance Problem Set. We also import the spotipy library and some needed functions. 

Variable initialization:
Next we initialize the variables that we plan on using as empty versions of what we want them to be, using empty lists for the variables "song", "album", "release", and "popularity". We elected to initialize the variables in this way so that they would be global variables and any function that we would write would be able to access and update the variables in the same way. We also use this to initialize sp as the code needed to access spotify. This was done for the person of ease of writing as it is much simpler to just write "sp" each time.

App configuration:
We then configure the app, using similar code from Finance, and adapating it as we need to, like using a different SQL database.

Index():
Next, we wrote the code for the index page, this had to be the first function because the index page is the main page accessed so we need it to work before all of the other pages. The function renders index.html using values from the global variables sp that any edits to those varibles will be changed on that index page. This also proves the importance of initializing empty global variables, otherwise the code will end up with errors that prevent it from working properly until the variables are introduced. For each variable, we decided to show only the first five values on the page so that it does not get too complicated. The user can use the see more button if they want to look at more results. Access to this page requires log in so that it cannot be accessed by just anyone.

Login():
We then implemented the login function, with similar code from Finance.

Register():
We implemented the register function also using similar code from Finance. The code also included some password requirements. 

Logout(): 
We then also implemented logout using similar code from Finance

Songs() and Albums():
We implemented both the songs and albums page, rendering their respective html pages using values from the global variables that they needed. These pages use global variables because it allows us to use our functions to edit global variables and change all of the website pages at once. Access to these pages require log in so that they cannot be accessed by just anyone.

Search():
We then implemented the search function, which is really the main function of the code. Since the search page can be accessed through both a GET (eg. clicking a link) and POST (eg. submitting a form) method, we simply rendered the search page again everytime the GET method was use and put most of the functionality inside the POST method. Each time something is submitted, the global variables are reset to empty variables so the user only gets the results of their most recent search. This was done so that they user would not have to sort through results for multiple searches, especially as the volume of searches increases. We used a form to get a user input for the artist/artists they were looking for and then we ran two searchs in the spotify API. One search would give us JSON data for each song related to the user's input and the other search would give us JSON data for each album related to the user's input. We did this because we wanted user's to be able to see information about both an artist's songs and albums. After getting these results, we indexed into them in order to get the name and popularity for each song and the name and release date for each album. These were all stored in the different global variables "song", "album", "release", and "popularity". We also included an error message if the user's searches returned no results. Finally, we rendered index.html but this time with some of the results of the user's search (since the data in index only shows the first 5). The songs and albums pages contain the full results of the user's searches. Access to this page requires log in so that it cannot be accessed by just anyone.

Error code:
We then implemented code to check for and handle code errors. This depended on code from Finance.

HELPERS.PY:
In this code we adapted code from the Finance Problem set to implement the functions that we needed for our project, like apology() and login_required()

TEMPLTATES:

In templates we stored all of the html templates of our site. The html was built upon the html of the Finance Problem Set but we made our own adapations to make it showcase what we wanted to.

Layout.html:
This contains the main html that stays the same accross every site. This included code like the navbar, which contains links to all of the pages, and footer that cites spotify as our source. We did this because we can simply extend the layout code each time instead of having to rewrite it for each html file that we make.

Apology.html: 
This just contains the html that displays during some sort of error.

Index.html:
This is the main page of the site, and after the user logs in, this is the first page that they see. The page uses jinja if-else statements to check if there are already any results to display and if not, it shows the search bar to the user. This is so that the user does not just see a blank screen if they enter the page. The user can then search through that search bar and their results will pop up. They will be able to see the names of songs and albums relating to that artists and some analytical data such as the song's popularity and the album's release date. The code uses jinja with for loops to display the results no matter how many results there are. The index page also only shows the first fivce results for each section so that it is not too crowded. The page also contains "see more" links for each section so that the user can see the full list of songs or albums that they looked for. We also formatted the results as tables and used CSS to make it look nice so that they user gets a good looking set of results.

Songs.html and albums.html:
While these two pages are not identical, the concept of the code of the page is similar. It shows the full search results of the user's input, for songs, that means the name of the song and its popularity and for albums that means the name of the album and its release date. Using a jinja if-else statement, the page checks if there are results to display and if not, tells the user to search for some artists.

Login.html and register.html:
The html for these pages relied heavily on the Finance problem set code, providing users with a way to create accounts and log in to the site.

STYLES.CSS:
We also have a styles.css page that determines how all of the page is going to look. This allows us to edit the visual formatting of site such as choosing colors, backgrounds, and results formatting.

ENDING NOTES:
Though finance was used as a template for this project, much of the work that went into this project involved figuring out how to make our ideas into a reality, with a large focus on understanding how to use and API and get to work in the way that we wanted it to. 
We hope you enjoy our project!!
