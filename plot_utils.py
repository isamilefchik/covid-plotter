"""
Convenience functions for graphing using matplotlib.
"""

import numpy as np
from scipy.signal import savgol_filter
from matplotlib import pyplot as plt


# Visual elements
FIGURE_TITLE_FONTSIZE = 16
TITLE_FONTSIZE = 9
AXIS_LABEL_FONTSIZE = 9
LEGEND_FONTSIZE = 8
NUM_TICKS = 10

# Savitsky-Golay smoothing filter parameters
WINDOW_SIZE = 25
POLYORDER = 2

# Average filter parameters
AVG_WINDOW = 7

# Default smoothing method
DEFAULT_SMOOTHING = 'avg'


def plot_line(title, axis, x_vals, y_vals_set, line_labels,
              line_colors, xlabel, ylabel):
    """
    Plot line graph.

    title        - Title of graph
    axis         - Axis object to graph on (plt subplot)
    x_vals       - x coordinates of data points (same for all y vals)
    y_vals_set   - Set of y coordinates of data points;
                   len(y_vals_set) == number of lines
    line_labels  - Labels for each line
    line_colors  - Colors for each line
    xlabel       - Label for x axis
    ylabel       - Label for y axis

    Return: None
    """

    axis.set_title(title, fontsize=TITLE_FONTSIZE)
    axis.set_xlabel(xlabel, fontsize=AXIS_LABEL_FONTSIZE)
    axis.set_ylabel(ylabel, fontsize=AXIS_LABEL_FONTSIZE)

    for i, y_vals in enumerate(y_vals_set):
        axis.plot(x_vals, y_vals, marker=".",
                  label=line_labels[i], color=line_colors[i])

    axis.set_xticks(np.arange(0, len(x_vals), step=len(x_vals)/NUM_TICKS))
    axis.legend(loc=2, fontsize=LEGEND_FONTSIZE)


