import pandas as pd
import pint
import pint_pandas


class Performance:
    """Analyze the performance of the propeller-engine pair.
    """
    def __init__(self, df: pd.DataFrame, max_power):
        """Initialize the Performance class

        Args:
            df (pd.DataFrame): Raw DataFrame with performance data.
            max_power (_type_): Maximum power of the engine.
        """        
        self.raw_df = df
        self.max_power = max_power
        self.max_rpm = self._get_max_rpm()
        self.perfomance_df = self.get_perfomance_df()

    def _get_max_rpm(self):
        """Get the maximum RPM of the engine limited by the maximum power. i.e. largest RPM such that df[df[Power]<=max_power]

        Returns:
            _type_: _description_
        """        
        peak_powers = (
            self.raw_df.pint.quantify().groupby("rpm", axis=0).max().Power
        )  # Get pandas series with peak power by rpm
        for i in range(0, len(peak_powers)): #Pandas syntax doesnt work here
            if peak_powers[peak_powers.index[i]] <= self.max_power:
                max_rpm = peak_powers.index[i]
        return max_rpm

    def get_perfomance_df(self) -> pd.DataFrame:
        """Get a slice of the DataFrame where rpm==max_rpm.

        Returns:
            pd.DataFrame: Performance DataFrame.
        """        
        return (
            self.raw_df.pint.quantify()
            .loc[self.raw_df.pint.quantify().rpm == self.max_rpm]
            .pint.dequantify()
        )
