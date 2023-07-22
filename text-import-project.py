# Import the modules needed
import os  # Provides functions for working with files and folders
import re  # Used for regular expressions to find/replace text
import mysql.connector  # Database connector for MySQL
import json  # Provides JSON encoder and decoder

# Load config file
with open('config.import.json') as f:
    config = json.load(f)

environment = config['environment']

# A dictionary to store the max_files limit for each environment
# Instead of a chain of if/elif conditions, this dictionary makes the code cleaner and more efficient
max_files_env = {
    'production': None,
    'development': 50,
    'staging': 100,
    'testing': 20
}

# Get max_files based on the environment
max_files = max_files_env.get(environment, 50)  # If the environment is not found, use 50 as a default

try:
    # Connect to the database 
    print("Connecting to database...")
    mydb = mysql.connector.connect(
        host=config['db']['host'],
        user=config['db']['user'],
        password=config['db']['password'],
        database=config['db']['name']
    )
    print("Connected!\n")

    # Create a cursor to execute SQL commands
    cursor = mydb.cursor()
    print("Cursor created.\n")

    # Set source and destination folders
    source_folder = config['folders']['source'] 
    dest_folder = config['folders']['destination']

    # Loop through all text files in source folder
    print("Processing files...")
    for count, file in enumerate(os.listdir(source_folder), start=1):  # enumerate gives us automatic counting

        # Check if hit limit
        if max_files and count > max_files:  # checking if max_files is not None before comparing
            print(f"Reached limit of {max_files} files") 
            break

        # Print filename we are starting
        print(f"Starting: {file}\n")

        # Open file and read text
        print("Opening file...")
        with open(os.path.join(source_folder, file)) as f:
            text = f.read()

        # Strip leading and trailing whitespace
        text = text.strip()

        # Clean text formatting
        print("Cleaning text...")
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r'\s{2,}', ' ', text)

        # Parse filename into variables
        print("Parsing filename...")
        filename = file.split('-')
        if len(filename) != 3:  # Expecting three parts after splitting by '-'
            print(f"Unexpected filename format: {file}. Skipping this file.")
            continue

        # Check if parts are numeric and have the expected lengths
        if not(filename[0].isdigit() and len(filename[0]) == 2 and
               filename[1].isdigit() and len(filename[1]) == 3 and
               filename[2].split('.')[0].isdigit() and len(filename[2].split('.')[0]) == 3):
            print(f"Filename parts are not numeric or have incorrect length: {file}. Skipping this file.")
            continue

        # Proceed with extraction only if the filename format is 
        # correct and parts are numeric with expected lengths
        source_id, id, page_num = filename[0], filename[1], filename[2].split('.')[0]  # direct assignments

        # Extract title and date
        print("Extracting metadata...")
        title, created_date = text.split('\n')[0], text.split('\n')[-1]  # direct assignments

        # Print progress 
        print(f"Processing: {file}\n")

        # Check if record exists
        select_sql = "SELECT id FROM writings WHERE source_id = %s AND id = %s"
        cursor.execute(select_sql, (source_id, id))

        if cursor.fetchone() is None:  # If no record is found, then insert the new record

            # Insert record into database
            print("Inserting to database...")
            sql = "INSERT INTO writings (source_id, id, title, body, page_num, created_date) VALUES (%s, %s, %s, %s, %s, %s)"     
            values = (source_id, id, title, text, page_num, created_date)
            cursor.execute(sql, values)
            print("Inserted to database!\n")
            mydb.commit()

        else:
            # Record exists, update it
            print("Updating record...")
            update_sql = """
            UPDATE writings
            SET title = %s, body = %s, page_num = %s, created_date = %s
            WHERE source_id = %s AND id = %s
            """
            
            cursor.execute(update_sql, (title, text, page_num, created_date, source_id, id))
            print("Record updated!\n")
            mydb.commit()
            
        # Write clean text to new file
        print("Writing clean file...")
        cleaned_file = os.path.join(dest_folder, file)
        with open(cleaned_file, 'w') as f:
            f.write(text)

        print(f"Wrote to {cleaned_file}\n")

    # Close the cursor
    cursor.close()
    print("Cursor closed.\n")

    # Close database 
    mydb.close()
    print("Database closed.\n")

except mysql.connector.Error as err:
    print(f"Something went wrong: {err}")  # If any error occurs during database operations, catch it and print it

print("Import complete!")
