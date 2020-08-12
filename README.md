
# CS50 Final Project
 ### It is a web application for online hotel booking.  
Rooms in the hotel are grouped by room categories. Each room category shares the same price, description and images. The user can use the search form to choose the necessary dates and number of guests and get a list of available room categories. The category is displayed in the list if it has at least one free room. Search is available for all users. Booking is available only for registered users. After choosing a room user may add optional service such as transfer to his order. The site has detailed views for every room category, which are fully editable by the admin including foto in the carousel. Also, every user has their own editable profile.  


Note, that it's possible to check-in and check- out for different guests on the same day for the same room.


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
Python 3.7
Django 3.0.8
jQuery
Bootstrap 4


![database schema](https://www.planttext.com/api/plantuml/img/XPDDJyCm38Rl-HKv8u745N4O7vgq0qD2uuoyrElCcgHANAH9_7ZIDbdIWCIbiPyazcixNNa6nuFkvAsm-qzKBD-irK_0s5ft5gBqv9safYO6DDQiGQySzKpMr5iQoAmjsveVG557JEZhdTwH-fL1GHykyBdcR1cw1sq7mw8iQ3s7ZmKbBnTK4aPT7RkHLPeNCEUGQreNUUQBEMwmN5YsWzwZIqHTkhkKV_zzBUEHLuCvVahmQEs9J2k5IDQK9pll7jsc16FkmWNdw0kwWZJOZ_DtMB1sGC--00ewzJ6FOIvXKfht5sAZrb6A5zCtd0YYahaTtqlqnZZ_1TevCFuGcYUIDLTTUEg8weGB52jz3gtz0-z8B_2Xe_R8SKW5jwuP4oU1Kbu5kHT5CYiEo-8PR3IqiLcJcKPH0j9jDV-v7Jc0h5koGjE4VpMyY1y0)

Detailed requirements can be found [here](https://cs50.harvard.edu/web/2020/projects/final/capstone/)