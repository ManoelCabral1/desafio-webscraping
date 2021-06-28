COPY books (category, name, stars, price, in_stock)
FROM '/home/manoel/DevPython/web scraping/consolidate_book_data.csv' 
WITH
DELIMITER ',' 
CSV HEADER;