# import required packages
import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
import plotly.express as px

# Page setting
st.set_page_config(layout="wide", page_title="Elections 2022 Analysis", page_icon="🗳️")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.header("2022 Kenya Presidential Election Analysis")
st.markdown(
    """
    The following analysis is based on the data released by the Independent Electoral and Boundaries Commission (IEBC) in August 2022. The data is available on the IEBC website [here](https://www.iebc.or.ke/). The key metrics are compared with the 2017 results.
    """
)

# Select Data to view: National, County/Diaspora
st.sidebar.image("data/motivate.png", width=300)
st.sidebar.title("Select the type of data you want to retrieve")
st.sidebar.subheader("Instructions:")
st.sidebar.markdown(
    """
    - Select the data to view using the select box below.
    - For National Results View the data on the main panel.
    - For County & Diaspora votes: Select the county from the dropdown list in the main panel.
        """
)

selection = st.sidebar.selectbox(
    "Select the type of data you want to retrieve", ["National", "County/Diaspora"]
)
# Load data
def load_data():
    df = pd.read_csv("data/elections_2022.csv")
    return df


data_df = load_data()

a1, a2, a3, a4 = st.columns(4)
a1.image("data/iebc.jpg", width=200)
a2.metric("Registered Voters", 22_120_458, +2_509_035)
a3.metric("Total Registered Voters", 14_213_137, -833_044)
a4.metric("Percentage Turnout", "66.14%", "-15.37%")


county_names = data_df["County Name"].unique()


def calculate_national_vote():
    data_df = load_data()
    total_df = data_df.sum(skipna=True)
    total_df = total_df.to_frame().reset_index()
    total_df.drop([0, 1, 6, 7, 8, 9], axis=0, inplace=True)
    total_df.reset_index(drop=True, inplace=True)
    total_df.rename(columns={"index": "Candidate", 0: "Votes"}, inplace=True)
    total_df["Votes"] = total_df["Votes"].astype(int)
    total_df["Percentage"] = (total_df["Votes"] / total_df["Votes"].sum() * 100).round(
        2
    )
    total_df.sort_values(by="Votes", ascending=False, inplace=True)
    total_df.reset_index(drop=True, inplace=True)
    return total_df


def calculate_county_vote(county_name):
    data_df = load_data()
    county_df = data_df.set_index("County Name")
    county_df = county_df.loc[county_name]
    county_df = county_df.to_frame().reset_index()
    county_df.drop([0, 5, 6, 7, 8], axis=0, inplace=True)
    county_df.reset_index(drop=True, inplace=True)
    county_df.rename(columns={"index": "Candidate"}, inplace=True)
    county_df["Percentage"] = (
        county_df[county_name] / county_df[county_name].sum() * 100
    ).round(2)
    county_df.sort_values(by=county_name, ascending=False, inplace=True)
    return county_df


def calculate_county_voter_data(county_name):
    data_df = load_data()
    county_df = data_df.set_index("County Name")
    county_df = county_df.loc[county_name]
    county_df = county_df.to_frame().reset_index()
    county_df.drop([1, 2, 3, 4, 7, 8], axis=0, inplace=True)
    county_df.reset_index(drop=True, inplace=True)
    county_df.rename(columns={"index": "Metric"}, inplace=True)
    turn_out = (
        (county_df.iloc[1][county_name] + county_df.iloc[2][county_name])
        / county_df.iloc[0][county_name]
        * 100
    )
    return turn_out


def list_top_turnout():
    top_turn_out_df = load_data()
    top_turn_out_df.drop(["Waihiga Mwaure", "George Wajackoyah"], axis=1, inplace=True)
    top_turn_out_df.sort_values(by="Percentage Turnout", ascending=False, inplace=True)
    top_turn_out_df["Winner"] = top_turn_out_df[["Raila Odinga", "William Ruto"]].max(
        axis=1
    )
    top_turn_out_df["Winner"] = np.where(
        top_turn_out_df["Winner"] == top_turn_out_df["Raila Odinga"],
        "Raila Odinga",
        "William Ruto",
    )
    top_turn_out_df = top_turn_out_df[["County Name", "Percentage Turnout", "Winner"]]
    top_turn_out_df.sort_values(by="Percentage Turnout", ascending=False)
    return top_turn_out_df


def list_bottom_turnout():
    bottom_turn_out_df = load_data()
    bottom_turn_out_df.drop(
        ["Waihiga Mwaure", "George Wajackoyah"], axis=1, inplace=True
    )
    bottom_turn_out_df.sort_values(
        by="Percentage Turnout", ascending=False, inplace=True
    )
    bottom_turn_out_df["Winner"] = bottom_turn_out_df[
        ["Raila Odinga", "William Ruto"]
    ].max(axis=1)
    bottom_turn_out_df["Winner"] = np.where(
        bottom_turn_out_df["Winner"] == bottom_turn_out_df["Raila Odinga"],
        "Raila Odinga",
        "William Ruto",
    )
    bottom_turn_out_df = bottom_turn_out_df[
        ["County Name", "Percentage Turnout", "Winner"]
    ]
    bottom_turn_out_df.sort_values(
        by="Percentage Turnout", ascending=True, inplace=True
    )
    return bottom_turn_out_df


