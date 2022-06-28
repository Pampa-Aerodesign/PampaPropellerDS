"""
Generic Dataframe Manipulation functions.
"""

import pandas as pd
import pint_pandas

NULL_UNITS = ["-", "(Adv Ratio)", "RPM"]


def fix_column_units(df: pd.DataFrame) -> pd.DataFrame:
    columns_list = df.columns.to_list()
    units_list = df.iloc[0].to_list()
    NULL_UNITS = ["-", "(Adv Ratio)", "RPM"]
    for i in range(0, len(columns_list)):
        unit = units_list[i]
        if unit in NULL_UNITS:
            unit = "(-)"
        columns_list[i] = columns_list[i] + " " + unit  # add units to columns
    df.columns = columns_list
    return df.drop(0)  # Remove first row which contained units


def raw_df_to_SI_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.apply(pd.to_numeric)
    df["V ()"] = df["V"] * 0.44704
    df["PWR"] = df["PWR"]
    df["Torque"] = df["Torque"] * 0.113
    df["Thrust"] = df["Thrust"] * 4.48
    return df


def raw_df_to_units_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop(0)
    df = df.apply(pd.to_numeric, errors="ignore")
    return pd.DataFrame(
        {
            "Velocity": pd.Series(df["V"], dtype="pint[mile / hour]"),
            "Advance Ratio": pd.Series(df["J"], dtype="pint[dimensionless]"),
            "Pe": pd.Series(df["Pe"], dtype="pint[dimensionless]"),
            "Ct": pd.Series(df["Ct"], dtype="pint[dimensionless]"),
            "Cp": pd.Series(df["Cp"], dtype="pint[dimensionless]"),
            "Power": pd.Series(df["PWR"], dtype="pint[horsepower]"),
            "Torque": pd.Series(df["Torque"], dtype="pint[lbf*in]"),
            "Thrust": pd.Series(df["Thrust"], dtype="pint[lbf]"),
            "rpm": pd.Series(df["RPM"], dtype="pint[rpm]"),
        }
    ).pint.dequantify()
