import plotly.express as px

def plot_oi(df):

    temp = (
        df.groupby(["strike","type"])["oi"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        temp,
        x="strike",
        y="oi",
        color="type",
        barmode="group",
        title="Open Interest Distribution"
    )

    return fig