def calculate_mean_turnout():
    mean_turn_out_df = load_data()
    mean_turn_out_df.drop(["Waihiga Mwaure", "George Wajackoyah"], axis=1, inplace=True)
    mean_turn_out_df.sort_values(by="Percentage Turnout", ascending=False, inplace=True)
    mean_turn_out_df["Winner"] = mean_turn_out_df[["Raila Odinga", "William Ruto"]].max(
        axis=1
    )
    mean_turn_out_df["Winner"] = np.where(
        mean_turn_out_df["Winner"] == mean_turn_out_df["Raila Odinga"],
        "Raila Odinga",
        "William Ruto",
    )
    mean_turn_out_df = mean_turn_out_df[["County Name", "Percentage Turnout", "Winner"]]
    raila_mean = mean_turn_out_df.loc[
        mean_turn_out_df["Winner"] == "Raila Odinga", "Percentage Turnout"
    ].mean()
    ruto_mean = mean_turn_out_df.loc[
        mean_turn_out_df["Winner"] == "William Ruto", "Percentage Turnout"
    ].mean()
    return raila_mean, ruto_mean


def visualise_national_data():
    national_df = calculate_national_vote()
    st.markdown(
        """
    ## National Results as Declared by the IEBC
    ### The following table shows the total number of votes cast for each candidate.
    """
    )
    st.table(national_df)
    st.markdown(
        """
    ## Percentage of Votes per Candidate
    """
    )
    fig = px.bar(national_df, x="Candidate", y="Percentage", color="Candidate")
    fig.update_layout()
    st.plotly_chart(fig, use_container_width=True)


def visualise_county_data():
    st.markdown(
        """
    ## County Results as Declared by the IEBC
    ## Use the dropdown list to select the county you want to view.
    """
    )
    county_name = st.selectbox("Select County:", county_names)
    county_presidential_data_df = calculate_county_vote(county_name)
    county_turn_out = calculate_county_voter_data(county_name).round(2)
    fig = px.bar(
        county_presidential_data_df, x="Percentage", y="Candidate", color="Candidate"
    )
    fig.update_layout()
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""### County Turnout:""")
    st.metric(label=f"{county_name}", delta=None, value=county_turn_out)


def visualise_top_turnout():
    top_turn_out_def = list_top_turnout().reset_index(drop=True)
    st.markdown(
        """
    - William Ruto won in 6 of the top 10 counties with the highest turnout.
    - Highest voter turnout evident in  Rift Valley.
    """
    )
    st.table(top_turn_out_def.head(10))


def visualise_bottom_turnout():
    top_turn_out_def = (
        list_top_turnout()
        .sort_values(by="Percentage Turnout", ascending=True)
        .reset_index(drop=True)
    )
    st.markdown(
        """
    - Raila Odinga won in all counties with the 10 lowest turnout.
    - Lowest turnout in Coastal counties - Significiant metric?
    """
    )
    st.table(top_turn_out_def.head(10))


def visualise_correlation():
    raila, ruto = calculate_mean_turnout()
    raila_average = round(raila, 2)
    ruto_average = round(ruto, 2)
    st.markdown(
        """
    ## Correlation between Turnout per County and Winner of the County
    - Although Raila won in more counties than Ruto, the average turnout in counties won by Raila was lower than the average turnout in counties won by Ruto. (63.04% vs 70.49%)
    - The dotted lines represents the average turnout for counties won by Raila (Blue) vs Ruto (Red).
    """
    )
    correlation_df = load_data()
    correlation_df.sort_values(by="Percentage Turnout", ascending=True, inplace=True)
    correlation_df["Winner"] = correlation_df[["Raila Odinga", "William Ruto"]].max(
        axis=1
    )
    correlation_df["Winner"] = np.where(
        correlation_df["Winner"] == correlation_df["Raila Odinga"],
        "Raila Odinga",
        "William Ruto",
    )
    fig = px.scatter(
        correlation_df,
        y="Percentage Turnout",
        x="County Name",
        color="Winner",
        size="Percentage Turnout",
        hover_name="County Name",
        size_max=60,
    )
    fig.add_shape(
        type="line",
        x0=0,
        y0=raila_average,
        x1=47,
        y1=raila_average,
        line=dict(color="Blue", width=2, dash="dash"),
    )
    fig.add_shape(
        type="line",
        x0=0,
        y0=ruto_average,
        x1=47,
        y1=ruto_average,
        line=dict(color="Red", width=2, dash="dash"),
    )
    fig.update_layout()
    st.plotly_chart(fig, use_container_width=True)


def visualiase_turnout_average():
    raila, ruto = calculate_mean_turnout()
    raila = round(raila, 2)
    ruto = round(ruto, 2)
    delta_raila_ruto = round((ruto - raila), 2)
    st.markdown(
        """
    # Analysis of Voter Turnout """
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Average % Turnout - Raila won Counties", value=raila)
    with c2:
        st.metric("Average % Turnout - Ruto won Counties", value=ruto)
    with c3:
        st.metric("Difference", value="", delta=delta_raila_ruto)
    b1, b2 = st.columns(2)
    with b1:
        visualise_top_turnout()
    with b2:
        visualise_bottom_turnout()


if __name__ == "__main__":

    try:
        if selection == "National":
            visualise_national_data()
            visualiase_turnout_average()
            visualise_correlation()
        else:
            visualise_county_data()
            visualiase_turnout_average()
            visualise_correlation()

    except BaseException as e:
        st.error(e)
