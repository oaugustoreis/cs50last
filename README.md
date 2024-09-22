
# News.Io

News.Io is a dynamic web application built with Django and JavaScript that allows users to personalize their news-reading experience. The application integrates with a news API (NewsAPI) to fetch the latest headlines and display them according to the user's category preferences and search queries. The application also supports saving news as favorites, theme personalization with "Dark Mode," and keyword search functionality.


## Distinctiveness and Complexity
This project meets the criteria for distinctiveness and complexity for the following reasons:

- Distinctiveness:
    Unlike conventional e-commerce or social media projects, this project focuses on a personalized content aggregation application where users can select and view news based on their preferences.

    The application makes use of external APIs to provide dynamic and relevant content, something not covered in other course projects.


- Complexity:
    The application integrates several advanced features, such as content preference customization, external API integration, user authentication, and storing user preferences in the database.

    The use of JavaScript for dynamic updates without reloading the page and support for Dark Mode adds an extra layer of interactivity and personalization.
  
## Features

  ### User Authentication:
    Users can create accounts, log in, and save their news preferences.
    Each user has their own profile with preferred news categories and sources.

  ### Content Personalization:
    Users can choose their favorite news categories (technology, sports, business, etc.).

  ### News Display
    News is displayed on the homepage, showing headlines, a brief summary, and an image.
    Users can click on a headline to be redirected to the original news website.

  ### Search Filters:
    Users can search for news by keywords or sort the results by publication date.

  ### Save Favorite News:
    Users can save news for later reading.

  ###  Dark Mode:
    Users can switch between light and dark modes for a personalized visual experience.
    
  ### Responsive Design:
    The application is adapted to work on both mobile and desktop devices.

## Technologies Used

- Frontend: HTML5, CSS3, JavaScript
- Backend: Django (Python), Django ORM
- Database: SQLite
- API Integration: NewsAPI
- User Authentication: Django's built-in authentication system


## Installation

1. Clone the repository:

```bash
  git clone https://github.com/oaugustoreis/news.io.git
```
2. Set up the database and migrate the tables:

```bash
  python manage.py makemigrations
  python manage.py migrate
```
3. Create a superuser (optional, for administration):

```bash
  python manage.py createsuperuser
```
4. Start the development server

```bash
  python manage.py runserver
  Abra seu navegador e vá até http://127.0.0.1:8000/
```

## Main Files

- manage.py: Main script for Django administrative commands.

- settings.py: General project settings.

- urls.py: Application routing.

- views.py: Handles page display logic and rendering.

- models.py: Defines data models, such as categories, sources, and favorite news.

- templates/: Directory containing HTML files for the main pages and settings.

- static/: Directory containing CSS and JavaScript files for the frontend.

- layout.html: Main page layout for the project.

- login.html: User login page.

- register.html: User registration page.

- saved.html: Page displaying saved news for the user.

- search.html: Page showing the search results based on user queries.

- style.css: CSS file for project styling.

- togglebutton.css: CSS file for the Dark Mode toggle button

## Authors

- [@oaugustoreis](https://www.github.com/oaugustoreis)

