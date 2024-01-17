import pyodbc
from fuzzywuzzy import fuzz

# Function to perform fuzzy matching
def best_fuzzy_match(target_word, word_list):
    best_match = None
    highest_score = 0

    for word in word_list:
        score = fuzz.ratio(target_word, word)
        if score > highest_score:
            highest_score = score
            best_match = word

    return best_match, highest_score

# Function to connect to a database and execute a query
def execute_query(connection_string, sql_query):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# First database connection and query
conn_str_first = (
    "Driver={SQL Server Native Client 11.0};"
    "Server=MICHGSQL16;"
    "Database=MOHAWKRPA;"
    "UID=MohawkRPA;"
    "PWD=XnWMtmD794;"
)
sql_first = """
SELECT TOP 1 OrderCities, OrderZip
FROM [MOHAWKRPA].[dbo].[Address_Validation_Bot]
ORDER BY CONVERT(datetime, PushedTimestamp) DESC
"""
result_first = execute_query(conn_str_first, sql_first)
order_zip, order_cities = (result_first[0][1], result_first[0][0]) if result_first else (None, None)

if order_zip:
    print("OrderZip:", order_zip)

    # Second database connection and query using the OrderZip
    conn_str_second = 'Driver={IBM i Access ODBC Driver};System=ASCSEQUEL.MOHAWKIND.COM; DataSource=Mohawk1;UID=E229540;PWD=orange59;CONNTYPE=2;'
    sql_second = f"SELECT STGCNM FROM \"VSTAX.D\".VTSXRFL5 WHERE STGCZP = '{order_zip}'"
    result_second = execute_query(conn_str_second, sql_second)

    # Process result for fuzzy matching
    words_from_db = [item[0].strip() for item in result_second if item[0]]

    # Print options from the second query
    print("Options from the second query:", words_from_db)

    # Perform fuzzy matching
    best_match, score = best_fuzzy_match(order_cities, words_from_db)
    print(f"Best fuzzy match for '{order_cities}': {best_match} with a score of {score}")
else:
    print("No data found in the first query")
