# Import the necessary classes and modules
from src.text_file_processor import TextFileProcessor
import json

def main():
    # Load configuration file
    with open('config/config_development.json') as f:
        config = json.load(f)
    
    # Extract configuration variables
    source_folder = config['folders']['source'] 
    dest_folder = config['folders']['destination']
    max_files = config['max_files']

    # Create an instance of TextFileProcessor
    processor = TextFileProcessor(source_folder, dest_folder, max_files)

    # Process files
    processor.process_files()

# If this script is run directly (not imported), call the main function
if __name__ == "__main__":
    main()
