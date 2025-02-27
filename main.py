from ctypes import c_int

import psycopg2
from psycopg2 import connect


class DataBase:

    def __init__(self):
        self.database = 'EPP'
        self.user = 'postgres'
        self.password = 'lich5800'

    def db_con(self):
        connection = psycopg2.connect(database=self.database, user=self.user, password=self.password)
        return connection

    def create_tables(self):
        connection = self.db_con()
        with connection.cursor() as cur:
            cur.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                client_id   SERIAL      PRIMARY KEY,
                first_name  VARCHAR(20) NOT NULL,
                last_name   VARCHAR(20) NOT NULL,
                email       VARCHAR(30) NOT NULL
            );
            ''')
            cur.execute('''
            CREATE TABLE IF NOT EXISTS phone_numbers (
                phone_id    SERIAL      PRIMARY KEY,
                client_id     INT         REFERENCES clients(client_id),
                number      VARCHAR(20) NOT NULL
            );
            ''')
            connection.commit()
        connection.close()
        print('Таблицы созданы')

    def write_client(self, first_name, last_name, email):
        connection = self.db_con()
        with connection.cursor() as cur:
            cur.execute('''
            INSERT INTO clients(first_name, last_name, email)
            VALUES(%s, %s, %s)
            ''', (first_name, last_name, email))
            connection.commit()
        connection.close()
        print('Клиент записан')

    def write_number(self, client_id, phone_number):
        connection = self.db_con()
        with connection.cursor() as cur:
            cur.execute('''
            INSERT INTO phone_numbers(client_id, number)
            VALUES(%s, %s)
            ''', (client_id, phone_number))
            connection.commit()
        connection.close()
        print('Номер телефона записан')

    def update_info(self, client_id, first_name, last_name, email):
        connection = self.db_con()
        with connection.cursor() as cur:
            cur.execute('''
            UPDATE clients 
            SET first_name = %s, last_name = %s, email = %s
            WHERE client_id = %s;
            ''', (first_name, last_name, email, client_id))
            connection.commit()
        connection.close()
        print('Данные клиента обновлены')

    def delete_number(self, client_id, number):
        connection = self.db_con()
        with connection.cursor() as cur:
            cur.execute('''
            DELETE FROM phone_numbers
            WHERE client_id = %s 
            AND number = %s;
            ''', (client_id, number))
            connection.commit()
        connection.close()
        print('Номер телефона удален')

    def delete_client(self, client_id):
        connection = self.db_con()
        with connection.cursor() as cur:
            cur.execute('''
            DELETE FROM phone_numbers
            WHERE client_id = %s;
            
            DELETE FROM clients
            WHERE client_id = %s;
            ''', (client_id, client_id))
            connection.commit()
        connection.close()
        print('Клиент удален')

    def find_client(self, first_name, last_name, email, phone_number):
        connection = self.db_con()
        with connection.cursor() as cur:
            client = cur.execute('''
            SELECT clients.client_id, clients.first_name, clients.last_name, phone_numbers.number
            FROM clients, phone_numbers
            WHERE clients.first_name = %s
            AND clients.last_name = %s
            AND clients.email = %s
            AND clients.client_id = phone_numbers.client_id
            AND phone_numbers.number = %s;
            ''', (first_name, last_name, email, phone_number))
            client = cur.fetchall()
        connection.close()
        if client == []:
            print('Клиент не найден')
        else:
            print(f'''Клиент найден:
            ID: {client[0][0]}
            Имя: {client[0][1]}
            Фамилия: {client[0][2]}
            Email: {client[0][3]}
            Номера телефонов: {", ".join(set(item[3] for item in client))}
            ''')

def main():
    db = DataBase()
    db.create_tables()
    db.write_client('John', 'Emin', 'home@ll.ry')
    db.write_number(1, '+79538954687')
    db.write_number(1, '895565544')
    db.update_info(1,'Hom', 'Jim', 'hhукеh@mmm.hj')
    db.delete_number(1, '+79538954687')
    db.delete_client(1)
    db.find_client('Hom', 'Jim', 'hhукеh@mmm.hj', '895565544')

if __name__ == '__main__':
    main()