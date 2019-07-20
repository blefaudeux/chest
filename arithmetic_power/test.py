#!/usr/bin/python3
import random
import math
import timeit


def recursive_power(a, b):
    # This will break if b gets too big (stack overflow)
    if b == 0:
        return 1

    if b == 1:
        return a

    r = recursive_power(a, b/2)

    if b % 2 == 0:
        return r * r

    return a * r * r


def naive_power(a, b):
    if b == 0:
        return 1

    if b == 1:
        return a

    res = 1
    for _ in range(b):
        res *= a

    return res


def better_power_constant_footprint(a, b):
    if b == 0:
        return 1

    if b == 1:
        return a

    carry = a
    exp = 1

    # Double the exponent at every iteration
    while 2 * exp < b:
        carry *= carry
        exp += exp

    if exp == b:
        return carry

    # Do the rest the naive way
    for _ in range(b-exp):
        carry *= a

    return carry


def better_power_lut(a, b):
    if b == 0:
        return 1

    if b == 1:
        return a

    carry = a
    exp = 1
    lut_exp = []
    lut_res = []

    # Double the exponent at every iteration
    # Keep the values in a LUT
    while 2 * exp < b:
        carry *= carry
        exp += exp

        lut_exp.append(exp)
        lut_res.append(carry)

    lut_exp.pop()  # This sample cannot be usable
    lut_res.pop()

    # Walk back the LUT to reuse intermediates if possible
    while lut_exp and exp < b:
        opt_exp = lut_exp.pop()
        opt_res = lut_res.pop()

        if opt_exp < b-exp:
            carry *= opt_res
            exp += opt_exp

    # Finish the naive way
    if exp == b:
        return carry

    for _ in range(b-exp):
        carry *= a
    return carry


if __name__ == "__main__":
    print("testing recursive power:")
    a = random.randint(-1000, 1000)
    b = random.randint(0, 100)
    print("a: {}, b = {}".format(a, b))

    def res():
        return better_power_constant_footprint(a, b)

    def res_recursive():
        try:
            return recursive_power(a, b)
        except RecursionError:
            return "Recursion Error - stack overflow"

    def res_lut():
        return better_power_lut(a, b)

    def res_ref():
        return naive_power(a, b)

    print("{:.2}s naive power".format(timeit.timeit(res_ref)))
    print("{} recursive power".format(res_recursive()))
    print("{:.2}s better power".format(timeit.timeit(res)))
    print("{:.2}s better power LUT".format(timeit.timeit(res_lut)))

    # The following calls are cached by cpython
    if res() != res_ref() or res() != res_lut():
        print("Invalid !")
        print(res(), res_ref(), res_lut())

    else:
        print("Valid !")
