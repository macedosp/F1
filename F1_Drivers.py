import pandas as pd
import streamlit as st

# Load data
df = pd.read_csv('arquivos/drivers_updated.csv')
winners_df = pd.read_csv('arquivos/winners.csv')

# Streamlit App
def main():
    st.title("F1 Drivers and Winners Filter App")
    
    # Sidebar for filters
    st.sidebar.header("Filter Options")
    
    # Filter by driver
    driver = st.sidebar.selectbox("Select a Driver", ['All'] + sorted(df['Driver'].unique().tolist()))
    
    # Filter by nationality
    nationality = st.sidebar.selectbox("Select Nationality", ['All'] + sorted(df['Nationality'].unique().tolist()))
    
    # Filter by Grand Prix
    grand_prix = st.sidebar.selectbox("Select Grand Prix", ['All'] + sorted(winners_df['Grand Prix'].unique().tolist()))
    
    # Filter by year
    year = st.sidebar.selectbox("Select Year", ['All'] + sorted(df['year'].unique().tolist()))
    
    # Apply filters
    filtered_df = df.copy()
    if driver != 'All':
        filtered_df = filtered_df[filtered_df['Driver'] == driver]
    if nationality != 'All':
        filtered_df = filtered_df[filtered_df['Nationality'] == nationality]
    if year != 'All':
        filtered_df = filtered_df[filtered_df['year'] == year]
    
    filtered_winners_df = winners_df.copy()
    if driver != 'All':
        filtered_winners_df = filtered_winners_df[filtered_winners_df['Winner'].str.contains(driver, case=False, na=False)]
    if grand_prix != 'All':
        filtered_winners_df = filtered_winners_df[filtered_winners_df['Grand Prix'] == grand_prix]
    if year != 'All':
        filtered_winners_df = filtered_winners_df[filtered_winners_df['Date'].str.contains(str(year))]
    if nationality != 'All':
        drivers_of_nationality = df[df['Nationality'] == nationality]['Driver'].unique()
        filtered_winners_df = filtered_winners_df[filtered_winners_df['Winner'].isin(drivers_of_nationality)]
    
    # Display the filtered data
    st.write("### Filtered F1 Drivers Data")
    st.dataframe(filtered_df)
    
    if driver != 'All':
        driver_gps = winners_df[winners_df['Winner'].str.contains(driver, case=False, na=False)]
        st.write(f"### Grand Prix Participation of {driver}")
        st.dataframe(driver_gps[['Grand Prix', 'Date', 'Car', 'Laps', 'Time']])
    
    st.write("### Filtered Grand Prix Winners Data")
    st.dataframe(filtered_winners_df)

if __name__ == "__main__":
    main()
