import pandas as pd
import pint
import pint_pandas


class Performance:
    def __init__(self, df: pd.DataFrame, max_power):
        self.raw_df = df
        self.max_power = max_power
        self.max_rpm = self._get_max_rpm()
        self.perfomance_df = self.get_perfomance_df()

    def _get_max_rpm(self):
        peak_powers = (
            self.raw_df.pint.quantify().groupby("rpm", axis=0).max().Power
        )  # Get pandas series with peak power by rpm
        for i in range(0, len(peak_powers)):
            if peak_powers[peak_powers.index[i]] <= self.max_power:
                max_rpm = peak_powers.index[i]
        return max_rpm

    def get_perfomance_df(self):
        return (
            self.raw_df.pint.quantify()
            .loc[self.raw_df.pint.quantify().rpm == self.max_rpm]
            .pint.dequantify()
        )
