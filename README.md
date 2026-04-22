# Library Operations Database

## Overview

Library Operations Database is a SQL project that models the core data layer for a library system. It includes a relational schema for authors, books, clients, and borrowing records, along with seed data and example business queries.

This repository was cleaned up from a PDF-only submission and converted into runnable SQL scripts so it is easier to review, run, and extend.

## Real-World Business Use Case

This project maps to a real library or school media center workflow.

A library needs to answer questions such as:

- Which books are currently in the catalog?
- Which author wrote each book?
- Which clients borrow books most often?
- What genres are most common?
- How many borrowing transactions happened in a given year?

A structured relational database makes these operations reliable and searchable. This kind of schema could support a school library portal, a community library system, or the back end for a book circulation dashboard.

## Repository Files

- `schema.sql` - creates the database, tables, relationships, and index
- `seed_data.sql` - loads sample records for authors, books, clients, and borrowing transactions
- `queries.sql` - example business queries for reporting and analysis
- `DataBase Data.docx.pdf` - original project source document
- `README.md` - project explanation and run instructions

## Database Schema

The project defines four core tables:

1. `Author`
   - `AuthorID`
   - `AuthorFirstName`
   - `AuthorLastName`
   - `AuthorNationality`

2. `Book`
   - `BookID`
   - `BookTitle`
   - `AuthorID`
   - `Genre`

3. `Client`
   - `ClientID`
   - `ClientFirstName`
   - `ClientLastName`
   - `ClientDOB`
   - `Occupation`

4. `Borrower`
   - `BorrowID`
   - `ClientID`
   - `BookID`
   - `BorrowDate`

Relationships:
- Each `Book` belongs to one `Author`
- Each `Borrower` record links one `Client` to one `Book`

## Key Features

- Relational schema with primary keys and foreign keys
- Borrowing transaction model
- Search optimization with an index on client last name
- Large sample dataset for testing and reporting
- Example SQL queries for business analysis

## Recommended Environment

This project is written in SQL syntax that fits MySQL or MariaDB best because it uses:

- `CREATE DATABASE`
- `USE library_database`
- `YEAR(...)`
- `LIMIT`

## How to Run the Project

### Option 1: MySQL command line

From the repository folder, run:

```powershell
mysql -u root -p < schema.sql
mysql -u root -p library_database < seed_data.sql
mysql -u root -p library_database < queries.sql
```

### Option 2: MySQL Workbench or another SQL IDE

1. Open `schema.sql` and run it
2. Open `seed_data.sql` and run it
3. Open `queries.sql` and run it
4. Review the query results

## Example Questions This Database Can Answer

- What are the most frequently borrowed books?
- Which clients borrow the most items?
- How many books are in each genre?
- Which authors have multiple books in the catalog?
- How many transactions happened each year?

## Suggested Professional Positioning

A stronger business-facing name for this project is:

**Library Operations Database**

This sounds more practical and recruiter-friendly than a classroom-style title.

## Future Improvements

- Add a `ReturnDate` field to track book returns
- Add a `Staff` table for librarians or administrators
- Add a `Branch` table for multi-location libraries
- Add stored procedures for common workflows
- Add views for reporting dashboards
- Add constraints for available inventory counts

## Source Note

The original SQL content came from the PDF included in this repository and was reorganized into runnable scripts for easier execution and review.
