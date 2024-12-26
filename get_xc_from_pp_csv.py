#! /bin/env python3

# get_xcr_from_pp_csv.py calculates exchange rates from paypal csv file
# There are 2 records per currency conversion.

# The exchange-rate is got by:
# - importing the csv into a pandas data-frame (df)
# - sorting by date-time and with default currency coming first
#   ! Assumes all 2-record conversions have the same date-time.
# - For each 2-record conversion transaction:
#   - calculate exchange rate as abs(foreign_currency / default_currency)
#   - construct and return P-directive
# All constructed P-directives are then output
# Output is in P-directive format

# Example:

# - Input
# "Date","Time","Time Zone","Description","Currency","Gross","Fee","Net","Balance","Transaction ID"
# "07/08/2023","14:05:07","Australia/Sydney","General currency conversion","AUD","-87.60","0.00","-87.60","0.00","001"
# "10/06/2024","11:08:07","Australia/Sydney","General currency conversion","AUD","-41.53","0.00","-41.53","0.00","002"
# "07/08/2023","14:05:07","Australia/Sydney","General currency conversion","USD","55.00","0.00","55.00","0.00","003"
# "10/06/2024","11:08:07","Australia/Sydney","General currency conversion","USD","26.22","0.00","26.22","0.00","004"

# - Output
# P 07/08/2023 14:05:07 USD 1.5927272727272725
# P 10/06/2024 11:08:07 USD 1.5839054157131962

# Notes:
# - Default currency must be set within the program (See CHANGEME)
# - Accepts stdin as input

import sys
import pandas as pd

from pathlib import Path

default_currency = "AUD"  # CHANGEME
df = None
def_amt = 0

usage = "Usage: get_xc_from_pp_csv.py <filename>"


def set_sort_flag(x):

    if x["Currency"] == default_currency:
        return 0
    else:
        return 1


def p_directive(x):

    global def_amt
    amt = x["Gross"]

    if x["Currency"] == default_currency:
        def_amt = amt
        return None
    else:
        xr = abs(def_amt / amt)
        return f"P {x['Date']} {x['Time']} {x['Currency']} {xr}"


if __name__ == "__main__":

    argc = len(sys.argv)
    if argc == 1:
        fn = sys.stdin
    elif argc == 2:
        fn = sys.argv[1]
        if not Path(fn).is_file():
            print(f"{fn} not found or is not a file. Exiting")
            exit(1)
    else:
        print(usage)
    df = pd.read_csv(fn)
    df_ = df[df["Description"] == "General currency conversion"][
        ["Date", "Time", "Time Zone", "Currency", "Gross"]
    ]
    df_["sort_idx"] = df_.apply(set_sort_flag, axis=1)
    df_ = df_.sort_values(by=["Date", "Time", "Time Zone", "sort_idx", "Currency"])
    df_["p_directive"] = df_.apply(p_directive, axis=1)
    df_ = df_[~df_["p_directive"].isnull()]
    print(df_.p_directive.to_string(index=False))

    exit(0)
