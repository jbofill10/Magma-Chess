import psycopg2
import dotenv, os
dotenv.load_dotenv()
import numpy
import pprint

class PSQL:

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

    def add_position(self, position, result):
        with self.connection.cursor() as cursor:

            try:
                cursor.execute(
                    "INSERT INTO train(position, result) VALUES ('{}', {});".format(position, result)
                )

                self.commit_count += 1

                if self.commit_count == 500000:
                    self.commit_count = 0
                    self.connection.commit()

            except Exception as e:
                print(f'Error inserting into PostgreSQL\n\n{e}')
                print("INSERT INTO train(position, result) VALUES ('{}', {});".format(position, result))

    def get_row_count(self):
        with self.connection.cursor() as cursor:
            # try:
            #     cursor.execute(
            #         "SELECT COUNT(*) FROM train;"
            #     )
            #
            #     row_count = cursor.fetchone()
            #     print("Row count successfully queried")
            #     print(row_count)
            #     return row_count[0]
            #
            # except Exception as e:
            #     print("Not able to get row count!")
            #     print(e)

            return 225319280

    def read_records_at(self, idxs):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    f'SELECT position, result FROM train where id >= {idxs[0]} and id <= {idxs[len(idxs)-1]}'
                )

                query_data = cursor.fetchall()
                x = []
                y = []
                for i in query_data:
                    x.append(i[0])
                    temp_y = i[1]

                    if temp_y == 1:
                        y.append([1, 0, 0])

                    elif temp_y == 0:
                        y.append([0, 1, 0])

                    else:
                        y.append([0, 0, 1])

                x = numpy.array(x)
                y = numpy.array(y)

                return x, y

            except Exception as e:
                print('Unable to retrieve training batch!')
                print(e)

    def last_commit(self):
        self.connection.commit()