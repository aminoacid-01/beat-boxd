# BeatBoxd - Everyone's a critic!
If everyone's a critic-  why not share your opinion?

A fully responsive django web application that allows users to review and rate their favourite (or least favourite) albums. Users can comment on existing reviews to keep the discussion going. 

[ put am i reponsive image here]

Deployed Link: https://beatboxd-e433560dd363.herokuapp.com/

## Contents:
- [UX - User Experience:](#ux---user-experience)
    - [User Stories](#user-stories)
    - [Wireframes](#wireframes)
    - [Design](#design)
    - [Accessibility](#accessibility)
    - [Fonts](#fonts)
- [Database Planning:](#database)
    - [ERDS](#erd)
- [Key Features:](#key-features)
    - [General]()
    - [Reviews]()
    - [Comments]()
    - [Future Features]()
- [AI Implementation]()
    - List them here
- [Testing:]()
    - [Validators]()
    - [Manual Testing]()
    - [Automated Testing]()
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

I used Coolors to help me workshop the overall colour scheme of BeatBoxed. After many iterations and testing the colours out in [Realtime Colors](https://www.realtimecolors.com/?colors=1f0a1c-dbf1fa-7f4b91-411f2a-de643b&fonts=Monoton-Truculenta), I eventually settled on the current colour scheme.

![rt_colors](docs/design/rt_colors.png)
![coolors](docs/design/beatboxd_coolors.png)


### Accessibility:


### Fonts:
As you can see in the picture

## Database Planning:
Before setting out on working on the project, I planned out some of my database models. 

### ERDs:


## Key Features

### General:
- **Navbar**: Displaying title in the Monoton font. Working navigational links to the homepage, sign in/out/up pages and create review page.
- **Footer**: Displays the copyright and project name. Has a link to my github.
- **Hero Banner**: Displays a photo of some cds to help the musical theming. A call to action with a button encouraging users to take part in the community and write their own reviews.

### Reviews:
- **CRUD**: Both site admins and users with accounts can create, read, edit, and delete reviews. Users can only delete their reviews.
- **Create/Edit Review Form**: A front-facing form where logged-in individuals can create and edit reviews. Created reviews can be seen listed on the review list page. I used javascript to hide the album input information when selecting prexisting albums from the database and fill the hidden inputs with the information.
- **Delete**: Users can delete their own comments by clicking on the delete button. Upon clicking the button, they will be redirected to the delete confirmation page where they will be asked if they are sure they want to delete. The extra confirmation is to ensure users don't accidentally delete their own posts by misclicking.
- **Album Link**: The review database is linked to the album database, so users can select any prexisting albums from a dropdown or create a new album in the database while they are filling out the create review form.
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
    - **Rating** (only if a rating is associated with the review)
    - **Review Body**
    - **Comment Form**
    - **List of Comments**



 

### Albums:
- **LastFM API integration**: I used the LastFM api to fetch album information to fill the album database. I decided to use this rather than having users upload album information or filling it out myself because it's more efficient. It saves time for both the end-users and the site admins.



### Comments:
- **CRUD**: Both site admins and users with accounts can create, read, edit, and delete reviews. Users can only edit and delete their own comments.
- **Comments Form**: A form on the review detail page where logged-in users can post comments. Upon form submission, users are presented with feedback below the form letting them know that their comment has gone through and is awaiting approval.
- **Edit Comment Form**: Users can edit their own comments. JavaScript is used to make the edit button toggle the visibility of the edit form for better user experience.
- **Moderation**: Site admins can approve comments before they appear in the dedicated comment section.










