class XpathValue():
    def __init__(self, hostname, xpath, value):
        self._hostname = hostname
        self._xpath = xpath
        self._data = {"value": value}