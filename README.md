# BeatBoxd - Everyone's a critic!
If everyone's a critic-  why not share your opinion?

A fully responsive django web application that allows users to review and rate their favourite (or least favourite) albums. Users can comment on existing reviews to keep the discussion going. 

![ screenshot of site ](docs/design/screenshot.png)


[Deployed Link](https://beatboxd-e433560dd363.herokuapp.com/)

## Contents:
- [UX - User Experience:](#ux---user-experience)
    - [User Stories](#user-stories)
    - [Wireframes](#wireframes)
    - [Design](#design)
    - [Accessibility](#accessibility)
    - [Fonts](#fonts)
- [Database Planning](#database)
- [Key Features:](#key-features)
    - [General](#general)
    - [Reviews](#reviews)
    - [Albums](#albums)
    - [Comments](#comments)
    - [Future Features]()
- [AI Implementation]()
- [Testing:]()
    - [Validators]()
    - [Manual Testing]()
    - [Automated Testing]()
- [Deployment](#deployment)
    - [Heroku]()
    - [PostgreSQL - Code Institute]()
    - [LastFM API]()
- [Credits]()


## UX - User Experience

### User Stories:
Project Board: [link](https://github.com/users/aminoacid-01/projects/4)


[List User Stories If I have time later]

### Wireframes:
When I have time put wireframes for all relevant pages.

[Mobile wfs]
[Desktop wfs]
[Tablet wfs]

### Design:



#### Colour Scheme:

- #1f0a1c
- #dbf1fa
- #7f4b91
- #411f2a
- #de643b

Coolors was used to help workshop the overall colour scheme of BeatBoxed. After many iterations and testing the colours out in [Realtime Colors](https://www.realtimecolors.com/?colors=1f0a1c-dbf1fa-7f4b91-411f2a-de643b&fonts=Monoton-Truculenta), the current colour scheme is the one that was used for BeatBoxd.

![rt_colors](docs/design/rt_colors.png)
![coolors](docs/design/beatboxd_coolors.png)


### Accessibility:


### Fonts:
As pictured in the colour scheme section, Real Time Colours was also used to preview and plan potential font combinations. 

**Monoton**:
A retro style font

**Truculenta**:
A thin and stylish font for body text

## Database Planning
The album, review and rating models are unique custom models.
Models and their ERDs were planned out with the use of [dbdiagram.io](https://dbdiagram.io).

![db](docs/db.png)


## Key Features

### General:
- **Navbar**: Displaying title in the Monoton font. Working navigational links to the homepage, sign in/out/up pages and create review page.
- **Footer**: Displays the copyright and project name.
- **Hero Banner**: Displays a photo of some cds to help the musical theming. A call to action with a button encouraging users to take part in the community and write their own reviews.

### Reviews:
- **CRUD**: Both site admins and users with accounts can create, read, edit, and delete reviews. Users can only delete their reviews.
- **Create/Edit Review Form**: A front-facing form where logged-in individuals can create and edit reviews. Created reviews can be seen listed on the review list page. I used javascript to hide the album input information when selecting prexisting albums from the database and fill the hidden inputs with the information.
- **Delete**: Users can delete their own comments by clicking on the delete button. Upon clicking the button, they will be redirected to the delete confirmation page where they will be asked if they are sure they want to delete. The extra confirmation is to ensure users don't accidentally delete their own posts by misclicking.
- **Album Link**: The review database is linked to the album database, so users can select any prexisting albums from a dropdown or create a new album in the database while they are filling out the create review form.
- **Ratings**: When creating new reviews, users will have the option to rate the current album from 1-5. If a user has associated a rating with their review, it will display it above the review body text.
- **Read Reviews**: Users can look at a short list of recent reviews on the home page. There's also a dedicate review list page where users can see a list of all available reviews. The review list displays:
    - **Album Cover**
    - **Album Title and Artist**
    - **Review Title**
    - **Author**
    - **Created On**
    - **Review Excerpt**: Shows an excerpt of the full review. If the review body is longer than 250 characters, the excerpt will only be the first 247 characters followed by trailing ellipses.

- **Review Detailed View**: When a user clicks one of the reviews in the review list they are redirected to an expanded version of the review displaying:
    - **Album Cover**
    - **Album Title and Artist**
    - **Review Title**
    - **Author**
    - **Created On**
    - **Updated On**
    - **Rating** (only if a rating is associated with the review)
    - **Review Body**
    - **Comment Form**
    - **List of Comments**

 

### Albums:
- **LastFM API integration**: I used the LastFM api to fetch album information to fill the album database. I decided to use this rather than having users upload album information or filling it out myself because it's more efficient. It saves time for both the end-users and the site admins.
- **Average Rating**: Displayed alongside album information.



### Comments:
- **CRUD**: Both site admins and users with accounts can create, read, edit, and delete reviews. Users can only edit and delete their own comments.
- **Comments Form**: A form on the review detail page where logged-in users can post comments. Upon form submission, users are presented with feedback below the form letting them know that their comment has gone through and is awaiting approval.
- **Edit Comment Form**: Users can edit their own comments. JavaScript is used to make the edit button toggle the visibility of the edit form for better user experience.
- **Moderation**: Site admins can approve comments before they appear in the dedicated comment section.

## AI Implementation

Copilot was used for:
- Advice on planning out album model
- Speed up coding via auto complete.
- Assist with bootstrap grids when stuck.
- Some JS, such as:
    - auto populating the hidden fields with existing album data for the create reviews form.
    - hiding the edit comments form.
- Setting up the implementation of the LastFM API.
- Troubleshooting any errors that came from working with the LastFM API.
- Fixing template errors.
- Workshop how to step by step write some functions.
- Speed up writing and updating docstrings
- Some commit messages
- Quickly apply similar bootstrap styling of one template to other related templates to save time. (eg. styling other account templates to have the bootstrap classes of the sign_up page).
- Advise and feedback on changes to models to double check that migrating them wouldn't cause problems.
- Troubleshooting JSON errors caused by the API.

Some problems that were caused by using Copilot were:
- It was inconsistant with naming conventions, particularly in the js.
- It would remove my own comments that I wrote for my own future reference.
- Would sometimes write comments that were incorrect.
- It would remove endblocks and endifs, breaking some django templates.
- It sometimes would create unwanted changes and edits to other files in the workspace.


## Testing

[Fill out with testing info]

## Deployment

### Heroku:
BeatBoxed was deployed via Heroku. Early deployment was utilised to ensure the project was properly configured and compatible with heroku.

[steps]

### PostgreSQL - Code Institute:
[steps] 

### LastFM API:
The project utilises the LastFM API to fetch album information to fill the Album database.

1. Sign up for Last.fm API key:
    - Go to https://www.last.fm/api/account/create
    - Create an API application and make a note of the API key.

2. Install reqests library:
    - Install the requests library using pip.
    - Use the requests library to make HTTP requests to the Last.fm API

3. Store API key in env.py
    - For security purposes, store the API key in the env.py.

4. Write a function to fetch and store album data from Last.fm using said API key.
    - the url: 'http://ws.audioscrobbler.com/2.0/'
    - Use the function to fetch and store data to the album model.

## Credits

- **Images:**
    - Album covers - Last.fm
    - Hero Image - Unsplash (person's username and link to post)
- **Code/Database Models**:
    - Used some of the steps I Think, Therefore I Blog tutorial to help set up the project.
    - Comment model - I Think, Therefore I Blog.


### Aknowlegements:
















