"Please rewrite and implement the TextFileProcessor class provided previously to process text files extracted from a document storage system.

The requirements are:

The system extracts thousands of text files daily from documents, named like 'source-docid-page.txt'

Each file contains a title on the first line, text contents, and a created date on the last line

The files need to be processed to clean the text, extract metadata, and insert into a SQL database

The database contains a table 'documents' with columns:

id INT primary key
source VARCHAR(100)
title VARCHAR(255)
contents TEXT
page INT
created_date DATETIME
After processing, the cleaned text should be written to an 'output' folder

The code needs to be production-ready with proper error handling, logging, and optimizations

Unit tests should be written to validate key functionality

Please provide a refactored implementation of the TextFileProcessor class and associated functions that follows best practices and fits these requirements. Explain your design decisions and tradeoffs. Annotate areas you would improve given more time.

The full code should:

Have proper OOP design and type annotations
Use SQLAlchemy for database access
Include input validation and robust error handling
Have configurable logging
Be modular and reusable
Include unit tests for key functions
Process files in parallel for efficiency
Be well commented for maintainability
