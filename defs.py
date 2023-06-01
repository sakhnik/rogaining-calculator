
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
quickevent_port = 1234

quickevent_url = f"http://localhost:{quickevent_port}/card"


def format_time(time: int) -> str:
    seconds = int(time) % 60
    minutes = int(time // 60)
    hours = minutes // 60
    minutes = minutes % 60
    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    return f"{minutes:02d}:{seconds:02d}"


def calc_tempo(time: int, distance_km: float) -> str:
    if distance_km == 0:
        return "INF"
    tempo = float(time) / distance_km
    return format_time(int(tempo))
