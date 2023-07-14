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




## notes: 

The database table's name will be "writings" and contain the fields id, title, body, created_date, created_at, and updated_at. The created_at and update_at are standard fare in the Laravel framework which will be used for this project. When creating the database please keep Laravel's standards in mind. 

When formatting each file's contents please keep in mind the following...

1. Line breaks need to be fixed and formatted.

2. Many words have a space between each character where they should not, please fix those.
   

When coming up with the contents of each database field, keep in mind the following...

1. Typically the Title will be on the top of the file in all caps, if such a title exists, please use that for the title, otherwise just use "Unknown" for the title field.

2. The created_date is usually the last line in a writing, sometimes it's missing, in the case that a created_date does not exist just insert a null charachter in the database.

As for the python script, please include very descriptive comments about what you're doing at any given moment.

Also, I want to see the progress as the script proceeds, ultimately if I run this script in the background, I'll be sending the output via some yet to be known Javascript framework, probably Alpine.
