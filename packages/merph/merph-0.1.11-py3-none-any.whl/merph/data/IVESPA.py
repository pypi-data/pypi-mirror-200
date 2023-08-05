import numpy as np
import pandas as pd
from pkg_resources import resource_stream

from ..stats import QHstats
from ..utilities.number_tools import isnumber

xlsstream = resource_stream(__name__, "../data/IVESPAData.xlsx")

df = pd.read_excel(xlsstream, header=[0, 1, 2], dtype=str, na_filter=False)  # type: ignore

col_types = df.columns.get_level_values(2)  # type: ignore
df.columns = df.columns.get_level_values(1)  # type: ignore

for col_name, col_type in zip(df.columns, col_types):  # type: ignore
    try:
        if col_type == "float":
            df[col_name] = df[col_name].replace(["unknown", "Unknown", "na", "NA"], np.NaN)  # type: ignore
            df[col_name] = df[col_name].astype(np.float64)  # type: ignore
        elif col_type == "int":
            df[col_name] = df[col_name].replace(["unknown", "Unknown", "na", "NA"], -1)  # type: ignore
            df[col_name] = df[col_name].astype(int)  # type: ignore
        elif col_type == "datetime":
            df[col_name] = pd.to_datetime(  # type: ignore
                df[col_name], format="dd/mm/yyyy hh:mm:ss", errors="coerce"  # type: ignore
            )
    except:
        raise ValueError(
            f"Could not convert type of column {col_name}.  Column values are: {df[col_name].values}"  # type: ignore
        )

df["MER (kg/s)"] = df["TEM Best estimate (kg)"] / (
    df["Duration Best estimate (hours)"] * 3600
)

df["Plume Height (km a.v.l.)"] = (
    df["Tephra Plume Top Best estimate (km a.s.l.)"]
    - df["Vent altitude (m a.s.l.)"] / 1000.0
)

df["Name"] = df["Volcano"].combine(  # type: ignore
    df["Event Name"], lambda a, b: a + " " + (str(b) or "")  # type: ignore
)
df["Eruption"] = df["Volcano"].combine(  # type: ignore
    df["Event Name"], lambda a, b: a + " " + (str(b) or "")  # type: ignore
)

df = df[df["Plume Height (km a.v.l.)"].notna()]
df = df[df["MER (kg/s)"].notna()]

IVESPA = QHstats(df, name="IVESPA", MER="MER", Height="Plume Height")
