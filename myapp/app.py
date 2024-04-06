from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)
app.debug = True
port = 8085

def fetch_mytable():
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

        # Check if the table exists, and create it if not
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS myapp (
                id INT AUTO_INCREMENT PRIMARY KEY,
                data VARCHAR(255)
            )
        """)

        # Check if the table is empty
        cursor.execute("SELECT COUNT(*) FROM myapp")
        table_count = cursor.fetchone()[0]

        # If table is empty, add text into data column
        if table_count == 0:
            cursor.execute("INSERT INTO myapp (data) VALUES (%s)", ("Welcome to ilandia!",))
            mydb.commit()  # Commit the transaction

        # Fetch all rows from the myapp table
        cursor.execute("SELECT * FROM myapp")

        # Fetch all rows
        rows = cursor.fetchall()

        # Close the connection
        cursor.close()
        mydb.close()

        # Return the rows
        return rows

    except mysql.connector.Error as error:
        return {"error": str(error)}

def fetch_message(id):
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

        # Fetch the specific row by ID
        cursor.execute("SELECT * FROM myapp WHERE id = %s", (id,))
        row = cursor.fetchone()

        # Close the connection
        cursor.close()
        mydb.close()

        # Return the row
        return row

    except mysql.connector.Error as error:
        return {"error": str(error)}

# GET method
@app.route('/')
def index():
    # Fetch all messages from MySQL
    messages = fetch_mytable()
    # Return all messages
    return jsonify(messages)

@app.route('/<int:id>')
def get_message(id):
    # Fetch a specific message from MySQL based on ID
    message = fetch_message(id)
    if message:
        # Return the message if found
        return jsonify(message)
    else:
        # Return a 404 error if message with specified ID not found
        return jsonify({"error": "No data for this row"}), 404

# POST method
@app.route('/add', methods=['POST'])
def add_data():
    try:
        # Get data from the request body
        data = request.json.get('data')

        if not data:
            return jsonify({"error": "No data provided"})

        # Connect to MySQL
        mydb = mysql.connector.connect(
            host="mysql",
            user="root",
            password="ilandev",
            database="mydb"
        )

        # Create a cursor object
        cursor = mydb.cursor()

        # Fetch the maximum ID from the myapp table
        cursor.execute("SELECT MAX(id) FROM myapp")
        max_id = cursor.fetchone()[0]

        # Calculate the next ID
        new_id = max_id + 1 if max_id else 1

        # Insert new data into the myapp table
        cursor.execute("INSERT INTO myapp (id, data) VALUES (%s, %s)", (new_id, data))
        mydb.commit()  # Commit the transaction

        # Close the connection
        cursor.close()
        mydb.close()

        return jsonify({"message": "Data added successfully", "id": new_id})

    except mysql.connector.Error as error:
        return jsonify({"error": str(error)})

# DELETE method
@app.route('/<int:id>', methods=['DELETE'])
def delete_message(id):
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

        # Delete the message with the specified ID
        cursor.execute("DELETE FROM myapp WHERE id = %s", (id,))
        mydb.commit()  # Commit the transaction

        # Close the connection
        cursor.close()
        mydb.close()

        return jsonify({"message": "Message deleted successfully"})

    except mysql.connector.Error as error:
        return jsonify({"error": str(error)})

if __name__ == '__main__':
    # Run Flask server with hostname and port
    app.run(host='0.0.0.0', port=port)