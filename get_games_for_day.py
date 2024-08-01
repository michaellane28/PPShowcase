# get_games_for_day.py
# 
#   - Responsible for populating the filter_schedule.xlsx file
#      - Contains two functions, one for finding first line players and one for finding first line powerplay players
#      - Team URLS and Top 5 Pentalty list defined
#      - Games are found from official NHL schedule based on specific date
#      - Games are checked to see if they fit the criteria
#      - Fitted games are written to the filtered_schedule file
#
#   - Runs once per day, automated using GitHub Actions
#

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
from datetime import datetime

# Function to scrape the first line players for a given team from the provided URL
def scrape_first_line_players(url):
    # Set up Selenium options for a headless Chrome browser
    options = Options()
    options.add_argument('--headless')  # Run in headless mode (without GUI)
    options.add_argument('--no-sandbox')  # Disable sandbox mode (necessary for some environments)
    options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems

    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome(options=options)
    driver.get(url)  # Navigate to the specified URL

    # Select the team dropdown and get the selected team's name
    team_select = driver.find_element(By.CSS_SELECTOR, 'select.h-8.border.border-black')
    selected_team = team_select.find_element(By.CSS_SELECTOR, 'option:checked').text

    # Find the forwards section and get the first four players' names
    forwards_section = driver.find_element(By.ID, 'forwards').find_element(By.XPATH, '..').find_element(By.XPATH, '..')
    players = forwards_section.find_elements(By.CSS_SELECTOR, 'div.flex.flex-row.justify-center span')
    player_names = [player.text for player in players[:4]]  # Get the names of the first four players

    driver.quit()  # Close the WebDriver
    return selected_team, player_names  # Return the selected team's name and player names

# Function to scrape the powerplay players for a given team from the provided URL
def scrape_first_powerplay_players(url):
    # Set up Selenium options for a headless Chrome browser
    options = Options()
    options.add_argument('--headless')  # Run in headless mode (without GUI)
    options.add_argument('--no-sandbox')  # Disable sandbox mode (necessary for some environments)
    options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems

    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome(options=options)
    driver.get(url)  # Navigate to the specified URL

    # Select the team dropdown and get the selected team's name
    team_select = driver.find_element(By.CSS_SELECTOR, 'select.h-8.border.border-black')
    selected_team = team_select.find_element(By.CSS_SELECTOR, 'option:checked').text

    # Find the powerplay section and get the powerplay players' names
    powerplay_section = driver.find_element(By.ID, 'powerplay').find_element(By.XPATH, '..').find_element(By.XPATH, '..')
    players = powerplay_section.find_elements(By.CSS_SELECTOR, 'div.flex.flex-row.justify-center span')
    player_names = [player.text for player in players]  # Get all players' names in the powerplay section

    driver.quit()  # Close the WebDriver
    return selected_team, player_names  # Return the selected team's name and player names

