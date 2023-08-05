from pkg_resources import resource_stream

from ..stats import read_excel

xlsstream = resource_stream(__name__, "../data/MastinData.xlsx")

Mastin = read_excel(xlsstream, name="Mastin", MER="MER", Height="Plume height")
