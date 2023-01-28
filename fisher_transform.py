import numpy as np
from pandas import DataFrame, Series
from sys import float_info as sflt


# Calculate the difference of 2 series. If difference is 0 at any row, replace it with epsilon.
# epsilon is the closest possible value to 0 (neither 0 nor 1). Complicated maths lol.
def high_low_range(high: Series, low: Series) -> Series:
    diff = high - low
    if diff.eq(0).any().any():
        diff += sflt.epsilon
    return diff


# Check if the used dataframe or series meets the minimum lenght required to implement the transformation
def series_validity(series: Series, min_length: int = None) -> Series:
    has_length = min_length is not None and isinstance(min_length, int)
    if series is not None and isinstance(series, Series):
        return None if has_length and series.size < min_length else series



# Calculate fisher transformation
def fisher(high, low, length=None, signal=None, offset=None, **kwargs):
    length = int(length) if length and length > 0 else 9   # Specify length (default is 9)
    signal = int(signal) if signal and signal > 0 else 1   # Specify signal ( default is 1)
    _length = max(length, signal)
    high = series_validity(high, _length)
    low = series_validity(low, _length)
    offset = int(offset) if isinstance(offset, int) else 0 # Calculate the offset

    if high is None or low is None: return

    # Calculate HL2 Indicator (HL2 = (High + Low) ÷ 2 = arithmetical mean of High and Low prices)
    hl2_ = 0.5 * (high + low)
    if offset != 0:
        hl2_ = hl2_.shift(offset)

    highest_hl2 = hl2_.rolling(length).max()
    lowest_hl2 = hl2_.rolling(length).min()

    hlr = high_low_range(highest_hl2, lowest_hl2)
    hlr[hlr < 0.001] = 0.001

    position = ((hl2_ - lowest_hl2) / hlr) - 0.5

    v = 0
    m = high.size
    result = [np.nan for _ in range(0, length - 1)] + [0]
    for i in range(length, m):
        v = 0.66 * position.iloc[i] + 0.67 * v
        if v < -0.99: v = -0.999
        if v > 0.99: v = 0.999
        result.append(0.5 * (np.log((1 + v) / (1 - v)) + result[i - 1]))
    fisher = Series(result, index=high.index)
    signalma = fisher.shift(signal)

    # Adjust values to offset
    if offset != 0:
        fisher = fisher.shift(offset)
        signalma = signalma.shift(offset)

    # Data processing ( remove NaN values )
    if "fillna" in kwargs:
        fisher.fillna(kwargs["fillna"], inplace=True)
        signalma.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        fisher.fillna(method=kwargs["fill_method"], inplace=True)
        signalma.fillna(method=kwargs["fill_method"], inplace=True)

    # Prepare DataFrame to return
    data = {"FISHER": fisher, "FISHER_SIGNAL": signalma}
    df = DataFrame(data)

    return df
