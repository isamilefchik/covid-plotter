"""
Plotting script for the COVID19 data from data.ca.gov.
"""

import argparse
from matplotlib import pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
import urllib

from plot_utils import standard_covid_plot, hospitalizations_plot, \
        plot_bar, plot_line, plot_estimated_daily_infections

mpl.rcParams['text.usetex'] = False

DAYS_ACTIVE = 8

def plot_ca(county):

    hospital_data_url = "https://data.ca.gov/dataset/529ac907-6ba1-4cb7-" \
            + "9aae-8966fc96aeef/resource/42d33765-20fd-44b8-" \
            + "a978-b083b7542225/download/hospitals_by_county.csv"
    cases_data_url = "https://data.ca.gov/dataset/590188d5-8545-4c93-" \
            + "a9a0-e230f0db7290/resource/926fd08f-cc91-4828-af38-" \
            + "bd45de97f8c3/download/statewide_cases.csv"
    test_data_url = "https://data.ca.gov/dataset/efd6b822-7312-477c-" \
            + "922b-bccb82025fbe/resource/b6648a0d-ff0a-4111-b80b-" \
            + "febda2ac9e09/download/statewide_testing.csv"

    hospital_csv_df = pd.read_csv(hospital_data_url)
    cases_csv_df = pd.read_csv(cases_data_url)
    tests_csv_df = pd.read_csv(test_data_url)

    hospital_df = hospital_csv_df.loc[hospital_csv_df['county'] == county]
    cases_df = cases_csv_df.loc[cases_csv_df['county'] == county]
    hospital_df = hospital_df.to_numpy()
    cases_df = cases_df.to_numpy()
    tests_csv_df = tests_csv_df.to_numpy()

    cases = cases_df[:, 3]
    deaths = cases_df[:, 4]
    dates = cases_df[:, 5]

    active = np.zeros_like(cases)
    for i in range(0, DAYS_ACTIVE):
        active[i] = cases[i]
        if i != 0:
            active[i] += active[i-1]

    for i in range(DAYS_ACTIVE, len(cases)):
        active[i] = (cases[i] + active[i-1]) - cases[i-DAYS_ACTIVE]



    hospitalized = hospital_df[:, 2] + hospital_df[:, 3]
    icu = hospital_df[:, 6] + hospital_df[:, 7]

    padding = np.zeros(len(cases) - len(hospitalized))

    hospitalized = np.concatenate((padding, hospitalized), axis=0)
    icu = np.concatenate((padding, icu), axis=0)

    for i, _ in enumerate(dates):
        dates[i] = str(dates[i])[5:7] + '/' + str(dates[i])[8:10]

    hospitalized[pd.isnull(hospitalized)] = 0
    icu[pd.isnull(icu)] = 0
    cases[pd.isnull(icu)] = 0
    deaths[pd.isnull(hospitalized)] = 0

    if len(dates) == 0:
        print("Could not find any entries for the county of Los Angeles.")
        return

    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))

    plot_bar(county + " COVID-19 Data",
             axes[0, 0],
             dates,
             [active, hospitalized],
             ["Active", "Hospitalized"],
             ["green", "lightcoral"],
             "Date",
             "Number",
             "avg")

    plot_bar(county + " COVID-19 Data",
             axes[0, 1],
             dates,
             [hospitalized, icu],
             ["Hospitalized", "ICU"],
             ["lightcoral", "orange"],
             "Date",
             "Number",
             "avg")

    plot_bar(county + " COVID-19 Data",
             axes[1, 0],
             dates,
             [deaths],
             ["Deaths"],
             ["dimgray"],
             "Date",
             "Number",
             "avg")

    plot_bar(county + " COVID-19 Data",
             axes[1, 1],
             dates,
             [hospitalized, deaths],
             ["Hospitalized", "Deaths"],
             ["lightcoral", "dimgray"],
             "Date",
             "Number",
             "avg")

    fig.tight_layout()
    plt.show()

    cases = cases_df[:, 1]
    deaths = cases_df[:, 2]
    standard_covid_plot("CA Gov COVID19 Data - " + county, county, dates, cases, deaths)

    cases = cases_df[:, 3]
    tests = tests_csv_df[:, 1]

    test_positivity = cases / tests
    plot_estimated_daily_infections(county, dates, np.array(test_positivity, dtype=np.float32), cases)


def main():
    """ Main function. """
    parser = argparse.ArgumentParser(description="Plot California COVID-19 data")
    parser.add_argument("county", default="Los Angeles")
    args = parser.parse_args()

    plt.style.use("ggplot")
    plot_ca(args.county)


main()
