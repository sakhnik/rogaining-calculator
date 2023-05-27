
def get_seconds(h, m, s):
    return (h * 60 + m) * 60 + s


start = get_seconds(11, 0, 0)
deadline = get_seconds(14, 0, 0)

pg_host = "localhost"
pg_db = "quickevent"
pg_user = "quickevent_admin"
pg_pass = ""
pg_ns = "sprint2023_5"

server_port = 12345
