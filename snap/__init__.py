def _volume_string(value):
    stars = int(value / 2)
    bars = 50 - stars
    return "|" + u'\u2588'*stars + " "*bars + "|"

def status_string(client):
    name = client.friendly_name.ljust(15, ' ')
    return "{} {}".format(name, _volume_string(client.volume))
