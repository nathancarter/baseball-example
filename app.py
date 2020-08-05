
# # Visualizing Baseball Salaries
# 
# This is a small notebook that does a simple visualization of Major League Baseball players' salary trends, using a dataset we've seen in previous weeks of this course.
# 
# ## Load the dataset

import streamlit as st
import pandas as pd

@st.cache
def load_data ():
    return pd.read_csv( 'baseball-salaries-simplified.csv' )
df = load_data()


# ## Choose parameters

min_year, max_year = st.sidebar.slider(
    'Years to include:', 1988, 2016, ( 2000, 2010 ), 1 )
position_names = {
    "1B" : "First base",
    "2B" : "Second base",
    "3B" : "Third base",
    "C" : "Catcher",
    "CF" : "Center field",
    "DH" : "Designated hitter",
    "LF" : "Left field",
    "OF" : "Outfield",
    "P" : "Pitcher",
    "RF" : "Right field",
    "RP" : "Relief pitcher",
    "SP" : "Starting pitcher",
    "SS" : "Shortstop"
}
position_abbrs = { value : key for key, value in position_names.items() }
position_order = [
    'P', 'SP', 'RP', 'C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'OF', 'DH'
]
position = st.sidebar.selectbox(
    'Position to include:', [ position_names[p] for p in position_order ] )
position_abbr = position_abbrs[position]


# ## Filter the dataset

just_2000s = (df.year >= min_year) & (df.year <= max_year)
just_one_pos = df.pos == position_abbr
focus = df[just_2000s & just_one_pos]


# ## Create a table of percentiles

# Which years do we care about?
years = range( min_year, max_year + 1 )

# We'll store the results in a new DataFrame.
df_pcts = pd.DataFrame( { "year" : years } )

# How to compute a percentile in a given year:
def percentile_in_year ( year, percent ):
    return focus[focus.year == year].salary.quantile( percent/100 )

# Fill the DataFrame using that function.
for percent in range( 0, 110, 10 ):
    df_pcts[percent] = [ percentile_in_year( year, percent ) for year in years ]

# Make years the index.
df_pcts.index = df_pcts.year
del df_pcts['year']

# Change units to millions of dollars.
df_pcts /= 1000000


# ## Plot the data

st.title( 'Major League Baseball Salaries' )
import matplotlib.pyplot as plt
df_pcts.plot( legend='upper left' )
plt.gcf().set_size_inches(8,10)
plt.title( f'Salaries for {position} ({len(focus)} players)', fontsize=20 )
plt.xticks( df_pcts.index, rotation=90 )
plt.ylabel( 'Salary percentiles in $1M', fontsize=14 )
plt.xlabel( None )
st.pyplot()


# ## Investigate Extreme Values

st.markdown( f'## Highest salaries for {position}, {min_year}-{max_year}' )
st.dataframe( focus.nlargest( 10, 'salary' ).reset_index( drop=True ) )
