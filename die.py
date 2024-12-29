class RollImpl:
    # Assumptions on data
    # should contain every number between minimum and maximum atleast once
    # for list format the list should be presorted
    _mean = None
    _median = None
    _mode = None
    _dev = None

    def __init__(self, data, format):
        assert format in ('list', 'dict')
        if format=='list':
            self._min = data[0]
            self._max = data[-1]
            self._den = len(data)
            self._data = [0] * (self._max - self._min + 1)
            j = 0
            self._data[j] = 1
            for i in range(1, self._den):
                if data[i]!=data[i - 1]:
                    j += 1
                    self._data[j] = 1
                else:
                    self._data[j] += 1
        elif format=='dict':
            data_key = sorted(set(data))
            self._min = data_key[0]
            self._max = data_key[-1]
            self._den = sum(data.values())
            self._data = [data[key] for key in data_key]

    def __str__(self):
        data_rep = '\n'.join([f'  {self._min + ind}: {x}' for ind, x in enumerate(self._data)])
        res = f'min: {self._min}\nmax: {self._max}\nden: {self._den}\n' \
                f'data:\n{data_rep}'
        return res

    def __add__(self, other):
        assert isinstance(other, int) or isinstance(other, self.__class__), \
            f"{other.__class__} not supported for this operation. Only int and {self.__class__.__name__} types supported."
        if isinstance(other, int):
            other = self.__class__([other], 'list')
        result = self.__class__([1], 'list')
        result._min = self._min + other._min
        result._max = self._max + other._max
        result._den = self._den * other._den
        result._data = [0] * (result._max - result._min + 1)
        for i, x in enumerate(self._data):
            for j, y in enumerate(other._data):
                result._data[i + j] += x * y
        return result

    def __iadd__(self, other):
        assert isinstance(other, int) or isinstance(other, self.__class__), \
            f"{other.__class__} not supported for this operation. Only int and {self.__class__.__name__} types supported."
        if isinstance(other, int):
            other = self.__class__([other], 'list')
        _min = self._min + other._min
        _max = self._max + other._max
        _den = self._den * other._den
        _data = [0] * (_max - _min + 1)
        for i, x in enumerate(self._data):
            for j, y in enumerate(other._data):
                _data[i + j] += x * y
        self._min, self._max = _min, _max
        self._den = _den
        self._data = _data
        self.stat_reset()
        return self

    def __imul__(self, other):
        assert isinstance(other, int), f"{other.__class__} not supported for this operation. Only int type supported."
        assert other > 0, "Integer must be greater than zero"
        _min = self._min * other
        _max = self._max * other
        _den = self._den ** other
        _data = [(0, x) for x in self._data]
        _data = self._data
        _new_data = [0] * (_max - _min + 1)
        for _ in range(other):
            _data = _new_data[:_new_data.find(0)]
            for i, x in enumerate(_data):
                for j, y in enumerate(self._data):
                    _new_data[i+j] += x * y
        s._min, self._max = _min, _max
        self._den = _den
        self._data = _new_data
        self.stat_reset()
        return self

    def __pow__(self, exp):
        assert isinstance(exp, int), f"{exp.__class__} not supported for this operation. Only int type supported."
        result = self.__class__([1], 'list')
        if exp == 0:
            return result
        fn = max if exp>0 else min
        exp = abs(exp)
        n = self._max - self._min + 1
        _data = self._data
        for _ in range(exp-1):
            _new_data = [0] * n
            for i in range(n):
                for j in range(n):
                    _new_data[fn(i, j)] += _data[i] * self._data[j]
            _data = _new_data
        result._min = self._min
        result._max = self._max
        result._den = self._den ** exp
        result._data = _data
        return result

    def __ipow__(self, exp):
        assert isinstance(exp, int), f"{exp.__type__} not supported for this operation. Only int type supported."
        if exp == 0:
            self._data = [1]
            self._den = 1
            self._min = self._max = 1
            self.stat_reset()
            return self
        fn = max if exp>0 else min
        exp = abs(exp)
        n = self._max - self._min + 1
        _data = self._data
        for _ in range(exp-1):
            _new_data = [0] * n
            for i in range(n):
                for j in range(n):
                    _new_data[fn(i, j)] += _data[i] * self._data[j]
            _data = _new_data
        self._den = self._den ** exp
        self._data = _data
        self.stat_reset()
        return self

    @property
    def mean(self):
        if not self._mean:
            self._mean = sum([(self._min + ind) * x for ind, x in enumerate(self._data)])/self._den
        return self._mean

    @property
    def median(self):
        if not self._median:
            med_ind = self._den//2
            for ind, x in enumerate(self._data):
                if x>med_ind:
                    break
                med_ind -= x
            self._median = self._min + ind
            if self._den%2==0 and med_ind==0:
                self._median -= 1/2
        return self._median

    @property
    def mode(self):
        if not self._mode:
            mode_value = 0
            mode_count = 0
            for ind, x in enumerate(self._data):
                if x>mode_count:
                    mode_value, mode_count = ind, x
            self._mode = self._min + mode_value
        return self._mode

    @property
    def dev(self):
        if not self._dev:
            temp = sum([((self._min + ind)**2) * x for ind, x in enumerate(self._data)])/self._den
            self._dev = (temp - self.mean**2) ** (1/2)
        return self._dev

    def stat_reset(self):
        self._mean = self._median = self._mode = self._dev = None

    def stat_print(self):
        print(f"mean: {self.mean}\nmedian: {self.median}")
        print(f"mode: {self.mode}\ndeviation: {self.dev}\n")
    # also add a multiplication function to class
    # multiplication function only for in multiplication not die to die multiplication

a = RollImpl([i+1 for i in range(6)], 'list')
print(a)
a.stat_print()

"""
b = RollImpl([i+1 for i in range(8)], 'list')
print(b)
b.stat_print()

c = a + b
print(c)
c.stat_print()

c += 5
print(c)
c.stat_print()

c = a ** -2
print(c)
c.stat_print()
"""

d = a ** 4
print(d)
d.stat_print()


a **= 2
print(a)
a.stat_print()

a **= 2
print(a)
a.stat_print()
