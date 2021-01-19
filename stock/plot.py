import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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

    def plotPriceLine(self, prices: list, date_list: list):
        """Plot line chart of prices.

        Args:
            prices: a list of prices.
            date_list: stock trading date list.
        """
        fig = go.Figure(data=go.Scatter(x=date_list, y=prices))
        fig.show()

    def plotTradingVolume(self, volumes: list, date_list: list):
        """Plot line chart of trading volumes.

        Args:
            volumes: a list of trading volume.
            date_list: stock trading date list.
        """
        trace_vol = go.Scatter(x=date_list, y=volumes, line_shape="spline")
        fig = go.Figure(data=trace_vol)
        fig.show()

    def plotMA(self,
               ma: list,
               prices: list,
               date_list: list,
               show=True) -> list:
        """Plot line chart of moving average and price.

        Args:
            ma: a list includes 3 days, 5 days, 10 days, and 20 days MA
            prices: closing price list
            date_list: stock trading date list
            show: show the line chart
        Return:
            Trace list that plotly lib can use to plot chart.
        """
        trace_prices = go.Scatter(
            x=date_list, y=prices, name="price", line_shape="spline")
        trace_ma_3 = go.Scatter(
            x=date_list[3:], y=ma[0], name="ma_3", line_shape="spline")
        trace_ma_5 = go.Scatter(
            x=date_list[5:], y=ma[1], name="ma_5", line_shape="spline")
        trace_ma_10 = go.Scatter(
            x=date_list[10:], y=ma[2], name="ma_10", line_shape="spline")
        trace_ma_20 = go.Scatter(
            x=date_list[20:], y=ma[3], name="ma_20", line_shape="spline")
        traces = [
            trace_prices, trace_ma_3, trace_ma_5, trace_ma_10, trace_ma_20
        ]
        if show:
            fig = go.Figure(traces)
            fig.show()
        return traces

    def plotVA(self,
               ma: list,
               volume: list,
               date_list: list,
               show=True) -> list:
        """Plot line chart of moving average of trading volumes and trading volumes.

        Args:
            ma: a list includes 5 days, 10 days, and 20 days MA.
            prices: closing price list
            show: show the line chart
        Return:
            Trace list that plotly lib can use to plot chart.
        """
        trace_volume = go.Scatter(
            x=date_list,
            y=volume,
            name="volume",
            mode="lines+markers",
            line_shape="spline")
        trace_va_5 = go.Scatter(
            x=date_list[5:],
            y=ma[0],
            name="va_5",
            mode="lines+markers",
            line_shape="spline")
        trace_va_10 = go.Scatter(
            x=date_list[10:],
            y=ma[1],
            name="va_10",
            mode="lines+markers",
            line_shape="spline")
        trace_va_20 = go.Scatter(
            x=date_list[20:],
            y=ma[2],
            name="va_20",
            mode="lines+markers",
            line_shape="spline")
        traces = [trace_volume, trace_va_5, trace_va_10, trace_va_20]
        if show:
            fig = go.Figure(traces)
            fig.show()
        return traces

    def plotMACD(self,
                 macd: list,
                 dif: list,
                 date_list: list,
                 show=True) -> list:
        """Plot line chart of trading volume and price.

        Args:
            macd: a list of MACD
            dif: a list of DIF.
            date_list: stock trading date list.
            show: show line chart.
        Return:
            Trace list that plotly lib can use to plot chart.
        """
        trace_macd = go.Scatter(
            x=date_list[35:], y=macd, name="MACD", line_shape="spline")
        trace_dif = go.Scatter(
            x=date_list[26:], y=dif, name="DIF", line_shape="spline")
        traces = [trace_macd, trace_dif]
        fig = go.Figure(traces)
        if show:
            fig.show()
        return traces

    def plotPriceVolume(self, ma: list, prices: list, va: list, volumes: list,
                        date_list: list):
        """Plot line chart of trading volume and price.

        Args:
            ma: a list includes 3 days, 5 days, 10 days, and 20 days MA.
            prices: closing price list.
            va: a list of moving average of trading volume includes 5, 10, 
            20 days.
            volumes: a list of trading volume.
            date_list: stock trading date list.
        """
        trace_ma = self.plotMA(ma, prices, date_list, False)
        trace_va = self.plotVA(va, volumes, date_list, False)
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True)
        for ma in trace_ma:
            fig.append_trace(ma, row=1, col=1)
        for va in trace_va:
            fig.append_trace(va, row=2, col=1)
        fig.show()