""" Wrapper for snapcast client with controll methods """

from snap.api import Api

class Client:
    def __init__(self, wrapped):
        """ wrap a snapcast client """
        self.client = wrapped
        self.friendly_name = wrapped.friendly_name

    def toggle_mute(self):
        """ Mute if unmuted or vice-versa """
        if self.client.muted:
            Api._run(self.client.set_muted(False))
        else:
            Api._run(self.client.set_muted(True))

    @property
    def volume(self):
        return self.client.volume

    @property
    def muted(self):
        return self.client.muted

    @property
    def identifier(self):
        return self.client.identifier

    def set_volume(self, percent):
        Api._run(self.client.set_volume(percent))

    def mute(self, status):
        Api._run(self.client.set_muted(status))

    def _change_vol(self, amt):
        """ Helper function for volume reduction"""
        volume = self.volume + amt
        volume = max(0, volume)
        volume = min(100, volume)
        self.set_volume(volume)

    def lower_volume(self):
        """ Reduce the volume by 5% """
        self._change_vol(-5)

    def raise_volume(self):
        """ Increase the volume by 5% """
        self._change_vol(5)


