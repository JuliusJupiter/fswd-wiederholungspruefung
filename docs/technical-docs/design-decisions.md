---
title: Design Decisions
parent: Technical Docs
nav_order: 5
---


# Design decisions
{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

## 01: Decision for a "Login" flask extensions 

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 15-Oct-2023

### Problem statement

For the Login and User handling i had to choose between Flask-HTTPAuth, Flask-Login, Flask-Praetorian or Flask-User.


### Decision

i have decided in favor of "Flask_Login". Since i had some experience with flask_login due to the group project i 
had clear preference for it from the start. I remembered how well i could understand the documentation last time and that
it had good examples in it.

### Regarded options

Before i started to implement the Login with "Flask_Login" i looked into "Flask-Praetorian". I got the impression that it was 
particularly well suited to implement different roles for users. Since the todo app doesn´t require different roles of users i 
didn´t choose it for my login.

After i implemented the API i came acoss the question of login-in with a API. While i looked into the topic i came across some examples
where "Flask-HTTPAuth" was used. Maybe "Flask-HTTPAuth" would have been a good choice, but since i already had used "Flask_Login" i didn´t
want to change everything again.


## 02: Decision for a "API" flask extensions 

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 23-Oct-2023

### Problem statement

For the Api flask extension i had to choose between Flask-RESTful, Flask-Restless-NG, Flask-RESTX and Flask-smorest.


### Decision

i have decided in favor of "Flask_RESTful". While looking into the Flask-RESTful documentation i discovered that the example 
given in the "Quickstart" section was also a Todo app. When i saw that i didn´t looked any further and started to implement the 
API with the "Flask_RESTful" extension like shown in the documentation.

### Regarded options

The "Petstore" example from the flask-smorest documentation wasn´t as good to understand. They used marshmallow as a 
serialization/deserialization library which i didn´t know (at that point) and didn´t plan on using. "Flask_RestX" seems to be quite 
similar to "Flask_Restful". "Flask_Restless" seems to be really simple. I could imagine to use it in the future, but i didn´t looked into 
it after i got inspired by the Flask_RESTful documentation.

