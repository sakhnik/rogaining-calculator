from storage import Storage
from position import Position
import psycopg2
import defs
from defs import pg_ns


class PgStorage(Storage):
    def __init__(self):
        with psycopg2.connect(host=defs.pg_host,
                              database=defs.pg_db,
                              user=defs.pg_user,
                              password=defs.pg_pass) as conn:
            with conn.cursor() as cursor:
                query = f"SELECT a.siid, a.firstname, a.lastname, c.name \
                    FROM {pg_ns}.competitors a \
                    LEFT JOIN {pg_ns}.classes c ON a.classid = c.id"
                cursor.execute(query)
                rows = cursor.fetchall()
                self.names = {siid: (f"{last} {first}", cl)
                              for siid, first, last, cl in rows}
            with conn.cursor() as cursor:
                query = f"SELECT code, latitude, longitude \
                    FROM {pg_ns}.codes WHERE note = 'E1'"
                cursor.execute(query)
                rows = cursor.fetchall()
                self.codes = {code: (lat, lon) for code, lat, lon in rows}

    def get_name(self, number: int) -> str:
        name, _ = self.names[number]
        return name

    def get_class(self, number: int) -> str:
        _, cl = self.names[number]
        return cl

    def get_start_position(self) -> Position:
        lat, lon = self.codes[10]
        return Position(lat, lon)

    def get_finish_position(self) -> Position:
        lat, lon = self.codes[900]
        return Position(lat, lon)

    def get_control_position(self, code: int) -> Position:
        lat, lon = self.codes[code]
        return Position(lat, lon)
