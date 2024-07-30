from selenium import webdriver
from selenium.webdriver.common.by import By

def scrape_first_line_players(url):
    driver = webdriver.Chrome()
    driver.get(url)

    # Find the selected team name
    team_select = driver.find_element(By.CSS_SELECTOR, 'select.h-8.border.border-black')
    selected_team = team_select.find_element(By.CSS_SELECTOR, 'option:checked').text

    # Find the "1st Line Forwards" section
    forwards_section = driver.find_element(By.ID, 'forwards').find_element(By.XPATH, '..').find_element(By.XPATH, '..')

    # Find all player names within this section
    players = forwards_section.find_elements(By.CSS_SELECTOR, 'div.flex.flex-row.justify-center span')

    # Extract and return player names
    player_names = [player.text for player in players[:4]]

    driver.quit()
    return selected_team, player_names