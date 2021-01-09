import argparse
from datetime import datetime
from stock import analytics

if __name__ == "__main__":
    args = argparse.Namespace(id="2885",
                                   year=2021,
                                   month=1,
                                   url="127.0.0.1",
                                   port=27017)
    analytics = analytics.Analytics(args)
    r_cnt_list = analytics.raisingDays()
    f_cnt_list = analytics.fallingDays()
    analytics.rasingFallingDaysStatistic()