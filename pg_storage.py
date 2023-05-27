from storage import Storage
from position import Position
import psycopg2
from defs import pg_host, pg_db, pg_user, pg_pass, pg_ns


class PgStorage(Storage):
    def __init__(self):
        with psycopg2.connect(host=pg_host,
                              database=pg_db,
                              user=pg_user,
                              password=pg_pass) as conn:
            with conn.cursor() as cursor:
                query = f"SELECT a.siid, a.firstname, a.lastname, c.name FROM {pg_ns}.competitors a LEFT JOIN {pg_ns}.classes c ON a.classid = c.id"
                cursor.execute(query)
                rows = cursor.fetchall()
                self.names = {siid: (f"{last} {first}", cl) for siid, first, last, cl in rows}

    def get_name(self, number: int) -> str:
        name, _ = self.names[number]
        return name

    def get_class(self, number: int) -> str:
        _, cl = self.names[number]
        return cl

    def get_start_position(self) -> Position:
        return Position()

    def get_finish_position(self) -> Position:
        return Position()

    def get_control_position(self, code: int) -> Position:
        return Position()