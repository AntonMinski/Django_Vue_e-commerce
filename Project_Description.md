# Django Vue e-commerce shop. 

This e-commerce project allow users to buy laptops and other used electronics.
it has product module, user module with users admin, order model with shopcart and
orderes history, home module with site structure.

This was my first web-project. Here i preserv most of static files and html / css
on backend side by django and Django templates.

After implemented some JS and Vue scripts to some options, instead os classical
way with django + Ajax / jQuery. 

Backend: Python Django 
Frontend: Vue (only some scripts files)
Rest: partialy implemented, just basic class-based viewsets
User registration and login: username + pasword.
Security: cookies only
Database: PostgreSQL (Django ORM)
Routing: on backend only 


# Software Design Pattern:
classic MVT (had problems with facade on Django)


# Product module:
- Categories model - all products related to them
- Has Mptt plugin to better category tree on html
- Base product models
- Notebook product model - extends basic product model with some additional options
    * Users can change some characteristics on fly, and see,
     how price change immediately
- Notebook images model
- Some additional models


# order module:
- users has their shopcart
- users can place orders based on shopcart and their profile address details, or add
new details
- users can see orders history


# users module:
- users can login, register, see their orders and shopcart
- users can change details
- users can ask some questions on a specific pages, leave some reviews
- users can change or drop their password
- users has own control panel with some options


# User profile:
- additional fields, like preferences, city, adress, etc...
- picture, related to profile


# some additional Django features:
- header with shopcart, user picture, etc, that can be visible on all pages
- templateTags, that holds some info, that we need on every rote
- template inheritance - all with DRY principle


# Rest api:
- basic CRUD functions on modules (not worked with details yet in this project)


# Frontend part:
1) dynamic autosearch script
2) laptop dynamic price change, related to specs change
3) all forms, etc.., done with HTML/CSS/JS.
No simple Django_forms, that lnot in concept with main style concept


# authowization and security:
- Basic Django cookie authorization



  