# Main function to execute the scraping and data collection
def main():
    # URLs for line combinations of all NHL teams
    TEAM_URLS = {
        'Anaheim Ducks': 'https://www.dailyfaceoff.com/teams/anaheim-ducks/line-combinations',
        'Arizona Coyotes': 'https://www.dailyfaceoff.com/teams/arizona-coyotes/line-combinations',
        'Boston Bruins': 'https://www.dailyfaceoff.com/teams/boston-bruins/line-combinations',
        'Buffalo Sabres': 'https://www.dailyfaceoff.com/teams/buffalo-sabres/line-combinations',
        'Calgary Flames': 'https://www.dailyfaceoff.com/teams/calgary-flames/line-combinations',
        'Carolina Hurricanes': 'https://www.dailyfaceoff.com/teams/carolina-hurricanes/line-combinations',
        'Chicago Blackhawks': 'https://www.dailyfaceoff.com/teams/chicago-blackhawks/line-combinations',
        'Colorado Avalanche': 'https://www.dailyfaceoff.com/teams/colorado-avalanche/line-combinations',
        'Columbus Blue Jackets': 'https://www.dailyfaceoff.com/teams/columbus-blue-jackets/line-combinations',
        'Dallas Stars': 'https://www.dailyfaceoff.com/teams/dallas-stars/line-combinations',
        'Detroit Red Wings': 'https://www.dailyfaceoff.com/teams/detroit-red-wings/line-combinations',
        'Edmonton Oilers': 'https://www.dailyfaceoff.com/teams/edmonton-oilers/line-combinations',
        'Florida Panthers': 'https://www.dailyfaceoff.com/teams/florida-panthers/line-combinations',
        'Los Angeles Kings': 'https://www.dailyfaceoff.com/teams/los-angeles-kings/line-combinations',
        'Minnesota Wild': 'https://www.dailyfaceoff.com/teams/minnesota-wild/line-combinations',
        'Montreal Canadiens': 'https://www.dailyfaceoff.com/teams/montreal-canadiens/line-combinations',
        'Nashville Predators': 'https://www.dailyfaceoff.com/teams/nashville-predators/line-combinations',
        'New Jersey Devils': 'https://www.dailyfaceoff.com/teams/new-jersey-devils/line-combinations',
        'New York Islanders': 'https://www.dailyfaceoff.com/teams/new-york-islanders/line-combinations',
        'New York Rangers': 'https://www.dailyfaceoff.com/teams/new-york-rangers/line-combinations',
        'Ottawa Senators': 'https://www.dailyfaceoff.com/teams/ottawa-senators/line-combinations',
        'Philadelphia Flyers': 'https://www.dailyfaceoff.com/teams/philadelphia-flyers/line-combinations',
        'Pittsburgh Penguins': 'https://www.dailyfaceoff.com/teams/pittsburgh-penguins/line-combinations',
        'San Jose Sharks': 'https://www.dailyfaceoff.com/teams/san-jose-sharks/line-combinations',
        'Seattle Kraken': 'https://www.dailyfaceoff.com/teams/seattle-kraken/line-combinations',
        'St. Louis Blues': 'https://www.dailyfaceoff.com/teams/st-louis-blues/line-combinations',
        'Tampa Bay Lightning': 'https://www.dailyfaceoff.com/teams/tampa-bay-lightning/line-combinations',
        'Toronto Maple Leafs': 'https://www.dailyfaceoff.com/teams/toronto-maple-leafs/line-combinations',
        'Vancouver Canucks': 'https://www.dailyfaceoff.com/teams/vancouver-canucks/line-combinations',
        'Vegas Golden Knights': 'https://www.dailyfaceoff.com/teams/vegas-golden-knights/line-combinations',
        'Washington Capitals': 'https://www.dailyfaceoff.com/teams/washington-capitals/line-combinations',
        'Winnipeg Jets': 'https://www.dailyfaceoff.com/teams/winnipeg-jets/line-combinations'
    }

    # List of top 5 teams with the most penalties per game
    TOP_5_PENALTY_TEAMS = ['Anaheim Ducks', 'Florida Panthers', 'Minnesota Wild', 'Montreal Canadiens', 'Ottawa Senators']

    # Get the current date in MM/DD/YYYY format
    current_date = datetime.now().strftime('%m/%d/%Y')

    # Load the NHL schedule from an Excel file
    schedule_df = pd.read_excel('formatted_NHL_2024-25_Schedule.xlsx')

    # Filter the schedule for games on the current date
    selected_date_games = schedule_df[schedule_df['Date'] == current_date]

    games = []

    # Iterate through the games scheduled for the current date
    for _, game in selected_date_games.iterrows():
        home_team = game['Home']
        visitor_team = game['Visitor']
        game_time = game['Time']

        # If the home team is in the top 5 penalty teams, get the visitor team's players
        if home_team in TOP_5_PENALTY_TEAMS:
            visitor_team_players = scrape_first_line_players(TEAM_URLS.get(visitor_team, ''))
            visitor_powerplay_players = scrape_first_powerplay_players(TEAM_URLS.get(visitor_team, ''))

            # Find players who are both in the first line and on the powerplay
            visitor_first_and_powerplay = list(set(visitor_team_players[1]) & set(visitor_powerplay_players[1]))

            # If there are at least 2 such players, add them to the games list
            if len(visitor_first_and_powerplay) >= 2:
                games.append({
                    'Date': game['Date'],
                    'Time': game_time,
                    'Team': home_team,
                    'Player1': visitor_first_and_powerplay[0],
                    'Player2': visitor_first_and_powerplay[1],
                    'Player3': visitor_first_and_powerplay[2] if len(visitor_first_and_powerplay) > 2 else ''
                })

        # If the visitor team is in the top 5 penalty teams, get the home team's players
        if visitor_team in TOP_5_PENALTY_TEAMS:
            home_team_players = scrape_first_line_players(TEAM_URLS.get(home_team, ''))
            home_powerplay_players = scrape_first_powerplay_players(TEAM_URLS.get(home_team, ''))

            # Find players who are both in the first line and on the powerplay
            home_first_and_powerplay = list(set(home_team_players[1]) & set(home_powerplay_players[1]))

            # If there are at least 2 such players, add them to the games list
            if len(home_first_and_powerplay) >= 2:
                games.append({
                    'Date': game['Date'],
                    'Time': game_time,
                    'Team': visitor_team,
                    'Player1': home_first_and_powerplay[0],
                    'Player2': home_first_and_powerplay[1],
                    'Player3': home_first_and_powerplay[2] if len(home_first_and_powerplay) > 2 else ''
                })

    # Define the file path for the Excel file
    file_path = 'filtered_schedule.xlsx'
    if os.path.exists(file_path):
        # If the file already exists, load it and append new results
        existing_df = pd.read_excel(file_path)
        results_df = pd.DataFrame(games)
        combined_df = pd.concat([existing_df, results_df], ignore_index=True)
    else:
        # If the file does not exist, create a new DataFrame with the results
        combined_df = pd.DataFrame(games)

    # Save the combined results to the Excel file
    combined_df.to_excel(file_path, index=False)

# Entry point of the script
if __name__ == "__main__":
    main()