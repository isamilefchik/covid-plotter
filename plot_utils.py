"""
Convenience functions for graphing using matplotlib.
"""

import numpy as np
from matplotlib import pyplot as plt

TITLE_FONTSIZE = 9
AXIS_LABEL_FONTSIZE = 9
X_TICK_STEPS = 10

def plot_line(title, axis, x_vals, y_vals_set, line_labels, line_colors, xlabel, ylabel):
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
        axis.plot(x_vals, y_vals, marker=".", label=line_labels[i], color=line_colors[i])

    axis.set_xticks(np.arange(0, len(x_vals), step=X_TICK_STEPS))
    axis.legend()

def plot_bar(title, axis, x_vals, y_vals_set, bar_labels, bar_colors, xlabel, ylabel, plot_avg):
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
    plot_avg     - Whether to calculate and plot 7-day averages

    Returns: None
    """

    axis.set_title(title, fontsize=TITLE_FONTSIZE)
    axis.set_xlabel(xlabel, fontsize=AXIS_LABEL_FONTSIZE)
    axis.set_ylabel(ylabel, fontsize=AXIS_LABEL_FONTSIZE)

    for i, y_vals, in enumerate(y_vals_set):
        axis.bar(x_vals, y_vals, label=bar_labels[i], color=bar_colors[i])

        if plot_avg:
            avg_vals = []

            # Calc 7-day avgs
            for j, _ in enumerate(y_vals):
                day_set = y_vals[max(0, j-3) : min(len(y_vals), j+4)]
                avg_vals.append(sum(day_set) / len(day_set))

            axis.plot(x_vals, avg_vals, label=bar_labels[i] + " avg.",
                      color=get_avg_color(bar_colors[i]))

    axis.set_xticks(np.arange(0, len(x_vals), step=X_TICK_STEPS))
    axis.legend()

def get_avg_color(bar_color):
    """
    Returns corresponding 7-day average line color given the bar color.
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

def standard_covid_plot(location, dates, c_nums, d_nums):
    """
    Standard routine for plotting covid data.

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
        plot_bar(title      = location + " COVID-19 Cumulative Confirmed Cases/Deaths",
                 axis       = axes[0, 0],
                 x_vals     = dates,
                 y_vals_set = [c_nums, d_nums],
                 bar_labels = ["cases", "deaths"],
                 bar_colors = ["lightcoral", "gray"],
                 xlabel     = "date",
                 ylabel     = "# of cases or deaths",
                 plot_avg   = True)

        plot_bar(title      = location + " COVID-19 Cumulative Confirmed Deaths",
                 axis       = axes[0, 1],
                 x_vals     = dates,
                 y_vals_set = [d_nums],
                 bar_labels = ["deaths"],
                 bar_colors = ["gray"],
                 xlabel     = "date",
                 ylabel     = "# of deaths",
                 plot_avg   = True)

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

        plot_bar(title      = location + " COVID-19 Confirmed Cases/Deaths 1st Deriv.",
                 axis       = axes[1, 0],
                 x_vals     = dates[1:],
                 y_vals_set = [c_derivs, d_derivs],
                 bar_labels = ["d_cases", "d_deaths"],
                 bar_colors = ["lightcoral", "gray"],
                 xlabel     = "date",
                 ylabel     = "# of cases or deaths / day",
                 plot_avg   = True)

        plot_bar(title      = location + " COVID-19 Confirmed Deaths 1st Deriv.",
                 axis       = axes[1, 1],
                 x_vals     = dates[1:],
                 y_vals_set = [d_derivs],
                 bar_labels = ["d_deaths"],
                 bar_colors = ["gray"],
                 xlabel     = "date",
                 ylabel     = "# of deaths / day",
                 plot_avg   = True)

        # ======================================
        # 2nd Derivatives
        # ======================================

        c_2derivs = []
        d_2derivs = []

        for i, _ in enumerate(c_derivs[1:]):
            c_2derivs.append(c_derivs[i+1]-c_derivs[i])

        for i, _ in enumerate(d_derivs[1:]):
            d_2derivs.append(d_derivs[i+1]-d_derivs[i])

        plot_bar(title      = location + " COVID-19 Confirmed Cases/Deaths 2nd Deriv.",
                 axis       = axes[2, 0],
                 x_vals     = dates[2:],
                 y_vals_set = [c_2derivs, d_2derivs],
                 bar_labels = ["d2_cases", "d2_deaths"],
                 bar_colors = ["lightcoral", "gray"],
                 xlabel     = "date",
                 ylabel     = r"# of cases or deaths / ${\mathrm{day}}^2$",
                 plot_avg   = True)

        plot_bar(title      = location + " COVID-19 Confirmed Deaths 2nd Deriv.",
                 axis       = axes[2, 1],
                 x_vals     = dates[2:],
                 y_vals_set = [d_2derivs],
                 bar_labels = ["d2_deaths"],
                 bar_colors = ["gray"],
                 xlabel     = "date",
                 ylabel     = r"# of deaths / ${\mathrm{day}}^2$",
                 plot_avg   = True)

    plot_cumulatives()
    plot_derivs()

    fig.tight_layout()
    plt.show()
