import sqlite3


def get_connection(ds, entity, name):
    query = f"Select from {entity} where name = '{name}'"
    result_map = {}
    try:
        connection = ds.connect()
        pointer = connection.cursor()
        pointer.execute(query)
        columns = [desc[0] for desc in pointer.description]
        for row in pointer.fetchall():
            result_map = {columns[i]: row[i] for i in range(len(columns))}
    except sqlite3.Error as error:
        print(error)
        raise SystemExit(0)
    finally:
        connection.close()
    return result_map


def get_data():
    sql_data = {}
    ds = sqlite3.connect('Dungeon_Data.db')
    try:
        sql_data["Warrior"] = get_connection(ds, "Hero", "Warrior")
        sql_data["Priestess"] = get_connection(ds, "Hero", "Priestess")
        sql_data["Thief"] = get_connection(ds, "Hero", "Thief")
        sql_data["Ogre"] = get_connection(ds, "Monster", "Ogre")
        sql_data["Skeleton"] = get_connection(ds, "Monster", "Skeleton")
        sql_data["Gremlin"] = get_connection(ds, "Monster", "Gremlin")
    finally:
        ds.close()
    return sql_data


if __name__ == '__main__':
    print(get_data())