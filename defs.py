
def get_seconds(h, m, s):
    return (h * 60 + m) * 60 + s


deadline = get_seconds(15, 0, 0)

pg_host = "localhost"
pg_db = "quickevent"
pg_user = "quickevent_admin"
pg_pass = ""
pg_ns = "sprint2023_5"

server_port = 12345
