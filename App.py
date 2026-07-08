import os
import pandas as pd
import plotly.express as px
from flask import Flask, render_template

app = Flask(__name__)
DATA_PATH = os.path.join("data", "heritage_sites.csv")


def load_data():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(
            f"Could not find {DATA_PATH}. Run 'python generate_sample_data.py' first."
        )
    df = pd.read_csv(DATA_PATH)

    if df["Danger"].dtype != object:
        df["Danger"] = df["Danger"].map({1: "Yes", 0: "No"})
    df["Danger"] = df["Danger"].astype(str).str.strip().str.title()
    df["Danger"] = df["Danger"].replace({"1": "Yes", "0": "No", "True": "Yes", "False": "No"})

    df["Date_inscribed"] = pd.to_numeric(df["Date_inscribed"], errors="coerce")
    df = df.dropna(subset=["Date_inscribed"])
    df["Date_inscribed"] = df["Date_inscribed"].astype(int)
    return df


def build_country_treemap(df):
    counts = df.groupby("Country")["Name_en"].count().reset_index()
    counts.columns = ["Country", "Site_Count"]
    fig = px.treemap(
        counts, path=["Country"], values="Site_Count",
        title="Heritage Sites by Country", color="Site_Count",
        color_continuous_scale="Blues",
    )
    fig.update_layout(margin=dict(t=50, l=10, r=10, b=10))
    return fig.to_html(full_html=False, include_plotlyjs="cdn")


def build_danger_pie(df):
    counts = df.groupby("Danger")["Name_en"].count().reset_index()
    counts.columns = ["Danger", "Site_Count"]
    fig = px.pie(
        counts, names="Danger", values="Site_Count",
        title="Heritage Sites at Risk (In Danger vs Not in Danger)",
        color="Danger",
        color_discrete_map={"Yes": "#d62728", "No": "#2ca02c"},
        hole=0.35,
    )
    fig.update_layout(margin=dict(t=50, l=10, r=10, b=10))
    return fig.to_html(full_html=False, include_plotlyjs=False)


def build_region_trend_line(df):
    trend = (
        df.groupby(["Date_inscribed", "Region"])["Name_en"]
        .count().reset_index()
        .rename(columns={"Name_en": "Site_Count"})
        .sort_values("Date_inscribed")
    )
    fig = px.line(
        trend, x="Date_inscribed", y="Site_Count", color="Region",
        markers=True, title="Regional Inscription Trends Over Time",
    )
    fig.update_layout(
        margin=dict(t=50, l=10, r=10, b=10),
        xaxis_title="Year Inscribed", yaxis_title="Number of Sites Inscribed",
    )
    return fig.to_html(full_html=False, include_plotlyjs=False)


@app.route("/")
def index():
    df = load_data()
    treemap_html = build_country_treemap(df)
    pie_html = build_danger_pie(df)
    line_html = build_region_trend_line(df)
    stats = {
        "total_sites": len(df),
        "total_countries": df["Country"].nunique(),
        "total_in_danger": (df["Danger"] == "Yes").sum(),
        "total_regions": df["Region"].nunique(),
    }
    return render_template(
        "index.html", treemap_html=treemap_html, pie_html=pie_html,
        line_html=line_html, stats=stats,
    )


if __name__ == "__main__":
    app.run(debug=True)
