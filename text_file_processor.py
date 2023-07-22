# Import the required libraries
import os
import re
import json
import mysql.connector

class TextFileProcessor:
    """Class to process text files and import data to a MySQL database."""

    def __init__(self, config):
        """Initialize TextFileProcessor with config data."""
        self.config = config
        self.mydb = self.connect_to_database()

    def connect_to_database(self):
        """Connect to the database and return the connection."""
        print("Connecting to database...")
        mydb = mysql.connector.connect(
            host=self.config['db']['host'],
            user=self.config['db']['user'],
            password=self.config['db']['password'],
            database=self.config['db']['name']
        )
        print("Connected!\n")
        return mydb

    def process_files(self):
        """Process files in the source directory and import data to the database."""
        cursor = self.mydb.cursor()
        print("Cursor created.\n")

        source_folder = self.config['folders']['source']
        dest_folder = self.config['folders']['destination']
        max_files_env = {'production': None, 'development': 50, 'staging': 100, 'testing': 20}
        max_files = max_files_env.get(self.config['environment'], 50)

        print("Processing files...")
        for count, file in enumerate(os.listdir(source_folder), start=1):
            if max_files and count > max_files:
                print(f"Reached limit of {max_files} files")
                break

            print(f"Starting: {file}\n")

            with open(os.path.join(source_folder, file)) as f:
                text = f.read()

            text = text.strip()

            print("Cleaning text...")
            text = re.sub(r'\n{3,}', '\n\n', text)
            text = re.sub(r'\s{2,}', ' ', text)

            print("Parsing filename...")
            filename = file.split('-')
            if len(filename) != 3 or not all(part.isdigit() for part in filename):
                print(f"Invalid filename: {file}. Skipping this file.")
                continue

            source_id, id, page_num = filename[0], filename[1], filename[2].split('.')[0]

            print("Extracting metadata...")
            title, created_date = text.split('\n')[0], text.split('\n')[-1]

            print(f"Processing: {file}\n")

            select_sql = "SELECT id FROM writings WHERE source_id = %s AND id = %s"
            cursor.execute(select_sql, (source_id, id))

            if cursor.fetchone() is None:
                print("Inserting to database...")
                sql = "INSERT INTO writings (source_id, id, title, body, page_num, created_date) VALUES (%s, %s, %s, %s, %s, %s)"     
                values = (source_id, id, title, text, page_num, created_date)
                cursor.execute(sql, values)
                print("Inserted to database!\n")
            else:
                print("Updating record...")
                update_sql = "UPDATE writings SET title = %s, body = %s, page_num = %s, created_date = %s WHERE source_id = %s AND id = %s"
                cursor.execute(update_sql, (title, text, page_num, created_date, source_id, id))
                print("Record updated!\n")

            self.mydb.commit()

            print("Writing clean file...")
            cleaned_file = os.path.join(dest_folder, file)
            with open(cleaned_file, 'w') as f:
                f.write(text)

            print(f"Wrote to {cleaned_file}\n")

        cursor.close()
        print("Cursor closed.\n")

    def close(self):
        """Close the database connection."""
        self.mydb.close()
        print("Database closed.\n")


if __name__ == "__main__":
    # Load config file
    with open('config.import.json') as f:
        config = json.load(f)

    processor = TextFileProcessor(config)
    processor.process_files()
    processor.close()

    print("Import complete!")
