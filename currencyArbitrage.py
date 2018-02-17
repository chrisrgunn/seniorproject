

class Currency:
    def __init__(self, name):
        self._name = name
        self._rates = []

    def getName(self):
        return self._name

    def getRates(self):
        return self._rates

    def addRateEdge(self, e):
        self._rates.append(e)

    def addRate(self, currency, weight=0):
        e = edge(currency, weight)
        self._rates.append(e)

    def findRates(self, maincurrency, current_value, depth):
        if self._name == maincurrency:
            #We are back at the main currency - see if the value > 1
            if current_value > 1.0:
                #We found a way to make money!
                print("We found a way!  ")
                print(current_value, self._name)
                return True
        if depth > 3:
            #Base case for recursion: too many exchanges
            return False
        for rate in self._rates:
            conversion = current_value * rate.getExchange()
            for c in currencies:
                if c.getName() == rate.getCurrency():
                    if c.findRates(maincurrency, conversion, depth+1):
                        print("from", current_value, self._name)
                        return True
        return False

    def findArbitrage(self):
        for rate in self._rates:
            for c in currencies:
                if c.getName() == rate.getCurrency():
                    if c.findRates(self._name, rate.getExchange(), 1):
                        return True
        return False


class Edge:
    def __init__(self, currency, rate = 0):
        self._currency = currency
        self._exchange = rate

    def getCurrency(self):
        return self._currency

    def getExchange(self):
        return self._exchange

    def setExchange(self, exchange):
        self._exchange = exchange


def addExchange(name1, name2, exchange1):
    e1 = Edge(name2, exchange1)
    e2 =Edge(name1, 1.0/exchange1)
    for currency in currencies:
        if currency.getName() == name1:
            currency.addRateEdge(e1)
        if currency.getName() == name2:
            currency.addRateEdge(e2)


def addExchange2(name1, name2, weight=0):
    for currency in currencies:
        if currency.getName() == name1:
            currency.addNeighbor(name2, exchange1)
        if currency.getName() == name2:
            currency.addNeighbor(name1, 1.0/exchange1)


currencies = []
currency = Currency("Dollar")
currencies.append(currency)
currency = Currency("Pound")
currencies.append(currency)
currency = Currency("Euro")
currencies.append(currency)
currency = Currency("Yen")
currencies.append(currency)

addExchange("Dollar", "Pound", 0.7)
addExchange("Dollar", "Euro", 0.95)
addExchange("Yen", "Dollar", 0.0085)
addExchange("Euro", "Pound", 0.75)
addExchange("Pound", "Yen", 175.0)
addExchange("Euro", "Yen", 233.3)

currencies[0].findArbitrage()