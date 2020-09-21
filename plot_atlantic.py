"""
Plotting script for the Atlantic's COVID Tracking Project's data.
"""

import argparse
from matplotlib import pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np

from plot_utils import standard_covid_plot, hospitalizations_plot, plot_bar, \
        plot_line, plot_estimated_daily_infections

mpl.rcParams['text.usetex'] = False


def plot_state_covidtracking(state):
    """ Plot COVID Tracking Project data for a given state. """

    dates = []
    cases = []
    deaths = []
    hospitalized = []

    # Read CSV file
    csv_df = pd.read_csv('./covidtracking-data/state-daily.csv')
    state_df = csv_df.loc[csv_df['state'] == state]

    dates_int = np.flip(state_df['date'].to_numpy())
    cases = np.flip(state_df['positive'].to_numpy())
    deaths = np.flip(state_df['death'].to_numpy())
    hospitalized = np.flip(state_df['hospitalizedCurrently'].to_numpy())
    icu = np.flip(state_df['inIcuCurrently'].to_numpy())
    positives = np.flip(state_df['positive'].to_numpy())
    negatives = np.flip(state_df['negative'].to_numpy())

    dates = []
    for date_int in dates_int:
        dates.append(str(date_int)[4:6] + '/' + str(date_int)[6:8])
    dates = np.array(dates)

    cases[pd.isnull(cases)] = 0
    deaths[pd.isnull(deaths)] = 0
    hospitalized[pd.isnull(hospitalized)] = 0
    icu[pd.isnull(icu)] = 0
    positives[pd.isnull(positives)] = 0
    negatives[pd.isnull(negatives)] = 0

    if len(dates) == 0:
        print("Could not find any entries for the state of " + state + ".")
        return

    standard_covid_plot("COVID Tracking Project Data (The Atlantic)", state, dates, cases, deaths)

    hospitalizations_plot(state, dates, hospitalized, icu)

    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(12, 8))

    positives = np.diff(positives, prepend=0)
    negatives = np.diff(negatives, prepend=0)
    plot_bar("COVID-19 Test Results",
             axes,
             dates,
             [negatives, positives],
             ["Number of negatives", "Number of positives"],
             ["green", "red"],
             "Date",
             "Count",
             "avg")
    fig.tight_layout()
    plt.show()

    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(12, 8))

    plot_bar("COVID-19 Test Results",
             axes,
             dates,
             [100.*(positives / (positives + negatives + 1e-19))],
             ["Percent positive"],
             ["green"],
             "Date",
             "Percent",
             "avg")
    fig.tight_layout()
    plt.show()

    d_cases = np.diff(cases, 1)
    d_cases = np.insert(d_cases, 0, 0, axis=0)
    test_positivity = positives / (positives + negatives + 1e-19)
    test_positivity = np.array(test_positivity, dtype=np.float32)
    plot_estimated_daily_infections(state, dates, test_positivity, d_cases)


def main():
    """ Main function. """

    parser = argparse.ArgumentParser(
        description="Plot the Atlantic's COVID Tracking Project COVID-19 data")
    parser.add_argument("state")
    args = parser.parse_args()

    plt.style.use("ggplot")

    plot_state_covidtracking(args.state)


main()
