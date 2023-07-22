# Import the modules needed
import os  # Provides functions for working with files and folders
import re  # Used for regular expressions to find/replace text
import mysql.connector  # Database connector for MySQL
import json  # Provides JSON encoder and decoder

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
    Process all files in the source folder.

    Returns
    -------
    None
    """
    # Get list of files in source folder
    file_list = self.get_file_list()

    # Loop through all files in source folder
    for count, file in enumerate(file_list, start=1):  # enumerate gives us automatic counting

        # Check if hit limit
        if self.max_files and count > self.max_files:  # checking if max_files is not None before comparing
            print(f"Reached limit of {self.max_files} files")
            break

        # Print filename we are starting
        print(f"Starting: {file}\n")

        # Get full file path
        file_path = os.path.join(self.source_folder, file)

        # Process individual file
        self.process_file(file, file_path)


def process_file(self, file_name, file_path):
    """
    Process a single file.

    Parameters
    ----------
    file_name : str
        a string representing the name of the file to process
    file_path : str
        a string representing the path of the file to process

    Returns
    -------
    None
    """
    # Parse filename into variables
    source_id, id, page_num = self.parse_filename(file_name)

    # Extract data from file
    title, text, created_date = self.extract_data_from_file(file_path)

    # Check if record exists
    exists = self.check_record_exists(source_id, id)

    if not exists:
        # Record does not exist, insert it
        self.insert_record(source_id, id, title, text, page_num, created_date)
    else:
        # Record exists, update it
        self.update_record(source_id, id, title, text, page_num, created_date)

    # Write clean text to new file
    self.write_clean_file(file_name, text)


def is_valid_filename(self, file):
    """
    Validate the file name.

    Parameters
    ----------
    file : str
        a string representing the name of the file to validate

    Returns
    -------
    bool
        True if the filename is valid, False otherwise
    """
    # The filename is expected to be in the format: source_id-id-page_num.txt
    match = re.fullmatch(r'\d{2}-\d{3}-\d{3}\.txt', file)
    return match is not None

    
def extract_metadata_from_filename(self, file):
    """
    Extract metadata from the filename.

    Parameters
    ----------
    file : str
        a string representing the name of the file to extract metadata from

    Returns
    -------
    tuple
        a tuple containing the source_id, id, and page_num extracted from the filename
    """
    # The filename is expected to be in the format: source_id-id-page_num.txt
    parts = file.split('-')
    source_id, id, page_num = parts[0], parts[1], parts[2].split('.')[0]
    return source_id, id, page_num

def extract_data_from_file(self, file_path):
    """
    Extract data from the file.

    Parameters
    ----------
    file_path : str
        a string representing the path of the file to extract data from

    Returns
    -------
    tuple
        a tuple containing the title, cleaned text and created date
    """
    # Open file and read text
    with open(file_path) as f:
        text = f.read()

    # Strip leading and trailing whitespace
    text = text.strip()

    # Clean text formatting
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'\s{2,}', ' ', text)

    # Extract title and date
    title, created_date = text.split('\n')[0], text.split('\n')[-1]

    return title, text, created_date


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
