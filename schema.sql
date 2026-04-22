CREATE DATABASE library_database; 
USE library_database; 
 
CREATE TABLE Author ( 
    AuthorID INT PRIMARY KEY , 
    AuthorFirstName VARCHAR(50) NOT NULL, 
    AuthorLastName VARCHAR(50) NOT NULL, 
    AuthorNationality VARCHAR(50) 
); 
 
CREATE TABLE Book ( 
    BookID INT PRIMARY KEY , 
    BookTitle VARCHAR(100) NOT NULL, 
    AuthorID INT NOT NULL, 
    Genre VARCHAR(50) NOT NULL, 
    FOREIGN KEY (AuthorID) REFERENCES Author(AuthorID) 
); 
 
CREATE TABLE Client ( 
    ClientID INT PRIMARY KEY , 
    ClientFirstName VARCHAR(50) NOT NULL, 
    ClientLastName VARCHAR(50) NOT NULL, 
    ClientDOB DATE NOT NULL, 
    Occupation VARCHAR(50) 
); 
 
CREATE TABLE Borrower ( 
    BorrowID INT PRIMARY KEY , 
    ClientID INT NOT NULL, 
    BookID INT NOT NULL, 
    BorrowDate DATE NOT NULL, 
    FOREIGN KEY (ClientID) REFERENCES Client(ClientID), 
    FOREIGN KEY (BookID) REFERENCES Book(BookID) 
); 
 
-- Create index on ClientLastName for efficient searching 
CREATE INDEX idx_client_lastname ON Client (ClientLastName);