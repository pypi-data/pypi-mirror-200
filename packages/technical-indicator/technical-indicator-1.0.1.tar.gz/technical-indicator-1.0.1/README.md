# Technical Indicator Python Package

This Python package provides methods to calculate various technical indicators from financial time series datasets. The indicators are organized into three categories: momentum indicators, volume indicators, and volatility indicators.

### Installation

You can install the Technical Indicator package using pip:

```
pip install technical-indicator
```

### Momentum Indicators

#### Relative Strength Index (RSI)

The RSI measures the ratio of upward price movements to downward price movements over a given period of time. To calculate the RSI using this library, initialize an instance of the RSI class with an array of prices and an optional lookback period (default is 14), and call the calculate method:

```
from technical_indicator.momentum import RSI

# Example data
period = 12
prices = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 17, 16, 18, 20]

# Initialize the RSI indicator with the prices and period
rsi = RSI(prices, period)

# Calculate the RSI values
rsi_values = rsi.calculate_rsi()
```
