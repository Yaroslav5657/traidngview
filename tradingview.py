import time
import yfinance as yf
from datetime import datetime, timedelta
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

# Додаємо тему для кращого вигляду (необов'язково)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def get_tradingview_chart(ticker):
    # Отримати дані для TradingView графіка (приклад)
    data = yf.download(ticker, period="1d", interval="1m")

    # Створити індикатор або будь-які необхідні елементи графіка

    fig = go.Figure()

    # Додайте свої дані до TradingView графіка
    fig.add_trace(go.Candlestick(x=data.index,
                                 open=data['Open'],
                                 high=data['High'],
                                 low=data['Low'],
                                 close=data['Close'],
                                 increasing_line_color='lime',
                                 decreasing_line_color='red',
                                 line=dict(width=0.6)  # Set the width of the candlesticks
                                 ))

    # Форматування осей та легенди
    fig.update_xaxes(type='category', tickmode='array',
                     tickvals=data.index[::10],  # кожні 10 інтервалів
                     ticktext=data.index.strftime('%H:%M').tolist()[::10],
                     showgrid=True, gridcolor='rgba(211,211,211,0.5)')

    fig.update_yaxes(showgrid=True, gridcolor='rgba(211,211,211,0.5)')
    fig.update_layout(xaxis_rangeslider_visible=False)

    return fig

app.layout = html.Div(children=[
    dcc.Graph(id='live-graph', config={'scrollZoom': False}),
    dcc.Interval(
        id='interval-component',
        interval=60*1000,  # оновлювати кожні 1 хвилину
        n_intervals=0
    )
])

@app.callback(Output('live-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph(n):
    # Тікер, який ви хочете відображати
    ticker = 'AAPL'

    # Отримати TradingView графік
    fig = get_tradingview_chart(ticker)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
