import numpy as np


class RSI:

    def __init__(self, prices=[], period=14):
        """
        Creates a new RSI calculator with the given prices and period.

        :param prices: A list of prices for a financial instrument.
        :type prices: List[float]
        :param period: The number of periods to use in the RSI calculation.
        :type period: int
        """
        self.prices = prices
        self.period = period

    def calculate_rsi(self):
        """
        Calculates the Relative Strength Index (RSI) for the given prices and period.

        The RSI is a momentum oscillator that measures the speed and change of price movements.
        It oscillates between 0 and 100, and is typically calculated over a period of 14 days.
        A reading above 70 is generally considered overbought, while a reading below 30 is oversold.

        :return: The RSI value for the given prices and period.
        :rtype: float
        """
        # Calculate the up and down values
        diff = np.diff(self.prices)
        up = np.where(diff > 0, diff, 0)
        down = np.where(diff < 0, -diff, 0)

        # Calculate the average gain and average loss
        avg_gain = np.mean(up[:self.period])
        avg_loss = np.mean(down[:self.period])

        # Calculate the RS and RSI
        rs = np.divide(avg_gain,
                       avg_loss,
                       out=np.zeros_like(avg_gain),
                       where=avg_loss != 0)
        rsi = 100 - 100 / (1 + rs)

        return rsi
