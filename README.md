# Address-Validation-Python-Script
This script fetches the latest 'OrderCities' and 'OrderZip' from a database, then queries a second database using 'OrderZip' to get a list of names. It applies fuzzy matching to find the closest match to 'OrderCities' in this list, defaulting to the first name if no close match exists.
