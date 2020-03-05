class cListBrand:

    def __new__(cls, name):
        return super(cLBrand, cls).__new__(cls) if name in cls._lb else None

class cBrand(cListBrand):
    def __init__(self, name):
        self.brand = name
        self.l_url = self._lb[name]['laser']
        self.i_url = self._lb[name]['inkjet']
        self.m_url = self._lb[name]['matrix']
        self._lb = None
    def __str__(self):
        return f'{self.brand}: Laser_url - {self.l_url != None}, Inkjet_url - {self.i_url != None}, Matrix_url - {self.m_url != None}'
