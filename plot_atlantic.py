"""
Plotting script for the Atlantic's COVID Tracking Project's data.
"""

import argparse
from matplotlib import pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np

from plot_utils import standard_covid_plot, hospitalizations_plot, plot_bar, plot_line

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
    state_df = state_df.to_numpy()

    dates = np.flip(state_df[:, 0], 0)
    cases = np.flip(state_df[:, 2], 0)
    deaths = np.flip(state_df[:, 16], 0)
    hospitalized = np.flip(state_df[:, 5], 0)
    icu = np.flip(state_df[:, 7], 0)
    positives = np.flip(state_df[:, 2], 0)
    negatives = np.flip(state_df[:, 3], 0)

    for i, _ in enumerate(dates):
        dates[i] = str(dates[i])[4:6] + '/' + str(dates[i])[6:8]

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

    plot_bar("COVID-19 Test Results",
             axes,
             dates,
             [negatives, positives],
             ["Number of negatives", "Number of positives"],
             ["green", "red"],
             "Date",
             "Number",
             "avg")
    fig.tight_layout()
    plt.show()

    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(12, 8))

    plot_bar("COVID-19 Test Results",
             axes,
             dates,
             [positives / (positives + negatives)],
             ["Percent positive"],
             ["green"],
             "Date",
             "Number",
             "avg")
    fig.tight_layout()
    plt.show()


def main():
    """ Main function. """

    parser = argparse.ArgumentParser(
        description="Plot the Atlantic's COVID Tracking Project COVID-19 data")
    parser.add_argument("state")
    args = parser.parse_args()

    plt.style.use("ggplot")

    plot_state_covidtracking(args.state)


main()
