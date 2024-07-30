from selenium import webdriver
from selenium.webdriver.common.by import By

def scrape_first_powerplay_players(url):
    driver = webdriver.Chrome()
    driver.get(url)

    # Find the selected team name
    team_select = driver.find_element(By.CSS_SELECTOR, 'select.h-8.border.border-black')
    selected_team = team_select.find_element(By.CSS_SELECTOR, 'option:checked').text

    # Find the "1st Powerplay Unit" section
    powerplay_section = driver.find_element(By.ID, 'powerplay').find_element(By.XPATH, '..').find_element(By.XPATH, '..')

    # Find all player names within this section
    players = powerplay_section.find_elements(By.CSS_SELECTOR, 'div.flex.flex-row.justify-center span')

    # Extract and return player names
    player_names = [player.text for player in players]

    driver.quit()
    return selected_team, player_names