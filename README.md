# Library Management System - V2

## Objective
To develop a multi-user Library Management System app that is used to issue, grant/revoke and 
maintain e-books across various sections like an online library and mange many more operations

## Frameworks Used:
1. Backend: Flask, Flask_Restful, Flask_SQLAlchemy, Flask_Cors 
2. Frontend: Vue, JavaScript, 
3. Security: Flask-Bcrypt, Flask-JWT-Extended 
4. Database: SQLite 
5. Batch Jobs (Backend Jobs): Redis, Celery

## Roles
The platform will have two roles;

1. librarian - the maintainer of sections and e-books in the library
    * An librarian can monitor all the users, see all the statistics
    * A librarian will create sections, e-books in the library.
    * A librarian can grant/revoke access for an e-book.


2. General user - an individual who wants to access an e-book from the library
    * A user can go through all the available sections and e-books in the library and can request for an e-book.
    * A user can request for maximum of 5 e-books at a time
    * A user can update their profile page, rate an e-book.

## Special Functionalities
1. Admin login and user login (RBAC)
    * Used Flask security and JWT based Token based authentication to implement role based access control


2. Backend Jobs
    * User Triggered Async Job - Export as CSV - Devised a CSV format details using celery and redis for the issued/returned/granted e-books done by the librarian.
    * This export is meant to download the Name, Content, Author(s), Date issued, Return date etc