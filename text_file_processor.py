import os
import re
import mysql.connector
import json

class TextFileProcessor:
    """
    Class for processing text files. Handles reading and cleaning the files, as well as inserting and updating records in the database.
    """

    def __init__(self, config_file):
        """
        Construct a new 'TextFileProcessor' object.

        :param config_file: The path to a JSON file containing the database and file configuration
        """
        # Load the configuration from the specified file
        with open(config_file) as f:
            self.config = json.load(f)

        # Connect to the database
        self.mydb = mysql.connector.connect(
            host=self.config['db']['host'],
            user=self.config['db']['user'],
            password=self.config['db']['password'],
            database=self.config['db']['name']
        )

        # Create a cursor for executing SQL commands
        self.cursor = self.mydb.cursor()

        # Set the source and destination folders from the config
        self.source_folder = self.config['folders']['source']
        self.dest_folder = self.config['folders']['destination']

    def process_files(self):
        """
        Process all files in the source folder: reading and cleaning the text and handling the database records.
        """
        # Loop through all text files in source folder
        for count, file in enumerate(os.listdir(self.source_folder), start=1):

            # Check if hit limit, if one is specified in the config
            if 'max_files' in self.config and count > self.config['max_files']:
                break

            # Open the file and read the text
            with open(os.path.join(self.source_folder, file)) as f:
                text = f.read()

            # Clean the text formatting
            text = self.clean_text(text)

            # Parse the filename into the necessary variables
            source_id, id, page_num = self.parse_filename(file)

            # Extract the title and date from the text
            title, created_date = self.extract_metadata(text)

            # Check if a corresponding record exists in the database and handle accordingly
            self.handle_database_record(source_id, id, title, text, page_num, created_date)

            # Write the cleaned text to a new file in the destination folder
            self.write_clean_file(file, text)

        # Close the database cursor once all files have been processed
        self.cursor.close()

    def clean_text(self, text):
        """
        Clean the provided text by stripping leading/trailing whitespace and fixing formatting.

        :param text: The original text
        :return: The cleaned text
        """
        text = text.strip()
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r'\s{2,}', ' ', text)
        return text

    def parse_filename(self, file):
        """
        Parse the provided filename into the necessary variables.

        :param file: The filename
        :return: A tuple containing the source_id, id, and page_num
        """
        filename = file.split('-')
        source_id, id, page_num = filename[0], filename[1], filename[2].split('.')[0]
        return source_id, id, page_num

    def extract_metadata(self, text):
        """
        Extract the title and date from the provided text.

        :param text: The cleaned text
        :return: A tuple containing the title and date
        """
        title, created_date = text.split('\n')[0], text.split('\n')[-1]
        return title, created_date

    def handle_database_record(self, source_id, id, title, text, page_num, created_date):
        """
        Check if a corresponding record exists in the database. If it does, update it, if not, insert a new record.

        :param source_id: The source id
        :param id: The id
        :param title: The title
        :param text: The cleaned text
        :param page_num: The page number
        :param created_date: The creation date
        """
        select_sql = "SELECT id FROM writings WHERE source_id = %s AND id = %s"
        self.cursor.execute(select_sql, (source_id, id))
        
        if self.cursor.fetchone() is None:
            # If no record is found, then insert the new record
            insert_sql = "INSERT INTO writings (source_id, id, title, body, page_num, created_date) VALUES (%s, %s, %s, %s, %s, %s)"
            self.cursor.execute(insert_sql, (source_id, id, title, text, page_num, created_date))
            self.mydb.commit()
        else:
            # If a record is found, update it
            update_sql = "UPDATE writings SET title = %s, body = %s, page_num = %s, created_date = %s WHERE source_id = %s AND id = %s"
            self.cursor.execute(update_sql, (title, text, page_num, created_date, source_id, id))
            self.mydb.commit()

    def write_clean_file(self, file, text):
        """
        Write the cleaned text to a new file in the destination folder.

        :param file: The filename
        :param text: The cleaned text
        """
        cleaned_file = os.path.join(self.dest_folder, file)
        with open(cleaned_file, 'w') as f:
            f.write(text)
