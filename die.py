class RollImpl:
    # Assumptions on data
    # should contain every number between minimum and maximum atleast once
    # for list format the list should be presorted
    _mean = None
    _median = None
    _mode = None
    _dev = None

    _min = None
    _max = None
    _den = None
    _data = None

    def __init__(self, *args):
        if len(args)>0:
            data, format = args[0], args[1]
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

    def __neg__(self):
        result = self.__class__()
        result._min, result._max = -self._max, -self._min
        result._den = self._den
        result._data = self._data[::-1]
        return result

    def __add__(self, other):
        assert isinstance(other, int) or isinstance(other, self.__class__), \
            f"{other.__class__} not supported for this operation. Only int and {self.__class__.__name__} types supported."
        if isinstance(other, int):
            other = self.__class__([other], 'list')
        result = self.__class__()
        result._min = self._min + other._min
        result._max = self._max + other._max
        result._den = self._den * other._den
        result._data = [0] * (result._max - result._min + 1)
        for i, x in enumerate(self._data):
            for j, y in enumerate(other._data):
                result._data[i + j] += x * y
        return result

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self.__add__(-other)

    def __rsub__(self, other):
        return (-self).__add__(other)

    def __mul__(self, other):
        assert isinstance(other, int), f"{other.__class__} not supported for this operation. Only int type supported."
        if other<0:
            other = -other
            self = -self
        sl = self._max - self._min + 1

        result = self.__class__()
        result._min = self._min * other
        result._max = self._max * other
        result._den = self._den ** other

        rl = result._max - result._min + 1
        result._data = self._data + [0] * (rl - sl)
        rl = sl
        for _ in range(other - 1):
            nl = rl + sl - 1
            for i in range(1, sl):
                for j in range(i):
                    result._data[nl-i] += self._data[sl-i+j] * result._data[rl-1-j]
            for i in range(rl-sl):
                result._data[rl-1-i] = self._data[0] * result._data[rl-1-i]
                for j in range(1, sl):
                    result._data[rl-1-i] += self._data[j] * result._data[rl-1-i-j]
            for i in range(sl):
                result._data[sl-i-1] = self._data[0] * result._data[sl-i-1]
                for j in range(1, sl-i):
                    result._data[sl-i-1] += self._data[j]*result._data[sl-i-1-j]
            rl = nl
        return result

    def __rmul__(self, other):
        return self.__mul__(other)

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
