# Import the necessary libraries
import os  # Provides functions for interacting with the operating system
import re  # Provides regular expression matching operations
import json  # Used for JSON manipulation
import mysql.connector  # Provides methods to connect to a MySQL database

class TextFileProcessor:
    """
    This class is used to process text files. It provides methods to read and clean files as well as
    inserting and updating records in a MySQL database.
    """

    def __init__(self, config_file, max_files=None):
        """
        Constructor for the 'TextFileProcessor' class.

        :param config_file: A string representing the path to the JSON file containing the database configuration.
        :param max_files: An integer representing the maximum number of files to process.
        """
        # Open and load the configuration file
        with open(config_file) as f:
            self.config = json.load(f)

        # Connect to the MySQL database
        self.connect_to_db()

        # Set the source and destination folders from the configuration file
        self.source_folder = self.config['folders']['source']
        self.dest_folder = self.config['folders']['destination']

        # Set the maximum number of files to process
        self.max_files = max_files

    def connect_to_db(self):
        """
        This method connects to a MySQL database using the configuration settings loaded from the configuration file.
        """
        try:
            self.mydb = mysql.connector.connect(
                host=self.config['db']['host'],
                user=self.config['db']['user'],
                password=self.config['db']['password'],
                database=self.config['db']['name']
            )

            # Create a cursor for executing SQL commands
            self.cursor = self.mydb.cursor()

        except mysql.connector.Error as err:
            print(f"Error connecting to the database: {err}")
            raise SystemExit

    def process_files(self):
        """
        This method processes all files in the source folder.
        """
        # Get a list of all files in the source folder
        file_list = os.listdir(self.source_folder)

        if file_list:
            total_files = len(file_list)

            # Iterate over all files in the source folder
            for count, file in enumerate(file_list, start=1):
                # If the number of processed files is greater than the maximum, stop processing
                if self.max_files and count > self.max_files:
                    print(f"Reached limit of {self.max_files} files")
                    break

                print(f"Starting: {file}\n")

                # Generate the full path of the file
                file_path = os.path.join(self.source_folder, file)

                # Extract metadata from the filename
                source_id, id, page_num = self.extract_metadata_from_filename(file)

                # Extract data from the file
                title, text, created_date = self.extract_data_from_file(file_path)

                # Clean the extracted text
                text = self.clean_data(text)

                # Write the cleaned text to a new file
                self.write_cleaned_file(file, text)

                # Prepare the data for insertion or update
                data = {
                    'source_id': source_id,
                    'id': id,
                    'page_num': page_num,
                    'title': title,
                    'text': text,
                    'created_date': created_date
                }

                # Insert or update the record in the database
                self.insert_or_update_record(data)

                print(f"Finished processing file {count} of {total_files}\n")

        else:
            print("No files found in the source directory.")

        # Close the database connection after all files have been processed
        self.close_db_connection()

    def extract_metadata_from_filename(self, file):
        """
        This method extracts metadata from a filename. It expects filenames in the format "source_id-id-page_num.txt".

        :param file: A string representing the filename to extract metadata from.
        :returns: A tuple containing the source_id, id, and page_num extracted from the filename.
        """
        match = re.match(r'(\d+)-(\d+)-(\d+)\.txt$', file)

        if not match:
            print(f"Filename '{file}' does not match expected format 'source_id-id-page_num.txt'. Skipping file.")
            return None, None, None

        return match.groups()

    def extract_data_from_file(self, file_path):
        """
        This method extracts data from a file. It expects files where the first line is the title
        and the last line is the created date.

        :param file_path: A string representing the full path of the file to extract data from.
        :returns: A tuple containing the title, raw text, and created date.
        """
        try:
            # Open and read the file
            with open(file_path) as f:
                text = f.read()

        except Exception as e:
            print(f"Could not read file {file_path}. Error: {str(e)}")
            return None, None, None

        # Extract the title and date from the text
        title, created_date = text.split('\n')[0], text.split('\n')[-1]

        return title, text, created_date

    def clean_data(self, raw_text):
        """
        This method cleans the extracted raw text data. It removes leading and trailing whitespaces,
        reduces multiple newlines to two, and reduces multiple whitespaces to one.

        :param raw_text: A string representing the raw text data to clean.
        :returns: A string representing the cleaned text data.
        """
        raw_text = raw_text.strip()

        raw_text = re.sub(r'\n{3,}', '\n\n', raw_text)
        raw_text = re.sub(r'\s{2,}', ' ', raw_text)

        return raw_text

    def insert_or_update_record(self, record_data):
        """
        This method inserts a new record or updates an existing one in the database.

        :param record_data: A dictionary containing the record data.
        """
        sql = """
        INSERT INTO records (source_id, id, title, text, page_num, created_date)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            title = VALUES(title),
            text = VALUES(text),
            page_num = VALUES(page_num),
            created_date = VALUES(created_date)
        """
        val = (record_data['source_id'], record_data['id'], record_data['title'], record_data['text'],
               record_data['page_num'], record_data['created_date'])

        try:
            self.cursor.execute(sql, val)
            self.mydb.commit()
        except mysql.connector.Error as err:
            print(f"Something went wrong with the SQL execution: {err}")

    def close_db_connection(self):
        """
        This method closes the connection to the MySQL database.
        """
        try:
            self.cursor.close()
            self.mydb.close()
            print("Database connection closed.")
        except mysql.connector.Error as err:
            print(f"Something went wrong when closing the database connection: {err}")
    
    def write_cleaned_file(self, file, text):
        """
        This method writes the cleaned text to a new file in the destination folder.

        :param file: A string representing the filename.
        :param text: A string representing the cleaned text.
        """
        cleaned_file = os.path.join(self.dest_folder, file)

        with open(cleaned_file, 'w') as f:
            f.write(text)



