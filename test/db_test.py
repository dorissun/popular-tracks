from testcontainers.mysql import MySqlContainer
import unittest
from  mysql.connector import connect

from popular_tracks import db

class TestDBMethods(unittest.TestCase):
    def test_db(self):
        with MySqlContainer('mysql:8.0.22') as mysql:
            conn = connect(user=mysql.MYSQL_USER,
                           password=mysql.MYSQL_PASSWORD,
                           database=mysql.MYSQL_DATABASE,
                           port=mysql.get_exposed_port(3306))

            db.db_setup(conn)

            track_info_1 = {"id":"1",
                            "name": "track1",
                            "uri": "spotify:artist:6sFI",
                            "duration_ms": 100,
                            "release_date": "2010-01-01"
                            }
            db.save_tracks(conn, track_info_1)

            cursor = conn.cursor()
            cursor.execute("SELECT count(*) from tracks")

            (cnt,) = cursor.fetchone()
            self.assertEqual(cnt, 1)

if __name__ == '__main__':
    unittest.main()
