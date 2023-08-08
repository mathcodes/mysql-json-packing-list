# optimized by:
# Reusign the connect_to_db Function: Reused the connect_to_db function instead of a separate connection in list_all_items.
# Refactoring Table Name Determination: Created a separate function to determine the table name based on the item type. This removes redundancy across the functions.
# Refactoring Query Execution: Created a common function to execute queries that can be used across multiple functions.

import mysql.connector
import json
def read_json_file():
    with open('data.json', 'r') as file:
        data = json.load(file)
    return data


def connect_to_db():
    return mysql.connector.connect(user='root', password='', host='localhost', database='PackingWithJSON')


def read_json_file():
    with open('data.json', 'r') as file:
        data = json.load(file)
    return data


def write_json_file(data):
    with open('./PackingWithJSON/data.json', 'w') as file:
        json.dump(data, file)


def get_table_name(item_type):
    tables = {'personal': 'personal_items', 'household': 'household_items', 'work': 'work_essentials'}
    return tables.get(item_type, None)


def execute_query(connection, query, values=None):
    cursor = connection.cursor()
    if values:
        cursor.execute(query, values)
    else:
        cursor.execute(query)
    connection.commit()
    cursor.close()


# create_item function
def create_item(item_type, item_name, quantity, colors, importance, complete):
    table_name = get_table_name(item_type)
    if table_name is None:
        print("Invalid item_type provided. Must be 'personal', 'household', or 'work'.")
        return

    query = f"INSERT INTO {table_name} (type, item_name, quantity, colors, importance, complete) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (item_type, item_name, quantity, colors, importance, complete)

    connection = connect_to_db()
    execute_query(connection, query, values)
    connection.close()


# Remaining functions can use similar refactoring based on the above approach

def read_item(item_type, item_name):
    table_name = get_table_name(item_type)
    if table_name is None:
        print("Invalid item_type provided. Must be 'personal', 'household', or 'work'.")
        return None, None

    query = f"SELECT * FROM {table_name} WHERE item_name = %s"
    values = (item_name,)

    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute(query, values)
    result = cursor.fetchall()

    json_result = []
    for row in result:
        json_result.append({
            'id': row[0],
            'type': row[1],
            'item_name': row[2],
            'quantity': row[3],
            'colors': row[4],
            'importance': row[5],
            'complete': row[6]
        })

    cursor.close()
    connection.close()

    return result, json_result


def update_data(item_type, item_name, quantity=None, colors=None, importance=None, complete=None):
    table_name = get_table_name(item_type)
    if table_name is None:
        print("Invalid item_type provided. Must be 'personal', 'household', or 'work'.")
        return

    update_parts = []
    values = []
    if quantity is not None:
        update_parts.append("quantity = %s")
        values.append(quantity)
    if colors is not None:
        update_parts.append("colors = %s")
        values.append(colors)
    if importance is not None:
        update_parts.append("importance = %s")
        values.append(importance)
    if complete is not None:
        update_parts.append("complete = %s")
        values.append(complete)

    values.append(item_name)
    update_query = f"UPDATE {table_name} SET {', '.join(update_parts)} WHERE item_name = %s"

    connection = connect_to_db()
    execute_query(connection, update_query, tuple(values))
    connection.close()

def delete_item(item_type, item_name):
    table_name = get_table_name(item_type)
    if table_name is None:
        print("Invalid item_type provided. Must be 'personal', 'household', or 'work'.")
        return

    delete_query = f"DELETE FROM {table_name} WHERE item_name = %s"
    values = (item_name,)

    connection = connect_to_db()
    execute_query(connection, delete_query, values)
    connection.close()


def list_all_items():
    connection = connect_to_db()
    cursor = connection.cursor()

    items = {
        'personal_items': [],
        'household_items': [],
        'work_essentials': []
    }

    tables = ['personal_items', 'household_items', 'work_essentials']

    for table in tables:
        cursor.execute(f"SELECT * FROM {table}")
        result = cursor.fetchall()

        # Processing code here
        for row in result:
            item = {
                'item_type': row[1],  # Assuming item_type is in the second column
                'item_name': row[2],  # Assuming item_name is in the third column
                'quantity': row[3],   # Assuming quantity is in the fourth column
                'colors': row[4],     # Assuming colors is in the fifth column
                'importance': row[5],  # Assuming importance is in the sixth column
                'complete': row[6]    # Assuming complete is in the seventh column
            }
            items[table].append(item)

    cursor.close()
    connection.close()

    return items

