import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.figure
from matplotlib.dates import DateFormatter
from matplotlib.ticker import FuncFormatter, MaxNLocator
import numpy as np
from typing import Tuple

class StravaPlots:
    def __init__(self, activity_data):
        self.df = pd.DataFrame(activity_data)

    def monthly_training_time(self):
        # Convert the date to datetime and extract month and year
        self.df['start_date'] = pd.to_datetime(self.df['start_date'])
        self.df['month_year'] = self.df['start_date'].dt.to_period('M')
        self.df['elapsed_time'] = ((self.df['elapsed_time']/60)/60) # convert seconds to hours

        # Aggregate training time by month
        monthly_training = self.df.groupby('month_year')['elapsed_time'].sum() 

        # Plotting
        plt.figure(figsize=(10, 6))
        monthly_training.plot(kind='bar')
        plt.title('Monthly Time Spent Training')
        plt.xlabel('Month')
        plt.ylabel('Training Time (hours)')
        return plt
    
    def monthly_training_time_grouped(self):
        # Convert the date to datetime and extract month and year
        self.df['start_date'] = pd.to_datetime(self.df['start_date'])
        self.df['month'] = self.df['start_date'].dt.month
        self.df['year'] = self.df['start_date'].dt.year

        # Aggregate training time by month and year
        monthly_training = self.df.groupby(['year', 'month'])['elapsed_time'].sum()

        # Create a bar plot
        fig, ax = plt.subplots(figsize=(10, 6))
        monthly_training.unstack().plot(kind='bar', ax=ax)
        ax.set_title('Monthly Time Spent Training')
        ax.set_xlabel('Year')
        ax.set_ylabel('Training Time (hours)')
        ax.legend(title='Month')
        plt.xticks(rotation=45)
        return fig, ax

