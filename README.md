# hl_utils

get_xc_from_pp_csv.py calculates exchange rates from PayPal csv files (which have 2-records per currency conversion).
Test as follows:
$ git clone git@github.com:soccja/hl_utils.git
$ chmod +x get_xc_from_pp_csv.py (linux/bsd)
$ cat test.csv| get_xc_from_pp_csv.py OR
$ get_xc_from_pp_csv.py test.csv
