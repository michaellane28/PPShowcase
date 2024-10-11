/*
    script.js
    
        - Responsible for formatting index.html elements

        - Sets  minimum and maximum dates that will be shown on the website at any given time
            - Values are updated via GitHub Actions
        
        -
*/

// Load and parse Excel files
const readExcelFile = (filePath, callback) => {
    fetch(filePath)
        .then(response => response.arrayBuffer())
        .then(arrayBuffer => {
            const workbook = XLSX.read(arrayBuffer, { type: 'array' });
            const sheetName = workbook.SheetNames[0];
            const worksheet = workbook.Sheets[sheetName];
            const data = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
            callback(data);
        });
};

// Global variables
let playersData = [];
let scheduleData = [];
const minDate = new Date(Date.UTC(2024, 9, 4)); 
const maxDate = new Date(Date.UTC(2024, 11, 20)); // UPDATED BY GITHUB ACTION
let currentDate = new Date(Date.UTC(2024, 11, 20)); // UPDATED BY GITHUB ACTION

// DOM elements
const currentDateElem = document.getElementById("currentDate");
const prevDateButton = document.getElementById("prevDate");
const nextDateButton = document.getElementById("nextDate");
const gamesList = document.getElementById('gamesList');
const noGamesImage = document.getElementById('noGamesImage');

// Format date as MM/DD/YYYY
const formatDate = (date) => {
    const day = String(date.getUTCDate()).padStart(2, '0');
    const month = String(date.getUTCMonth() + 1).padStart(2, '0'); 
    const year = date.getUTCFullYear();
    return `${month}/${day}/${year}`;
};

// Get player image URL
const getPlayerImage = (playerName) => {
    const normalizedPlayerName = playerName.toLowerCase(); // Normalize input name to lowercase
    const player = playersData.find(p => p.name.toLowerCase() === normalizedPlayerName); // Normalize names in data to lowercase
    if (player && player.imageUrl) {
        console.log('Player Image URL:', player.imageUrl); // Debugging line
        return player.imageUrl;
    } else {
        console.log('Player Image URL: Not found, using default image'); // Debugging line
        return 'default-skater.png'; // Default image for players not found in player dataset
    }
};

// Get team logo
const getTeamLogo = (teamName) => {
    const normalizedTeamName = teamName.toLowerCase().replace(/ /g, '_');
    const fileName = normalizedTeamName + '.png';
    return `/NHL_Team_Logos/${fileName}`;
};

// Display games for the current date
const displayGames = () => {
    gamesList.innerHTML = '';

    const games = scheduleData.filter(game => game.date === formatDate(currentDate));

    if (games.length === 0) {
        noGamesImage.style.display = 'block'; // Show the image
    } else {
        noGamesImage.style.display = 'none'; // Hide the image
        games.forEach(game => {
            const player1Image = getPlayerImage(game.player1);
            const player2Image = getPlayerImage(game.player2);
            const teamLogo = getTeamLogo(game.team);

            const gameItem = document.createElement('div');
            gameItem.className = 'game-item';
            gameItem.innerHTML = `
                <div class="players-info">
                    <div class="player">
                        <img src="${player1Image}" alt="${game.player1}" class="player-image">
                        <span class="player-name">${game.player1}</span>
                    </div>
                    <div class="game-plus">
                        <span class="plus">+</span>
                    </div>
                    <div class="player">
                        <img src="${player2Image}" alt="${game.player2}" class="player-image">
                        <span class="player-name">${game.player2}</span>
                    </div>
                    <div class="game-vs">
                        <span class="vs">vs</span>
                    </div>
                    <div class="team-info">
                        <img src="${teamLogo}" alt="${game.team} logo" class="team-logo">
                        <span class="team-name">${game.team}</span>
                    </div>
                </div>
                <div class="game-time">
                    <span>${game.time} ET</span>
                </div>
            `;
            gamesList.appendChild(gameItem);
        });
    }
};

// Load data from Excel files
const loadData = () => {
    return Promise.all([
        new Promise((resolve) => {
            readExcelFile('nhl_players.xlsx', (data) => {
                playersData = data.slice(1).map(row => ({ name: row[0].toLowerCase(), imageUrl: row[1] }));
                console.log('Players Data:', playersData); // Debugging line
                resolve();
            });
        }),
        new Promise((resolve) => {
            readExcelFile('filtered_schedule.xlsx', (data) => {
                scheduleData = data.slice(1).map(row => ({
                    date: row[0],
                    time: row[1],
                    team: row[2].toLowerCase(),
                    player1: row[3].toLowerCase(),
                    player2: row[4].toLowerCase()
                }));
                resolve();
            });
        })
    ]);
};

// Update date display and games list
const updateDate = () => {
    currentDateElem.textContent = formatDate(currentDate);
    prevDateButton.style.display = currentDate > minDate ? 'inline' : 'none';
    nextDateButton.style.display = currentDate < maxDate ? 'inline' : 'none';
    displayGames();
};

// Event listeners for date navigation
prevDateButton.addEventListener("click", () => {
    if (currentDate > minDate) {
        currentDate.setUTCDate(currentDate.getUTCDate() - 1);
        updateDate();
    }
});

nextDateButton.addEventListener("click", () => {
    if (currentDate < maxDate) {
        currentDate.setUTCDate(currentDate.getUTCDate() + 1);
        updateDate();
    }
});

// Initial data load and display
loadData().then(() => {
    updateDate();
});

// Add this to your script.js
document.addEventListener('scroll', () => {
    const dateSlider = document.querySelector('.date-slider');
    const firstGameItem = document.querySelector('.game-item');

    if (firstGameItem) {
        const dateSliderBottom = dateSlider.getBoundingClientRect().bottom;
        const firstGameItemTop = firstGameItem.getBoundingClientRect().top;

        if (firstGameItemTop > dateSliderBottom) {
            dateSlider.classList.remove('shadow');
        } else {
            dateSlider.classList.add('shadow');
        }
    }
});