import pandas as pd
import yfinance as yf
from fisher_transform import fisher


'''This code downloads historical data of a stock from yfinance package and implements the fisher transformation.'''

# Download the dataframe
df = yf.download("AXISBANK.NS", period="60d", interval="15m")

# Apply transformation
df_trans = fisher(df["High"], df["Low"])  # Passing the high and low column
df = pd.concat([df, df_trans], axis=1)    # Concatenating the original dataframe and the fisher transformation values
print(df)