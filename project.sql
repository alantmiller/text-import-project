-- Raw SQL
CREATE TABLE writings (
  id INT AUTO_INCREMENT PRIMARY KEY,
  source_id INT,
  title VARCHAR(255), 
  body TEXT,
  page_num INT NULL, 
  created_date DATE NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create table
CREATE TABLE sources (
  id INT AUTO_INCREMENT PRIMARY KEY,
  source VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Populate data
INSERT INTO sources (id, source)
VALUES
  (1, "Idle Thoughts"),
  (2, "Memoirs"), 
  (4, "My Dedication");
