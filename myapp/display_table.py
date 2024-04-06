import mysql.connector

try:
    # Connect to MySQL
    mydb = mysql.connector.connect(
        host="mysql",
        user="root",
        password="ilandev",
        database="mydb"
    )

    # Create a cursor object
    cursor = mydb.cursor()

    # Execute a query to select all rows from the table
    cursor.execute("SELECT * FROM myapp")

    # Fetch all rows
    rows = cursor.fetchall()

    # Print the table header
    print("ID\tData")

    # Print each row
    for row in rows:
        print(f"{row[0]}\t{row[1]}")

except mysql.connector.Error as error:
    print("Error:", error)

finally:
    # Close the connection
    if 'mydb' in locals() and mydb.is_connected():
        cursor.close()
        mydb.close()