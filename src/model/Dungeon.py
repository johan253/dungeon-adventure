class Dungeon:
    def __init__self(self):
        self.__my_rooms = [[]] # Room Array
        self.__my_user_x_coordinate = 0.0
        self.__my_user_y_coordinate = 0.0

    def __create_maze(self):
        pass

    def __maze_is_valid(self,maze):
        pass

    def get_user_x(self):
        return self.__my_user_x_coordinate

    def get_user_y(self):
        return self.__my_user_y_coordinate

    def get_current_room(self):
        return self.__my_rooms

    def to_string(self):
        return str(self)


