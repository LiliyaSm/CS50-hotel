
# CS50 Final Project
 ### It is a web application for online hotel booking.  
Rooms in the hotel are grouped by room categories. Each room category shares the same price, description and images. The user can use the search form to choose the necessary dates and number of guests and get a list of available room categories. The category is displayed in the list if it has at least one free room. Search is available for all users. Booking is available only for registered users. After choosing a room user may add optional service such as transfer to his order. The site has detailed views for every room category, which are fully editable by the admin including foto in the carousel. Also, every user has their own editable profile.  


Note, that it's possible to check-in and check- out for different guests on the same day for the same room.


### Distinctiveness and complexity requirements:
This project uses class-based Django views (ListView, DetailView) unlike my previous projects in the CS50 course. Project is implemented with complex forms usage, the admin panel provides multiple images upload capabilities, and custom SQL queries were used to provide available bookings search. It also has more complex page layouts and design: I have implemented a custom mobile navigation menu and slider, swiper. User registration is more difficult either: every user has an editable profile linked with the related user object.

### Project structure:
Project Hotel has two installed apps - users and reservations.


Project Hotel folder contains file urls.py with project-level URL configurations.


In users app directory there are files for providing users registration and login:
* view.py module - the views for users app;
* forms.py module - the forms for users app;
* folder "templates" contains HTML files: registration, profile displaying and so on;
*  models.py - the models to work with data and database.

In reservations app directory there are files for providing the whole process of displaying all site information and handling room booking: 
* folder "templates" contains HTML files for displaying pages: main, booking, room category descriptions and other pages;
* folder "static" contains CSS, javascript and jpg files;
* admin.py - app’s models registered with the Django admin application;
* models.py - the models to work with data and database;
* view.py module - the views for reservations app;
* forms.py module - the forms for reservations app.

In all directories:
* apps.py - defines basic configuration settings

Technologies:
1. Python 3.7
2. Django 3.0.8
3. jQuery
4. Bootstrap 4


![database schema](https://www.planttext.com/api/plantuml/img/XPJBRjmm34Nt-Wgj0oH0jqKNwGC1icWR1Cbwm95f3nCz38akC44_Fh9bZHvjqSs8FB9rhqXwRWE3vyLe-K4miKRv3HYE4506TK83GhZZ2ogMZywPhy0uENyMeixaHqb3JomOxDc0GNcQcPpjjmoGlNFiUZw28arC6FgTsPFwGq7175_WSy_PCUZFnYsMcmlTfUFt2-MiNAWcZAPxx4PsCj_1dgFMjZOwwSLoRenyN7uiveW-4tMfRcl_q-zhkJ_oqs8vFmjySUwLx2I5oD6cKv8beB-lmQfTfU0z_G9TaG7dTImyLcnQC72eW0Aj3gaDwGgRqxBVcDszFaShGMo_oMKELu_Rp6GmaWzyQ926diG19ItsT9N_d_wJ1nl6M7EHesIZokBOgrTiq5wW-6dWN_0JcGQFcgOJxxsjkFF3AfmDIdaLxLuSoU8uBitqt1kOzXflOUvW3SXCtTYaSfG3v3zAyk3TI3gUlmUf82LPErEbLLyAB9qfBFMcvF6xf3UquKHpHUUJitYmgLWNVdqbvTxKjYgtQ8VuRnM7_nq0)

Detailed requirements can be found [here](https://cs50.harvard.edu/web/2020/projects/final/capstone/)
