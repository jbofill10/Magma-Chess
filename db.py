import psycopg2
import dotenv, os, sys
dotenv.load_dotenv()


class SQL:

    connection = None
    cursor = None
    commit_count = 0

    def __init__(self):
        try:
            self.connection = psycopg2.connect(os.getenv('SQL_URL'))
            self.cursor = self.connection.cursor()

            print('Connected to PostgreSQL!')

        except Exception as e:

            print(f'Could not connect to PostgreSQL\n\n{e}')

    def add_position(self, index, position, result):

        with self.connection.cursor() as cursor:

            try:
                cursor.execute(
                    "INSERT INTO train(id, position, result) VALUES ({}, '{}', '{}');".format(index, position, result)
                )

                self.commit_count += 1
                if self.commit_count == 100000:
                    self.commit_count = 0
                    self.connection.commit()

            except Exception as e:
                print(f'Error inserting into PostgreSQL\n\n{e}')
                print("INSERT INTO train(id, position, result) VALUES ({}, '{}', '{}');".format(index, position, result))
                sys.exit(0)