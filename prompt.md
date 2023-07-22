Please rewrite and implement the TextFileProcessor class provided previously to process text files extracted from a document storage system. 

The requirements are:

- The system extracts text files from specific documents, named like `source-docid-page.txt`

- Each file may contain a title on the first line and/or a created date on the last line, but these are not guaranteed to exist

- The files need to be processed to clean the text, extract metadata, and insert into a MariaDB SQL database

- The database contains tables:

    - `writings` table:

        ```sql
        CREATE TABLE writings (
          id INT PRIMARY KEY AUTO_INCREMENT,
          source_id VARCHAR(100),
          title VARCHAR(255), 
          body TEXT,
          created_date DATETIME, 
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        ```

    - `sources` table:  

        ```sql
         CREATE TABLE sources (
           id INT PRIMARY KEY AUTO_INCREMENT,
           source VARCHAR(100),
           created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
           updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  
         )
        ```

- After processing, the cleaned text should be written to an `output` folder  

- The code needs to be production-ready with:

    - Proper OOP design and type annotations
    - Use SQLAlchemy for database access because it provides an ORM that abstracts away SQL details and enables easier testing
    - Input validation and robust error handling
    - Configurable logging
    - Modular and reusable code
    - Unit tests for key functions
    - Parallel processing for efficiency
    - Well commented for maintainability
