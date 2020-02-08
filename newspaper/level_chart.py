import pandas as pd
import plotly
import plotly.graph_objects as go

def create_level(df):
    traces = []
    for i in df.columns[1:-1]:
        trace = go.Bar(x=df['Newspaper'], y=df[i], name=i, text=df[i], textposition="outside")
        traces.append(trace)
    data = traces
    layout = go.Layout(barmode='group')
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(font=dict(size=9), legend=dict(x=-.1, y=1.2), legend_orientation="h", margin=dict(t=5,b=5,l=5,r=5))
    div = plotly.offline.plot(fig, include_plotlyjs=False, output_type='div', config={"displayModeBar": False})
    return div

def create_level_percent(df,color):
    trace = go.Bar(x=df['Newspaper'], text=df.iloc[:,-1], textposition="outside", 
                   y=df.iloc[:,-1], marker_color=color)
    data = [trace]
    layout = go.Layout(margin=dict(t=5,b=5,l=5,r=5))
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(font=dict(size=9))
    div = plotly.offline.plot(fig, include_plotlyjs=False,
                              output_type='div', config={"displayModeBar": False})
    return div

def create_pie_chart(df):
    data=[go.Pie(labels=df['Newspaper'], values=df['News Articles'], hole=.3)]
    layout = go.Layout(margin=dict(t=5,b=5,l=5,r=5))
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(font=dict(size=9), legend=dict(x=-.1, y=1.2), legend_orientation="h")
    div = plotly.offline.plot(fig, include_plotlyjs=False,
                              output_type='div', config={"displayModeBar": False})
    return div
