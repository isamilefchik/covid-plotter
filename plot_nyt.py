"""
Plotting script for NYT COVID-19 data.
"""

import csv
import argparse
from matplotlib import pyplot as plt
import matplotlib as mpl

from plot_utils import standard_covid_plot

mpl.rcParams['text.usetex'] = False

def plot_state_nyt(state):
    """ Plot NYT data for a given state. """

    c_nums = []
    d_nums = []
    dates = []

    # Read CSV file
    with open('./nyt-data/us-states.csv') as csvfile:
        read_csv = csv.reader(csvfile, delimiter=',')

        for row in read_csv:
            if row[1] in [state, state.title()]:
                if state != row[1]:
                    state = row[1]

                dates.append(row[0].split("-")[1] + "/" + row[0].split("-")[2])
                c_nums.append(row[3])
                d_nums.append(row[4])

    if len(dates) == 0:
        print("Could not find any entries for the state of " + state + ".")
        return

    for i, _ in enumerate(c_nums):
        c_nums[i] = int(c_nums[i])

    for i, _ in enumerate(d_nums):
        d_nums[i] = int(d_nums[i])

    standard_covid_plot("NYT COVID Data", state, dates, c_nums, d_nums)

def plot_county_nyt(state, county):
    """ Plot NYT data for a given county. """

    c_nums = []
    d_nums = []
    dates = []

    # Read CSV file
    with open('./nyt-data/us-counties.csv') as csvfile:
        read_csv = csv.reader(csvfile, delimiter=',')
        for row in read_csv:
            if row[2] in [state, state.title()]  and row[1] in [county, county.title()]:
                if state != row[2]:
                    state = row[2]
                if county != row[1]:
                    county = row[1]

                dates.append(row[0].split("-")[1] + "/" + row[0].split("-")[2])
                c_nums.append(row[4])
                d_nums.append(row[5])

    if len(dates) == 0:
        print("Could not find any entries for " + county + " County, " + state + ".")
        return

    for i, _ in enumerate(c_nums):
        c_nums[i] = int(c_nums[i])

    for i, _ in enumerate(d_nums):
        d_nums[i] = int(d_nums[i])

    standard_covid_plot("NYT COVID Data", county + " County, " + state, dates, c_nums, d_nums)

def main():
    """ Main function. """

    parser = argparse.ArgumentParser(description="Plot NYT COVID-19 data")
    parser.add_argument("--state", required=True)
    parser.add_argument("--county", default=None)
    args = parser.parse_args()

    plt.style.use("ggplot")

    if args.county is not None:
        plot_county_nyt(args.state, args.county)
    else:
        plot_state_nyt(args.state)

main()
