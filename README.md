<img src="ppshowcaseLogo.png" alt="Alt text" width="213" height="120">

# Powerplay Showcase

A web application that displays games for the NHL 2024-25 season, in which 2 players on one team are on both first line forward and first line powerplay and the other team was top 5 in penalty minutes last year.

## Background

 - The schedule used for this application is the 2024-25 Official NHL Schedule (by Day).xlsx dataset provided by NHL.com
 - All player images have been scraped from NHL.com and populated into an excel file

## Main Features

The games displayed on the website are pulled from filtered_schedule.xlsx. This file is populated through this process:
 - get_games_for_day,py:
   - Checks official schedule for games on a specific date.
   - Checks each game against the criteria
      - Checks if the home team is in Top 5 list
         - If true, scrapes first line and first line powerplay players for away team looking for 2 commonalities
            - If true, home team and away players are added to games list
      - Checks if the awat team is in Top 5 list
         - If true, scrapes first line and first line powerplay players for home team looking for 2 commonalities
            - If true, home team and away players are added to games list
      - (Both teams are checked in case they are both in Top 5 list)
   - Appends the games list to the excel file

 - update_schedule.yml:
   - GitHub Action triggered everday at 12:00 AM CDT
   - Runs the get_games_for_day.py script based on the current date
   - Pushes the changes to the repository
  
The dates displayed on the site are determined by the minDate and maxDate values in script.js. The currentDate value determines which date is shown when the user first opens the site on a given day:
 - update_dates.py:
   - Opens the script.js and incrementes the currentDate and maxDate values by one day

 - update_dates.yml:
   - GitHub Action triggered everyday at 12:10 AM CDT
   - Runs the update_dates.py script
   - Pushes the changes to the repository


