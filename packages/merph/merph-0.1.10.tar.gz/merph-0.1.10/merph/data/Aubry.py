import pandas as pd
from pkg_resources import resource_stream

# from ..stats import QHstats, Date, Time, Duration, DateTime, HeightObs, Refs
from ..stats import QHstats, read_excel

xlsstream = resource_stream(__name__, "../data/AubryData.xlsx")

df = pd.read_excel(xlsstream)

df["MER (kg/s)"] = df["Erupted tephra mass (kg)"] / (df["Duration (hrs)"] * 3600)
# df['H'] = df['Vent altitude (m a.s.l.)']/1000 + df['Plume height (km a.v.l.)']

df["Name"] = df["Volcano"].combine(
    df["Eruption"], lambda a, b: a + " " + (str(b) or "")
)
df["Eruption"] = df["Volcano"].combine(
    df["Eruption"], lambda a, b: a + " " + (str(b) or "")
)

Aubry = QHstats(df, name="Aubry", MER="MER", Height="Plume height")
