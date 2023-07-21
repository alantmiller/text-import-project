# Import the modules needed
import os # Provides functions for working with files and folders
import re # Used for regular expressions to find/replace text
import mysql.connector # Database connector for MySQL
import json

# Load config file
with open('config.import.json') as f:
  config = json.load(f)

# Database credentials from config  
db_host = config['db']['host']
db_user = config['db']['user']
db_pass = config['db']['password']
db_name = config['db']['name']

environment = config['environment']

  # Set max files based on environment
  if environment == 'production':
    max_files = None 
  else:
    if environment == 'development':
      max_files = 50
    elif environment == 'staging':  
      max_files = 100
    elif environment == 'testing':
      max_files = 20
    else:
      max_files = 50

# Connect to the database 
# Replace with your real connection settings
print("Connecting to database...")
mydb = mysql.connector.connect(
  host=db_host,
  user=db_user,
  password=db_pass,
  database=db_name
)
print("Connected!\n")

# Create a cursor to execute SQL commands
cursor = mydb.cursor()
print("Cursor created.\n")

# Set source and destination folders
source_folder = config['folders']['source'] 
dest_folder = config['folders']['destination']

# Loop through files
count = 0

# Loop through all text files in source folder
print("Processing files...")
for file in os.listdir(source_folder):

  count += 1
  
    # Check if hit limit
  if count >= max_files:
    print(f"Reached limit of {max_files} files") 
    break

  # Print filename we are starting
  print(f"Starting: {file}\n")

  # Open file and read text
  print("Opening file...")
  with open(os.path.join(source_folder, file)) as f:
    text = f.read()

 # Trim whitespace  
  text = text.strip()

  # Clean text formatting
  print("Cleaning text...")
  text = re.sub(r'\n{3,}', '\n\n', text)
  text = re.sub(r'\s{2,}', ' ', text)

  # Parse filename into variables
  print("Parsing filename...")
  filename = file.split('-')
  source_id = filename[0]
  id = filename[1] 
  page_num = filename[2].split('.')[0]

  # Extract title and date
  print("Extracting metadata...")
  title = text.split('\n')[0]
  created_date = text.split('\n')[-1]

  # Print progress 
  print(f"Processing: {file}\n")

  # Check if record exists
select_sql = "SELECT id FROM writings WHERE source_id = %s AND id = %s"
cursor.execute(select_sql, (source_id, id))

  # Insert record into database
  print("Inserting to database...")
  sql = "INSERT INTO writings (source_id, id, title, body, page_num, created_date)
           VALUES (%s, %s, %s, %s, %s, %s)"
           
  values = (source_id, id, title, text, page_num, created_date)

  cursor.execute(sql, values)

  print("Inserted to database!\n")

  mydb.commit()

  # Write clean text to new file
  print("Writing clean file...")
  cleaned_file = os.path.join(dest_folder, file)
  with open(cleaned_file, 'w') as f:
     f.write(text)

  print(f"Wrote to {cleaned_file}\n")

# Close database 
mydb.close()
print("Database closed.\n")

print("Import complete!")
