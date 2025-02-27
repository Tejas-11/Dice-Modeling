from die import RollImpl


tests = [
    # addition tests
    'a = a + 5',
    'a = 5 + a',
    'a += 5',
    'a = a + b',
    'a = b + a',
    'a += b',

    # negation tests
    'a = -a',

    # subtraction tests
    'a = a - 5',
    'a = 5 - a',
    'a -= 5',
    'a = a - b',
    'a = b - a',
    'a -= b',

    # power tests
    'a = a**2',
    'a = a**3',
    'a = a**-3',
    'a **= 2',

    # multiplication tests
    'a = a * 3',
    'a = 3 * a',
    'a *= 3',
    'a = a * -3'
]


def run_test(test, a, b):
    print(test)
    test += '\nprint(a)'
    exec(test)
    print('\n\n')


def main():
    #a = RollImpl([i+1 for i in range(4)], 'list')
    a = RollImpl([1, 2, 2, 3, 3, 3], 'list')
    b = RollImpl([i+1 for i in range(8)], 'list')

    for test in tests:
        run_test(test, a, b)


if __name__ == '__main__':
    main()
