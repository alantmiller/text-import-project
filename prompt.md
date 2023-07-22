# Text File Processor

Please implement a `TextFileProcessor` class to process OCR extracted text files.

## Requirements

**Input Files**

- Extracted from specific input directory
- Named like `source-id-page.txt` 
- May contain optional title and created date

**Text Cleaning** 

- Remove leading and trailing whitespace
- Reduce extra spaces between words to single spaces
- Standardize line breaks to 2 lines between paragraphs   
- Fix word breaks like "c a t" into consolidated words 
- Handle common OCR errors and misspellings
- Try to parse title and date from files
  - Titles are often ALL CAPS on first line
  - Dates may be in formats like 08-27-1969 on last line
- Log any unparsable titles/dates to `processing_errors.log`

**Output**  

- Write cleaned text to output folder
- Use original filename with `.cleaned.txt` suffix

**Database (MariaDB and SQLAlchemy)**

- `sources` table:

    ```sql
    CREATE TABLE sources (
      id INT PRIMARY KEY AUTO_INCREMENT,
      source VARCHAR(100),
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )

    INSERT INTO sources (source) VALUES  
      ('Idle Thoughts'),  
      ('Dedication'),
      ('Memoirs')
    ```

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

**Code Quality**

- Modular OOP design 
- Robust error handling
- Unit tests
- Configurable logging
- Parallel processing 
- Comments

**Configuration** 

- JSON config file for DB/paths

Let me know if any requirements need clarification or expansion!
