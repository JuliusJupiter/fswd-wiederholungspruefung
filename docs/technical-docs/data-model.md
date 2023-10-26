---
title: Data Model
parent: Technical Docs
nav_order: 3
---

# Data model
{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

## Changes to the Datamodel

### User class

First i added a User model class. 
It has a "id" Value (Integer) which has the autoincrement parameter set to "True" and functions as the primary key.
I Added two other attributes of typ string to store the "username" and the "password". Both have the propertie "nullable" set
 to "False" and "username also has the "unique" propertie set to "True".
Flask login requires you to implement the following methods:

 __init__(self, username, password)

is_active(self)
    
get_id(self)
    
is_authenticated(self)

If i understood correctly you could alternatively let your user class extend UserMixin from flask_login, but i desided to 
just implement the methods because i already was half way finished when i read about the usermaxin in the flask-login documentation.

### Todo class

I added the user_id as an attribute to the Todo Model class. It´s an foreign-key connecting a todos to a id from the "User" class.
It has the propertie "ondelete" set to "CASCADE" so the todos from a User will be deleted if the User is deleted.

### Insert sample method

I added some sample-user to the "insert_sample" method, so i could use this method for testing!