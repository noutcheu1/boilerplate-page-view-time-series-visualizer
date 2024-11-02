import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean data
df['value'] = pd.to_numeric(df['value'], errors='coerce')

# Drop NaN values if they exist
df = df.dropna(subset=['value'])
df = df[
    (df['value'] >= df['value'].quantile(0.025))
    & (df['value'] <= df['value'].quantile(0.975))
]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(16, 6))
    ax.plot(df.index, df['value'], color='red')
    ax.set(xlabel='Date', ylabel='Page Views', title='Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()
    
    # Group by year and month, then calculate the mean
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Reorder the months for plotting
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    
    # Ensure the months are ordered properly
    df_bar = df_bar[month_order]
    
    # Draw bar plot
    fig, ax = plt.subplots(figsize=(16, 6))
    df_bar.plot(kind='bar', ax=ax)
    ax.set_ylabel('Average Page Views')
    ax.set_xlabel('Years')
    ax.set_title('Average Page Views per Month')
    ax.legend(title='Months', bbox_to_anchor=(1.05, 1))

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots
    df_box = df.copy()
    
    # Add 'year' and 'month' columns
    df_box['year'] = df_box.index.year
    df_box['month'] = df_box.index.strftime('%b')  # Short month names
    # df_box = df_box.groupby(['year', 'month'])['value'].mean().unstack()

    # Reorder the months for plotting
    
    # Draw box plots using Seaborn
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
    # Create the boxplot with month on x-axis and value on y-axis
    sns.boxplot(x='year', palette='Set3', y='value', data=df_box, ax=ax1)
    
    ax1.set_ylabel('Page Views')
    ax1.set_xlabel('Year')
    ax1.set_title('Year-wise Box Plot (Trend)')
    sns.boxplot(x='month', palette='Set3', y='value', data=df_box, ax=ax2, order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                                                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    
    ax2.set_ylabel('Page Views')
    ax2.set_xlabel('Month')
    ax2.set_title('Month-wise Box Plot (Seasonality)')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
