import math


class Calculator:

    def __init__(self):
        """Create an instance of a Calculator object. This instance will have a field, memory, whose initial value
        will be 0"""
        self.__memory: float = 0

    @property
    def memory(self):
        return self.__memory

    def add(self, addend: int | float) -> float:
        """Take a numeric value, addend, and add it to the current value in memory. Save the result in memory
        and return it."""
        Calculator.__assert_number(addend)
        self.__memory += addend
        return self.__memory

    def subtract(self, subtrahend: float) -> float:
        """Take a numeric value, subtrahend, and subtract it to the current value in memory. Save the result in memory
        and return it."""
        Calculator.__assert_number(subtrahend)
        self.__memory -= subtrahend
        return self.__memory

    def multiply(self, multiplicand: float) -> float:
        """Take a numeric value, multiplicand, and multiply it by the current value in memory. Save the result in memory
        and return it."""
        Calculator.__assert_number(multiplicand)
        self.__memory *= multiplicand
        return self.__memory

    def divide(self, divisor: float) -> float:
        """Take a numeric value, multiplicand, and divide the current value in memory by it. Save the result in memory
        and return it."""
        Calculator.__assert_number(divisor)
        self.__memory /= divisor
        return self.__memory

    def calculate_nth_root(self, degree: float) -> float:
        """Take a numeric value other than zero, degree, and calculate the degree-th root of the current value
        in memory. Save the result in memory and return it."""
        Calculator.__assert_number(degree)
        assert degree != 0, 'Root degree must not be zero. Please enter a different value'
        if self.__memory < 0:
            self.__memory = -math.pow(abs(self.__memory), 1 / degree)
        else:
            self.__memory = math.pow(self.__memory, 1 / degree)
        return self.__memory

    def reset_memory(self) -> None:
        """Set memory back to 0."""
        self.__memory = 0

    @staticmethod
    def __assert_number(value) -> None:
        """Assert whether a value is an instance of int or float. Otherwise, send an AssertionError and request the
        user to ask one of those two instance types."""
        assert isinstance(value, (int, float)), 'Please enter a numeric value, such as an int or float'
