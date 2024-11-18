import pandas as pd
import streamlit as st
import altair as alt

# Load data
df = pd.read_csv('Arquivos/drivers_updated.csv')
winners_df = pd.read_csv('/arquivos/winners.csv')
fastest_laps_df = pd.read_csv('/arquivos/fastest_laps_updated.csv')
teams_df = pd.read_csv('/arquivos/teams_updated.csv')

# Streamlit App
def main():
    st.title("F1 Championship Wins Counter")
    
    # Filter only drivers who have won a championship
    champions_data = df[df['Pos'] == '1']
    champions = champions_data['Driver'].unique()
    
    # Prepare data for plotting championship wins
    champion_wins_count = champions_data.groupby('Driver')['year'].nunique().reset_index()
    champion_wins_count.columns = ['Driver', 'Championship Wins']
    
    # Sidebar for driver selection
    st.sidebar.header("Select a Driver")
    driver = st.sidebar.selectbox("Driver", sorted(df['Driver'].unique().tolist()))
    
    # Plot the data using Altair for championship wins
    st.write("## Comparative Results of Championship Winners")
    if driver:
        champion_wins_count['color'] = champion_wins_count['Driver'].apply(lambda x: 'Selected' if x.strip().lower() == driver.strip().lower() else 'Other')
        chart = alt.Chart(champion_wins_count).mark_bar().encode(
            x=alt.X('Driver', sort='-y', title='Driver'),
            y=alt.Y('Championship Wins', title='Number of Championship Wins'),
            color=alt.Color('color', scale=alt.Scale(domain=['Selected', 'Other'], range=['orange', 'skyblue']), legend=None)
        ).properties(
            width=600,
            height=400,
            title='Number of Championship Wins by Driver'
        )
        st.altair_chart(chart, use_container_width=True)
    
    # Prepare data for plotting wins
    drivers_with_wins = winners_df['Winner'].value_counts().reset_index()
    drivers_with_wins.columns = ['Driver', 'Wins']
    drivers_with_wins = drivers_with_wins[drivers_with_wins['Wins'] > 0]
    
    # Plot the data using Altair for wins
    st.write("## Comparative Results of Drivers with Wins")
    if driver:
        drivers_with_wins['color'] = drivers_with_wins['Driver'].apply(lambda x: 'Selected' if x.strip().lower() == driver.strip().lower() else 'Other')
        wins_chart = alt.Chart(drivers_with_wins).mark_bar().encode(
            x=alt.X('Driver', sort='-y', title='Driver'),
            y=alt.Y('Wins', title='Number of Wins'),
            color=alt.Color('color', scale=alt.Scale(domain=['Selected', 'Other'], range=['orange', 'skyblue']), legend=None)
        ).properties(
            width=600,
            height=400,
            title='Number of Wins by Driver'
        )
        st.altair_chart(wins_chart, use_container_width=True)
    
    if driver:
        # Filter driver data
        driver_data = df[df['Driver'].str.strip().str.lower() == driver.strip().lower()]
        driver_wins_data = winners_df[winners_df['Winner'].str.strip().str.lower().str.contains(driver.strip().lower(), na=False)]
        
        # Count championship wins (times the driver has 'Pos' == 1)
        championship_wins_data = driver_data[driver_data['Pos'] == '1']
        num_championship_wins = championship_wins_data.shape[0]
        
        # Get years of championship wins
        championship_years = championship_wins_data['year'].tolist() if num_championship_wins > 0 else []
        
        # Count number of Grand Prix participated
        num_gps = driver_data.shape[0]
        
        # Count number of wins (from winners dataset)
        num_wins = driver_wins_data.shape[0]
        
        # Display the result
        st.write(f"## Statistics for {driver}")
        st.write(f"- **Number of Championship Wins**: {num_championship_wins}")
        if championship_years:
            st.write(f"  - **Years of Championship Wins**: {', '.join(map(str, championship_years))}")
        st.write(f"- **Number of Grand Prix Participated**: {num_gps}")
        st.write(f"- **Number of Wins**: {num_wins}")

if __name__ == "__main__":
    main()
