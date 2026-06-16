def calculate_voltage(current, resistance):
    return current * resistance


def calculate_current(voltage, resistance):
    if resistance == 0:
        raise ValueError("Resistance cannot be zero.")
    return voltage / resistance


def calculate_resistance(voltage, current):
    if current == 0:
        raise ValueError("Current cannot be zero.")
    return voltage / current


def series_resistance(resistances):
    return sum(resistances)


def parallel_resistance(resistances):
    for resistance in resistances:
        if resistance == 0:
            raise ValueError("Resistance cannot be zero.")
    
    reciprocal_sum = 0

    for resistance in resistances:
        reciprocal_sum += 1 / resistance

    return 1 / reciprocal_sum


def power_from_voltage_current(voltage, current):
    return voltage * current


def power_from_current_resistance(current, resistance):
    return current ** 2 * resistance


def power_from_voltage_resistance(voltage, resistance):
    return voltage ** 2 / resistance

def voltage_divider(vin, r1, r2):
    return vin * r2 / (r1 + r2)


def divider_current(vin, r1, r2):
    return vin / (r1 + r2)


def resistor_power(current, resistance):
    return current ** 2 * resistance


import numpy as np


def solve_two_loop_kvl(r1, r2, r3, v1, v2):

    A = np.array([
        [r1 + r3, -r3],
        [-r3, r2 + r3]
    ])

    B = np.array([
        v1,
        v2
    ])

    currents = np.linalg.solve(A, B)

    return currents[0], currents[1]