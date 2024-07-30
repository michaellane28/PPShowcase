import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import os

def scrape_first_line_players(url):
    driver = webdriver.Chrome()
    driver.get(url)
    team_select = driver.find_element(By.CSS_SELECTOR, 'select.h-8.border.border-black')
    selected_team = team_select.find_element(By.CSS_SELECTOR, 'option:checked').text
    forwards_section = driver.find_element(By.ID, 'forwards').find_element(By.XPATH, '..').find_element(By.XPATH, '..')
    players = forwards_section.find_elements(By.CSS_SELECTOR, 'div.flex.flex-row.justify-center span')
    player_names = [player.text for player in players[:4]]
    driver.quit()
    return selected_team, player_names

def scrape_first_powerplay_players(url):
    driver = webdriver.Chrome()
    driver.get(url)
    team_select = driver.find_element(By.CSS_SELECTOR, 'select.h-8.border.border-black')
    selected_team = team_select.find_element(By.CSS_SELECTOR, 'option:checked').text
    powerplay_section = driver.find_element(By.ID, 'powerplay').find_element(By.XPATH, '..').find_element(By.XPATH, '..')
    players = powerplay_section.find_elements(By.CSS_SELECTOR, 'div.flex.flex-row.justify-center span')
    player_names = [player.text for player in players]
    driver.quit()
    return selected_team, player_names

def main(date_to_check):
    # Define the URL for each team
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

    TOP_5_PENALTY_TEAMS = ['Anaheim Ducks', 'Florida Panthers', 'Minnesota Wild', 'Montreal Canadiens', 'Ottawa Senators']


    # Read the schedule
    schedule_df = pd.read_excel('formatted_NHL_2024-25_Schedule.xlsx')

    # Filter schedule by the specified date
    selected_date_games = schedule_df[schedule_df['Date'] == date_to_check]

    games = []

    for _, game in selected_date_games.iterrows():
        home_team = game['Home']
        visitor_team = game['Visitor']
        game_time = game['Time']

        if home_team in TOP_5_PENALTY_TEAMS:
            visitor_team_players = scrape_first_line_players(TEAM_URLS.get(visitor_team, ''))
            visitor_powerplay_players = scrape_first_powerplay_players(TEAM_URLS.get(visitor_team, ''))

            visitor_first_and_powerplay = list(set(visitor_team_players[1]) & set(visitor_powerplay_players[1]))

            if len(visitor_first_and_powerplay) >= 2:
                games.append({
                    'Date': game['Date'],
                    'Time': game_time,
                    'Team': home_team,
                    'Player1': visitor_first_and_powerplay[0],
                    'Player2': visitor_first_and_powerplay[1],
                    'Player3': visitor_first_and_powerplay[2] if len(visitor_first_and_powerplay) > 2 else ''
                })

        if visitor_team in TOP_5_PENALTY_TEAMS:
            home_team_players = scrape_first_line_players(TEAM_URLS.get(home_team, ''))
            home_powerplay_players = scrape_first_powerplay_players(TEAM_URLS.get(home_team, ''))

            home_first_and_powerplay = list(set(home_team_players[1]) & set(home_powerplay_players[1]))

            if len(home_first_and_powerplay) >= 2:
                games.append({
                    'Date': game['Date'],
                    'Time': game_time,
                    'Team': visitor_team,
                    'Player1': home_first_and_powerplay[0],
                    'Player2': home_first_and_powerplay[1],
                    'Player3': home_first_and_powerplay[2] if len(home_first_and_powerplay) > 2 else ''
                })

        # Check if the file exists
    file_path = 'filtered_schedule.xlsx'
    if os.path.exists(file_path):
        # If the file exists, read the existing data
        existing_df = pd.read_excel(file_path)
        # Append the new data to the existing data
        results_df = pd.DataFrame(games)
        combined_df = pd.concat([existing_df, results_df], ignore_index=True)
    else:
        # If the file does not exist, create a new DataFrame
        combined_df = pd.DataFrame(games)

    # Save the combined data to Excel
    combined_df.to_excel(file_path, index=False)


if __name__ == "__main__":
    # Specify the date to check
    DATE_TO_CHECK = '10/08/2024'
    main(DATE_TO_CHECK)