def plot_bar(title, axis, x_vals, y_vals_set, bar_labels,
             bar_colors, xlabel, ylabel, smooth='none'):
    """
    Plot bar graph.

    title        - Title of graph
    axis         - Axis object to graph on (plt subplot)
    x_vals       - x coordinates of data points (same for all y vals)
    y_vals_set   - Set of y coordinates of data points;
                   len(y_vals_set) == number of lines
    line_labels  - Labels for each line
    line_colors  - Colors for each line
    xlabel       - Label for x axis
    ylabel       - Label for y axis
    smooth       - One of the following options:
                    * 'savgol' - Savitsky-Golay smoothing
                    * 'avg'    - 7-day rolling average
                    * 'none'   - No smoothed line plotted

    Returns: None
    """

    axis.set_title(title, fontsize=TITLE_FONTSIZE)
    axis.set_xlabel(xlabel, fontsize=AXIS_LABEL_FONTSIZE)
    axis.set_ylabel(ylabel, fontsize=AXIS_LABEL_FONTSIZE)

    for i, y_vals, in enumerate(y_vals_set):
        axis.bar(x_vals, y_vals, label=bar_labels[i], color=bar_colors[i], alpha=0.8)

        # Calculate smooth line coordinates
        if smooth != 'none':
            x_smooth = np.copy(x_vals)

            if smooth == 'savgol':
                y_smooth = savgol_filter(y_vals, WINDOW_SIZE, POLYORDER)

            elif smooth == 'avg':
                y_smooth = []
                for j, _ in enumerate(y_vals[AVG_WINDOW-1:]):
                    frame_avg = sum(y_vals[j:j+AVG_WINDOW]) / float(AVG_WINDOW)
                    y_smooth.append(frame_avg)
                y_smooth = np.array(y_smooth)
                x_smooth = x_smooth[AVG_WINDOW//2:-(AVG_WINDOW//2)]

            axis.plot(x_smooth,
                      y_smooth,
                      #  label=bar_labels[i] + " smoothed",
                      color=get_smooth_color(bar_colors[i]))

    axis.set_xticks(np.arange(0, len(x_vals), step=len(x_vals)/NUM_TICKS))
    axis.legend(loc=2, fontsize=LEGEND_FONTSIZE)


def get_smooth_color(bar_color):
    """
    Returns corresponding smoothing line color given the bar color.
    """

    if bar_color in ["red", "lightcoral"]:
        return "crimson"

    if bar_color in ["black"]:
        return "midnightblue"

    if bar_color in ["dimgray", "dimgrey", "gray", "grey", "darkgrey",
                     "darkgray", "silver", "lightgray", "lightgrey", "gainsboro"]:
        return "black"

    if bar_color in ["green"]:
        return "limegreen"

    # Default average line color
    return "moccasin"


def standard_covid_plot(title, location, dates, c_nums, d_nums):
    """
    Standard routine for plotting covid data.

    title    - String indicating title for entire figure.
    location - String indicating the location of the data (e.g. country or state or city)
    dates    - List of dates of data (x-values of plot)
    c_nums   - List of cumulative number of cases (daily)
    d_nums   - List of cumulative number of deaths (daily)

    Returns: None
    """
    fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(12, 8))

    for i in range(3):
        for j in range(2):
            axes[i, j].tick_params(labelsize=8)

    def plot_cumulatives():
        plot_bar(title=location + " COVID-19 Cumulative Confirmed Cases/Deaths",
                 axis=axes[0, 0],
                 x_vals=dates,
                 y_vals_set=[c_nums, d_nums],
                 bar_labels=["cases", "deaths"],
                 bar_colors=["lightcoral", "gray"],
                 xlabel="date",
                 ylabel="# of cases or deaths",
                 smooth=DEFAULT_SMOOTHING)

        plot_bar(title=location + " COVID-19 Cumulative Confirmed Deaths",
                 axis=axes[0, 1],
                 x_vals=dates,
                 y_vals_set=[d_nums],
                 bar_labels=["deaths"],
                 bar_colors=["gray"],
                 xlabel="date",
                 ylabel="# of deaths",
                 smooth=DEFAULT_SMOOTHING)

    def plot_derivs():

        # ======================================
        # 1st Derivatives
        # ======================================

        c_derivs = []
        d_derivs = []

        for i, _ in enumerate(c_nums[1:]):
            c_derivs.append(c_nums[i+1]-c_nums[i])

        for i, _ in enumerate(d_nums[1:]):
            d_derivs.append(d_nums[i+1]-d_nums[i])

        plot_bar(title=location + " COVID-19 Confirmed Cases/Deaths 1st Deriv.",
                 axis=axes[1, 0],
                 x_vals=dates[1:],
                 y_vals_set=[c_derivs, d_derivs],
                 bar_labels=["d_cases", "d_deaths"],
                 bar_colors=["lightcoral", "gray"],
                 xlabel="date",
                 ylabel="# of cases or deaths / day",
                 smooth=DEFAULT_SMOOTHING)

        plot_bar(title=location + " COVID-19 Confirmed Deaths 1st Deriv.",
                 axis=axes[1, 1],
                 x_vals=dates[1:],
                 y_vals_set=[d_derivs],
                 bar_labels=["d_deaths"],
                 bar_colors=["gray"],
                 xlabel="date",
                 ylabel="# of deaths / day",
                 smooth=DEFAULT_SMOOTHING)

        # ======================================
        # 2nd Derivatives
        # ======================================

        c_2derivs = []
        d_2derivs = []

        for i, _ in enumerate(c_derivs[1:]):
            c_2derivs.append(c_derivs[i+1]-c_derivs[i])

        for i, _ in enumerate(d_derivs[1:]):
            d_2derivs.append(d_derivs[i+1]-d_derivs[i])

        plot_bar(title=location + " COVID-19 Confirmed Cases/Deaths 2nd Deriv.",
                 axis=axes[2, 0],
                 x_vals=dates[2:],
                 y_vals_set=[c_2derivs, d_2derivs],
                 bar_labels=["d2_cases", "d2_deaths"],
                 bar_colors=["lightcoral", "gray"],
                 xlabel="date",
                 ylabel=r"# of cases or deaths / ${\mathrm{day}}^2$",
                 smooth=DEFAULT_SMOOTHING)

        plot_bar(title=location + " COVID-19 Confirmed Deaths 2nd Deriv.",
                 axis=axes[2, 1],
                 x_vals=dates[2:],
                 y_vals_set=[d_2derivs],
                 bar_labels=["d2_deaths"],
                 bar_colors=["gray"],
                 xlabel="date",
                 ylabel=r"# of deaths / ${\mathrm{day}}^2$",
                 smooth=DEFAULT_SMOOTHING)

    plot_cumulatives()
    plot_derivs()

    fig.suptitle(title, fontsize=FIGURE_TITLE_FONTSIZE)
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()


