
from ...abc import Building


class _TerminalDict(dict, Building):

    @property
    def parcel(self):
        return self
