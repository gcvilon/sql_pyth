import psycopg2



class DataBase:

    def __init__(self):
        self.database = 'EPP'
        self.user = 'postgres'
        self.password = 'lich5800'

    def create_tables(self):
        with psycopg2.connect(database=self.database, user=self.user, password=self.password) as connection:
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
        print('Таблицы созданы')

    def write_client(self, first_name, last_name, email):
        with psycopg2.connect(database=self.database, user=self.user, password=self.password) as connection:
            with connection.cursor() as cur:
                cur.execute('''
                INSERT INTO clients(first_name, last_name, email)
                VALUES(%s, %s, %s)
                ''', (first_name, last_name, email))
        print('Клиент записан')

    def write_number(self, client_id, phone_number):
        with psycopg2.connect(database=self.database, user=self.user, password=self.password) as connection:
            with connection.cursor() as cur:
                cur.execute('''
                INSERT INTO phone_numbers(client_id, number)
                VALUES(%s, %s)
                ''', (client_id, phone_number))
        print('Номер телефона записан')

    def update_info(self, client_id=None, first_name=None, last_name=None, email=None):
        if client_id is None:
            print("Ошибка: Необходимо указать client_id.")
            return
        with psycopg2.connect(database=self.database, user=self.user, password=self.password) as connection:
            with connection.cursor() as cur:
                updates = []
                params = []
                if first_name is not None:
                    updates.append("first_name = %s")
                    params.append(first_name)
                if last_name is not None:
                    updates.append("last_name = %s")
                    params.append(last_name)
                if email is not None:
                    updates.append("email = %s")
                    params.append(email)
                if not updates:
                    print("Ошибка: Не указаны данные для обновления.")
                    return
                query = f'''
                UPDATE clients 
                SET {', '.join(updates)}
                WHERE client_id = %s;
                '''
                params.append(client_id)
                cur.execute(query, params)
        print('Данные клиента обновлены')

    def delete_number(self, client_id, number):
        with psycopg2.connect(database=self.database, user=self.user, password=self.password) as connection:
            with connection.cursor() as cur:
                cur.execute('''
                DELETE FROM phone_numbers
                WHERE client_id = %s 
                AND number = %s;
                ''', (client_id, number))
        print('Номер телефона удален')

    def delete_client(self, client_id):
        with psycopg2.connect(database=self.database, user=self.user, password=self.password) as connection:
            with connection.cursor() as cur:
                cur.execute('''
                DELETE FROM phone_numbers
                WHERE client_id = %s;
                
                DELETE FROM clients
                WHERE client_id = %s;
                ''', (client_id, client_id))
        print('Клиент удален')

    def find_client(self, first_name=None, last_name=None, email=None, phone_number=None):
        with psycopg2.connect(database=self.database, user=self.user, password=self.password) as connection:
            with connection.cursor() as cur:
                query = '''
                SELECT clients.client_id, clients.first_name, clients.last_name, clients.email, phone_numbers.number
                FROM clients
                LEFT JOIN phone_numbers ON clients.client_id = phone_numbers.client_id
                WHERE (%s IS NULL OR clients.first_name = %s)
                  AND (%s IS NULL OR clients.last_name = %s)
                  AND (%s IS NULL OR clients.email = %s)
                  AND (%s IS NULL OR phone_numbers.number = %s);
                '''
                cur.execute(query,
                            (first_name, first_name, last_name, last_name, email, email, phone_number, phone_number))
                client_data = cur.fetchall()

        if not client_data:
            print('Клиент не найден')
        else:
            clients = {}
            for row in client_data:
                client_id, first_name, last_name, email, phone_number = row
                if client_id not in clients:
                    clients[client_id] = {
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': email,
                        'phone_numbers': set()
                    }
                if phone_number:
                    clients[client_id]['phone_numbers'].add(phone_number)
            for client_id, data in clients.items():
                print(f'''Клиент найден:
                        ID: {client_id}
                        Имя: {data['first_name']}
                        Фамилия: {data['last_name']}
                        Email: {data['email']}
                        Номера телефонов: {", ".join(data['phone_numbers']) if data['phone_numbers'] else "Нет данных"}
                        ''')

def main():
    db = DataBase()
    db.create_tables()
    db.write_client('John', 'Emin', 'home@ll.ry')
    db.write_number(1, '+79538954687')
    db.update_info(client_id=1,first_name='Home', last_name='Jim', email='hhукеh@mmm.hj')
    db.delete_number(1, '+79538954687')
    db.delete_client(1)
    db.find_client(last_name='Emin')

if __name__ == '__main__':
    main()