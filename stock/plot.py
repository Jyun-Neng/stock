import plotly.express as px
import pandas as pd


class Plot():
    """
    Data visulization
    """

    def plot2DHist(self, df: object):
        """Plot histogram.

        Args:
            df: pandas DataFrame object contains two columns with x-axis and 
                y-axis informations.
        """
        labels = df.columns
        fig = px.bar(df, x=labels[0], y=labels[1])
        fig.show()