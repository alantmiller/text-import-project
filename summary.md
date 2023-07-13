# Import Text Files Project

## Requirements

- Import text files into MySQL database
- Text files named like ##-##-##.txt
  - First part is source ID
  - Second part is unique writing ID
  - Third part is page number
- Database table fields:
  - id - Primary key
  - source_id - Reference to source
  - title - Title extracted from text
  - body - Main text content
  - page_num - Page number from filename
  - created_date - Date extracted from text
- Parse filename to get source_id, id, page_num
- Clean up text formatting during import
- Extract title and created_date from text
- Handle cases where title/date are missing

## Implementation

- Python script processes files
  - Detailed comments explaining logic
  - Parse filename into variables
  - Clean text, extract title & date
  - Insert into database
- Laravel job class dispatches importer service
  - Executes python script
  - Passes database credentials config
- Log progress, failures, etc

## Database Schema

```
-- Raw SQL
CREATE TABLE writings (
  id INT PRIMARY KEY AUTO_INCREMENT,
  source_id INT, 
  title VARCHAR(255),
  body TEXT,
  page_num INT,
  created_date DATE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```