-- Example business queries for the Library Operations Database

-- 1. List all books with their authors
SELECT
    b.BookID,
    b.BookTitle,
    CONCAT(a.AuthorFirstName, ' ', a.AuthorLastName) AS AuthorName,
    b.Genre
FROM Book b
JOIN Author a ON b.AuthorID = a.AuthorID
ORDER BY b.BookTitle;

-- 2. Show all borrowing records with client and book details
SELECT
    br.BorrowID,
    CONCAT(c.ClientFirstName, ' ', c.ClientLastName) AS ClientName,
    b.BookTitle,
    br.BorrowDate
FROM Borrower br
JOIN Client c ON br.ClientID = c.ClientID
JOIN Book b ON br.BookID = b.BookID
ORDER BY br.BorrowDate DESC;

-- 3. Count how many books exist in each genre
SELECT
    Genre,
    COUNT(*) AS TotalBooks
FROM Book
GROUP BY Genre
ORDER BY TotalBooks DESC, Genre ASC;

-- 4. Find the most frequently borrowed books
SELECT
    b.BookTitle,
    COUNT(*) AS BorrowCount
FROM Borrower br
JOIN Book b ON br.BookID = b.BookID
GROUP BY b.BookID, b.BookTitle
ORDER BY BorrowCount DESC, b.BookTitle ASC
LIMIT 10;

-- 5. Find the most active library clients
SELECT
    CONCAT(c.ClientFirstName, ' ', c.ClientLastName) AS ClientName,
    COUNT(*) AS TotalBorrowed
FROM Borrower br
JOIN Client c ON br.ClientID = c.ClientID
GROUP BY c.ClientID, c.ClientFirstName, c.ClientLastName
ORDER BY TotalBorrowed DESC, ClientName ASC
LIMIT 10;

-- 6. Show authors with the number of books in the catalog
SELECT
    CONCAT(a.AuthorFirstName, ' ', a.AuthorLastName) AS AuthorName,
    COUNT(*) AS TotalBooks
FROM Book b
JOIN Author a ON b.AuthorID = a.AuthorID
GROUP BY a.AuthorID, a.AuthorFirstName, a.AuthorLastName
ORDER BY TotalBooks DESC, AuthorName ASC;

-- 7. Find clients born after January 1, 2000
SELECT
    ClientID,
    ClientFirstName,
    ClientLastName,
    ClientDOB,
    Occupation
FROM Client
WHERE ClientDOB > '2000-01-01'
ORDER BY ClientDOB ASC;

-- 8. Count how many borrowing transactions happened per year
SELECT
    YEAR(BorrowDate) AS BorrowYear,
    COUNT(*) AS TotalTransactions
FROM Borrower
GROUP BY YEAR(BorrowDate)
ORDER BY BorrowYear ASC;

-- 9. Show all science books
SELECT
    BookID,
    BookTitle,
    Genre
FROM Book
WHERE Genre = 'Science'
ORDER BY BookTitle ASC;

-- 10. Find all books borrowed by a specific client ID
SELECT
    c.ClientID,
    CONCAT(c.ClientFirstName, ' ', c.ClientLastName) AS ClientName,
    b.BookTitle,
    br.BorrowDate
FROM Borrower br
JOIN Client c ON br.ClientID = c.ClientID
JOIN Book b ON br.BookID = b.BookID
WHERE c.ClientID = 35
ORDER BY br.BorrowDate DESC;
