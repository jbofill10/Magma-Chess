import pymysql.cursors
import dotenv, os
dotenv.load_dotenv()


class SQL:

    connection = None
    commit_count = 0

    def __init__(self):
        try:
            self.connection = pymysql.connect(
                host=os.getenv('host'),
                user=os.getenv('user'),
                passwd=os.getenv('password'),
                db=os.getenv('db'),
                cursorclass=pymysql.cursors.DictCursor
            )

            print('Connected to MySQL!')
        except Exception as e:
            print(f'Could not connect to SQL\n\n{e}')

    def add_position(self, index, position, result):

        with self.connection.cursor() as cursor:

            try:
                cursor.execute(
                    "INSERT INTO dataset(`id`, `position`, `result`) VALUES ({}, '{}', {});".format(index, position, result)
                )
                self.commit_count += 1
                if self.commit_count == 1000000:
                    self.commit_count = 0
                    self.connection.commit()
            except Exception as e:
                print(f'Error inserting into SQL\n\n{e}')