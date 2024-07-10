import psycopg2
import constant


class DataBase:
    def __init__(self):
        self.connection = psycopg2.connect(host=constant.host, user=constant.user, password=constant.password, database=constant.db_name)

    def __connection_on(self):
        try:
            connection = self.connection
        except Exception as e:
            print(e)

    def __connection_off(self):
        connection = self.connection
        if connection:
            connection.close()
            print('Conection off')

    def Add(self, table_name: str, data: dict) -> None:
            if self.__find(table_name, data):
                self.__update(table_name, data)
            else:
                self.__add(table_name, data)

    def Get(self, table_name: str, data: dict, parametr: str):
        return self.__get(table_name, data, parametr)

    def __get(self, table_name: str, data: dict, parametr: str):
        connection = self.connection
        if table_name == 'users':
            set_condition = [f"{key} = '{value}'" if isinstance(value, str) else f"{key} = {value}" for key, value in
                             data.items() if key == 'telegram']
            set_condition = ', '.join(set_condition)
        else:
            set_condition = [f"{key} = '{value}'" if isinstance(value, str) else f"{key} = {value}" for key, value in
                             data.items() if key == 'telegram' or key == 'data']
            set_condition = ' and '.join(set_condition)
        with connection.cursor() as cursor:
            cursor.execute(
                f"""select {parametr} from {table_name} where {set_condition}"""
            )
            return cursor.fetchall()

    def __add(self, table_name: str, data: dict) -> None:
        connection = self.connection

        column_names_str = ', '.join([column for column in data.keys()])
        values_placeholder = ', '.join([str("'" + str(data[d]) + "'") for d in data.keys()])
        with connection.cursor() as cursor:
            cursor.execute(
                f'''INSERT INTO {table_name} ({column_names_str}) VALUES ({values_placeholder});'''
            )
            connection.commit()

    def __update(self, table_name: str, data: dict) -> None:
        connection = self.connection

        if table_name == 'users':
            set_expressions = [f"{key} = '{value}'" if isinstance(value, str) else f"{key} = {value}" for key, value in
                               data.items() if key != 'telegram']
            set_condition = [f"{key} = '{value}'" if isinstance(value, str) else f"{key} = {value}" for key, value in
                               data.items() if key == 'telegram']
        else:
            set_expressions = [f"{key} = '{value}'" if isinstance(value, str) else f"{key} = {value}" for key, value in
                               data.items() if key != 'telegram' or key != 'data']
            set_condition = [f"{key} = '{value}'" if isinstance(value, str) else f"{key} = {value}" for key, value in
                               data.items() if key == 'telegram' or key == 'data']
        set_clause1 = ', '.join(set_expressions)
        set_clause2 = 'and '.join(set_condition)
        with connection.cursor() as cursor:
            cursor.execute(
                f"""UPDATE {table_name} SET {set_clause1} WHERE {set_clause2}"""
            )
            connection.commit()

    def __delete(self, table_name: str, telegram: str) -> None:
        connection = self.connection

        with connection.cursor() as cursor:
            cursor.execute(
                f"""delete from {table_name} where telegram = '{telegram}'"""
            )
            connection.commit()

    def Find(self, table_name, data):
        return self.__find(table_name, data)

    def __find(self, table_name, data):

        connection = self.connection

        if table_name == 'users':
            set_condition = [f"{key} = '{value}'" if isinstance(value, str) else f"{key} = {value}" for key, value in
                               data.items() if key == 'telegram']
        else:
            set_condition = [f"{key} = '{value}'" if isinstance(value, str) else f"{key} = {value}" for key, value in
                               data.items() if key == 'telegram' or key == 'data']
        set_clause = 'and '.join(set_condition)
        with connection.cursor() as cursor:
            cursor.execute(
                f"""select * from {table_name} where {set_clause}"""
            )
            if not cursor.fetchall() == []:
                return True
            else:
                return False