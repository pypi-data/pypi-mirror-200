from pkg_resources import resource_stream

# from ..stats import QHstats, Date, Time, Duration, DateTime, HeightObs, Refs
from ..stats import read_csv, read_excel, QHstats

xlsstream = resource_stream(__name__, '../data/SparksData.xlsx')

Sparks=read_excel(xlsstream, name='Sparks', MER='MER', Height='Plume height')

# csvstream = resource_stream(__name__, '../data/SparksData.csv')
# 
# Sparks=read_csv(csvstream, name='Sparks', MER='MER', Height='Height')
