# Library Management System - V2

**Library Management System - V2** is a multi-user application designed to manage e-books across various sections like an online library. The system supports functionalities such as issuing, granting/revoking, and maintaining e-books. It provides an efficient and structured way for librarians to manage e-books and for general users to access them.

## Frameworks and Tools Used

The project is built using the following frameworks and tools:

- **SQLite**: For data storage.
- **Flask**: For API development.
- **VueJS**: For user interface (UI) development.
- **Bootstrap**: For HTML generation and styling.
- **Redis**: For caching.
- **Redis and Celery**: For batch jobs.

## Roles

The platform includes two primary roles:

1. **Librarian**: The administrator responsible for managing sections and e-books in the library.
   - Can monitor all users and view relevant statistics.
   - Responsible for creating sections and adding e-books.
   - Has the authority to grant or revoke access to e-books.

2. **General User**: An individual who wants to access an e-book from the library.
   - Can browse all available sections and e-books.
   - Can request a maximum of 5 e-books at a time.
   - Has the ability to update their profile and rate e-books.

## Terminologies

### Section
All the e-books in the library are classified into one or more sections (e.g., Philosophy, Science, Arts, etc.).

A section may have:
- **ID**: Unique identifier.
- **Name**: Name of the section.
- **Date Created**: Date the section was created.
- **Description**: A brief description of the section.

### E-book
An e-book is a digital format of content that can be accessed and rated on any web-enabled device.

An e-book may have:
- **ID**: Unique identifier.
- **Name**: Title of the e-book.
- **Content**: The digital content of the e-book.
- **Author(s)**: The authors of the e-book.
- **Date Issued**: The date the e-book was issued.
- **Return Date**: The date by which the e-book should be returned.

## Core Functionalities

1. **Admin and User Login (RBAC)**
   - A login/register form for both librarian and user roles.
   - Implements role-based access control using either Flask security or JWT-based token authentication.
   - Differentiates all types of users using a suitable model.

2. **Librarian Dashboard**
   - Automatically adds the librarian whenever a new database is created.
   - Displays all relevant statistics (e.g., active users, grant requests, e-books issued, revoked, etc.).

3. **Section Management** (Librarian)
   - Create, update, and delete sections to categorize e-books by genre.

4. **E-book Management** (Librarian)
   - Create, edit, and delete e-books within a section.

5. **Search Functionality**
   - Allows users to search for e-books based on sections, authors, titles, etc.
   - Enables users to search for sections.

6. **General User Functionalities**
   - Request or return e-books (up to 5 at a time).
   - Access e-books for a specified period (e.g., 7 days).
   - Provide feedback for e-books.
   - Automatic or manual revoking of e-books based on the return period.

7. **Librarian Functionalities**
   - View all issue/return requests.
   - Grant or revoke e-books for users.
   - Monitor active users, grant requests, e-books issued, etc.

8. **Backend Jobs**
   - **Scheduled Daily Reminders**: Send daily reminders to users via Google Chat, SMS, or email.
   - **Monthly Activity Report**: Create a monthly report detailing sections and e-books issued, return dates, ratings, etc., and send via email.
   - **User-Triggered Async Job - Export as CSV**: Export details of issued/returned/granted e-books in CSV format.

9. **Performance and Caching**
   - Implement caching to enhance performance.
   - Set cache expiry to optimize API performance.

## Getting Started

To run this project locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/library-management-system-v2.git
