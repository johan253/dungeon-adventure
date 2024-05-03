import sqlite3


class DatabaseController:
    __DATABASE_PATH = '../DungeonData.db'
    __DB = sqlite3.connect(__DATABASE_PATH)
    __instance = None

    def __new__(cls, *args, **kwargs):
        """
        This method creates a new instance of the DatabaseController class if one does not already exist.
        otherwise, it returns the existing instance.
        :param args: the arguments passed to the class constructor
        :param kwargs: the keyword arguments passed to the class constructor
        """
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        """
        Constructor for the DatabaseController class
        """
        pass

    def __get_connection(self, ds, character_class, name):
        query = f"Select * from '{character_class}' where name = '{name}'"
        result_map = {}
        try:
            pointer = ds.cursor()
            pointer.execute(query)
            columns = [desc[0] for desc in pointer.description]
            for row in pointer.fetchall():
                result_map = {columns[i]: row[i] for i in range(len(columns))}
        except sqlite3.Error as error:
            print(error)
            raise SystemExit(0)
        finally:
            return result_map

    def get_stats(self, character_class: str, character_name: str):
        """
        This method retrieves the stats of a character from the database
        :param character_class: the class of the character
        :return: a dictionary containing the stats of the character
        """
        return self.__get_connection(self.__DB, character_class, character_name)

    def get_all_data(self) -> dict:
        """
        This method retrieves all data from the database
        :return: a dictionary containing all data from the database
        """
        query_hero = "Select * from Hero"
        query_monster = "Select * from Monster"
        data = {}
        try:
            pointer = self.__DB.cursor()
            pointer.execute(query_hero)
            columns = [desc[0] for desc in pointer.description]
            data['Hero'] = [{columns[i]: row[i] for i in range(len(columns))} for row in pointer.fetchall()]
            pointer.execute(query_monster)
            columns = [desc[0] for desc in pointer.description]
            data['Monster'] = [{columns[i]: row[i] for i in range(len(columns))} for row in pointer.fetchall()]
        except sqlite3.Error as error:
            print(error)
            raise SystemExit(0)
        finally:
            return data


if __name__ == '__main__':
    data = DatabaseController().get_all_data()
    for char_class in data:
        for char in data[char_class]:
            print(char)
