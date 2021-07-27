from pytest import mark
from bot.calculator import Calculator

@mark.usefixtures('browser')
class TestCalculatorGoogle:

    @mark.parametrize(
        'num_1, num_2',
        [(1, 2), (3, 3), (4, 5), (645332, 422345)]
    )
    def test_sum_of_two_numbers(self, num_1, num_2):
        calculator = Calculator(self.browser)
        result = int(calculator.calculate(f'{num_1} + {num_2}'))
        assert result == num_1 + num_2

    @mark.parametrize(
        'num_1, num_2',
        [(1, 2), (3, 3), (4, 5), (645332, 422345)]
    )
    def test_multiplication_of_two_numbers(self, num_1, num_2):
        calculator = Calculator(self.browser)
        result = int(calculator.calculate(f'{num_1} * {num_2}'))
        assert result == num_1 * num_2

    @mark.parametrize(
        'num_1, num_2',
        [(1, 2), (3, 3), (4, 5), (645332, 422345)]
    )
    def test_division_of_two_numbers(self, num_1, num_2):
        calculator = Calculator(self.browser)
        result = float(calculator.calculate(f'{num_1} / {num_2}'))
        assert result == num_1 / num_2

    @mark.parametrize(
        'num_1, num_2',
        [(5, 2), (3, 3), (4, 5), (32, 5)]
    )
    def test_pow(self, num_1, num_2):
        calculator = Calculator(self.browser)
        result = int(calculator.calculate(f'{num_1} ** {num_2}'))
        assert result == num_1 ** num_2