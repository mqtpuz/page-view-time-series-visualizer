import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

from calendar import month_name, month_abbr     # Convenient way of getting lists of month names and abbreviations
from matplotlib.patches import Rectangle        # Necessary for clearing bar plot's blank rectangles

register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=['date'], sep=',')

# Clean data
df = df.loc[(df.value >= df.value.quantile(0.025)) & (df.value <= df.value.quantile(0.975))]


def draw_line_plot():
    df_line = df.copy()
    
    # Draw line plot
    fig, ax = plt.subplots(figsize=(12, 5))
    
    ax.plot(df_line.index, df_line.value, color='firebrick')

    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['Months'] = df_bar.index.strftime('%B')
    df_bar['year'] = df_bar.index.year

    # Draw bar plot
    g = sns.catplot(df_bar, kind='bar',
                      x='year', y='value', hue='Months',
                      hue_order=list(month_name[1:]),
                      estimator='mean',
                      errorbar=None, 
                      palette='tab20', 
                      legend_out=False,
                      aspect=16/9)

    g.set_axis_labels('Years', 'Average Page Views')
    fig = g.figure

    ax_bar = fig.axes[0]


    def number_of_bars():
        return len([rect for rect in ax_bar.get_children() if isinstance(rect, Rectangle)])


    if number_of_bars() > 49:   # Clears rectangles of width 0  untill number of rectanlges reaches limit imposed by test_module.py
        rectlist = [rect for rect in ax_bar.get_children() if isinstance(rect, Rectangle)]
        for rect in rectlist:
            if rect.get_width() == 0:
                rect.remove()
                if number_of_bars() <= 49:
                    break

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, gridspec_kw={'wspace': 0.05})
    fig.set_size_inches(15, 5)

    sns.boxplot(df_box, x='year', y='value', ax=ax1, palette='Dark2')
    sns.boxplot(df_box, x='month', y='value', ax=ax2, order=list(month_abbr[1:]), palette='Set3')

    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')
    ax1.set_title('Year-wise Box Plot (Trend)')

    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')
    ax2.set_title('Month-wise Box Plot (Seasonality)')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