def hospitalizations_plot(location, dates, h_nums, icu_nums):
    """
    Hospitalizations graphs.

    location - String indicating the location of the data (e.g. country or state or city)
    dates    - List of dates of data (x-values of plot)
    h_nums   - List of cumulative number of cases (daily)
    d_nums   - List of cumulative number of deaths (daily)

    Returns: None
    """

    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))

    for i in range(2):
        for j in range(2):
            axes[i, j].tick_params(labelsize=8)

    def plot_cumulatives():
        plot_bar(title=location + " COVID-19 Active Hospitalizations",
                 axis=axes[0, 0],
                 x_vals=dates,
                 y_vals_set=[h_nums, icu_nums],
                 bar_labels=["hospital", "ICU"],
                 bar_colors=["lightcoral", "gray"],
                 xlabel="date",
                 ylabel="# of people",
                 smooth=DEFAULT_SMOOTHING)

        plot_bar(title=location + " COVID-19 Active ICU Occupancy",
                 axis=axes[0, 1],
                 x_vals=dates,
                 y_vals_set=[icu_nums],
                 bar_labels=["ICU"],
                 bar_colors=["gray"],
                 xlabel="date",
                 ylabel="# of people",
                 smooth=DEFAULT_SMOOTHING)

    def plot_derivs():

        # ======================================
        # 1st Derivatives
        # ======================================

        h_derivs = []
        icu_derivs = []

        for i, _ in enumerate(h_nums[1:]):
            h_derivs.append(h_nums[i+1]-h_nums[i])

        for i, _ in enumerate(icu_nums[1:]):
            icu_derivs.append(icu_nums[i+1]-icu_nums[i])

        plot_bar(title=location + " COVID-19 Active Hospitalizations 1st Deriv.",
                 axis=axes[1, 0],
                 x_vals=dates[1:],
                 y_vals_set=[h_derivs, icu_derivs],
                 bar_labels=["d_cases", "d_deaths"],
                 bar_colors=["lightcoral", "gray"],
                 xlabel="date",
                 ylabel="# of cases or deaths / day",
                 smooth=DEFAULT_SMOOTHING)

        plot_bar(title=location + " COVID-19 Active ICU Occupancy 1st Deriv.",
                 axis=axes[1, 1],
                 x_vals=dates[1:],
                 y_vals_set=[icu_derivs],
                 bar_labels=["d_ICU"],
                 bar_colors=["gray"],
                 xlabel="date",
                 ylabel="# of people / day",
                 smooth=DEFAULT_SMOOTHING)

    plot_cumulatives()
    plot_derivs()

    fig.tight_layout()
    plt.show()


def plot_estimated_daily_infections(location, dates, test_positivity_series, cases):
    """
    Estimated daily infections graphs.

    location                - String indicating the location of the data (e.g. country or state or city)
    dates                   - List of dates of data (x-values of plot)
    test_positivity_series  - Numpy array of (# positive tests)/(# of total tests) per day
    cases                   - Numpy array of number of new cases (daily)

    Returns: None
    """

    fig, axis = plt.subplots(nrows=1, ncols=1, figsize=(12, 8))

    prevalence_ratio = (np.sqrt(test_positivity_series) * 16) + 2.5

    daily_new_infections = prevalence_ratio * cases

    plot_bar(title=location + " COVID-19 Estimated Daily New Infections",
             axis=axis,
             x_vals=dates,
             y_vals_set=[daily_new_infections],
             bar_labels=["New infections"],
             bar_colors=["lightcoral"],
             xlabel="data",
             ylabel="# of new infections per day",
             smooth=DEFAULT_SMOOTHING)

    fig.tight_layout()
    plt.show()
