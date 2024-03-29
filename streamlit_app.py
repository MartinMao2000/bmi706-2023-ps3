import altair as alt
import pandas as pd
import streamlit as st

### P1.2 ###

# Move this code into `load_data` function {{
# }}


@st.cache
def load_data():
    ## {{ CODE HERE }} ##
    cancer_df = pd.read_csv("https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/cancer_ICD10.csv").melt(  # type: ignore
    id_vars=["Country", "Year", "Cancer", "Sex"],
    var_name="Age",
    value_name="Deaths",
    )

    pop_df = pd.read_csv("https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/population.csv").melt(  # type: ignore
        id_vars=["Country", "Year", "Sex"],
        var_name="Age",
        value_name="Pop",
    )

    df = pd.merge(left=cancer_df, right=pop_df, how="left")
    df["Pop"] = df.groupby(["Country", "Sex", "Age"])["Pop"].fillna(method="bfill")
    df.dropna(inplace=True)

    df = df.groupby(["Country", "Year", "Cancer", "Age", "Sex"]).sum().reset_index()
    df["Rate"] = df["Deaths"] / df["Pop"] * 100_000

    return df


# Uncomment the next line when finished
df = load_data()

### P1.2 ###


st.write("## Age-specific cancer mortality rates")

### P2.1 ###
# replace with st.slider

# Create a slider for selecting the year
year = st.slider('Select a year', 1994, 2020, 2012)  # Default value is 2012

# Filter the DataFrame based on the selected year
subset = df[df["Year"] == year]

### P2.1 ###


### P2.2 ###
# Add a radio button for sex selection
sex = st.radio("Select Sex", ('M', 'F'))  # 'M' and 'F' are the options for male and female

# Filter the subset based on the selected sex
subset = subset[subset["Sex"] == sex]
### P2.2 ###


### P2.3 ###
# replace with st.multiselect
# (hint: can use current hard-coded values below as as `default` for selector)
countries = [
    "Austria",
    "Germany",
    "Iceland",
    "Spain",
    "Sweden",
    "Thailand",
    "Turkey",
]
all_countries = df['Country'].unique().tolist()
selected_countries = st.multiselect('Select countries', options=all_countries, default=countries)
subset = subset[subset['Country'].isin(selected_countries)]
### P2.3 ###


### P2.4 ###
# replace with st.selectbox
cancer_types = df['Cancer'].unique().tolist()
selected_cancer = st.selectbox('Select a cancer type', options=cancer_types, index=cancer_types.index("Malignant neoplasm of stomach"))
cancer = "Malignant neoplasm of stomach"
subset = subset[subset["Cancer"] == selected_cancer]
### P2.4 ###


### P2.5 ###
ages = [
    "Age <5",
    "Age 5-14",
    "Age 15-24",   
    "Age 25-34",
    "Age 35-44",
    "Age 45-54",
    "Age 55-64",
    "Age >64",
]

# chart = alt.Chart(subset).mark_bar().encode(
#     x=alt.X("Age", sort=ages),
#     y=alt.Y("Rate", title="Mortality rate per 100k"),
#     color="Country",
#     tooltip=["Rate"],
# ).properties(
#     title=f"{cancer} mortality rates for {'males' if sex == 'M' else 'females'} in {year}",
# )

# Heatmap chart code
chart = alt.Chart(subset).mark_rect().encode(
    x=alt.X("Age:O", sort=ages),
    y=alt.Y("Country:N"),
    color=alt.Color("Rate:Q", scale=alt.Scale(type="log", domain=(0.01, 1000), clamp=True)),
    tooltip=["Country", "Age", "Rate"],
).properties(
    title=f"{selected_cancer} mortality rates for {'males' if sex == 'M' else 'females'} in {year}",
)

### P2.5 ###

st.altair_chart(chart, use_container_width=True)

countries_in_subset = subset["Country"].unique()
if len(countries_in_subset) != len(countries):
    if len(countries_in_subset) == 0:
        st.write("No data avaiable for given subset.")
    else:
        missing = set(countries) - set(countries_in_subset)
        st.write("No data available for " + ", ".join(missing) + ".")
