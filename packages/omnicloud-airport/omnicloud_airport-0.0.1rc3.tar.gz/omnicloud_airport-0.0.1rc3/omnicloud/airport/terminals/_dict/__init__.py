from ...abc import Building
from ...tools.pkg import import_gates


class Terminal(dict, Building):
    '''
    It as an omnicloud.airport's Terminal for a main python object "dict".
    '''

    @property
    def parcel(self):
        return self


import_gates(__file__, __name__)
