async function submitYearPlayer() {
  const yearInput = document.getElementById("year").value.trim();
  if (yearInput) {
    if (yearInput < 2012 || yearInput > 2024) {
      alert("Please enter a year between 2012 and 2024");
      return;
    } else if (yearInput == 2020) {
      alert(
        "The 2020 season was compromised due to COVID-19. Please select a different year."
      );
      return;
    }
    try {
      const response = await fetch(
        `https://www.backend.ufastats.com/api/v1/players?years=${yearInput}`
      );
      const players = await response.json();

      const select = document.getElementById("player");
      select.innerHTML = ""; // Clear existing options

      const defaultOption = document.createElement("option");
      defaultOption.value = "";
      defaultOption.color = "grey";
      defaultOption.textContent = "Select or type a player";
      select.appendChild(defaultOption);

      players.data.forEach((player) => {
        const option = document.createElement("option");
        const fullName = `${player.firstName} ${player.lastName}`;

        option.value = player.playerID; // Adjust based on your API response
        option.textContent = fullName;
        select.appendChild(option);
      });

      if (window.playerChoices) {
        window.playerChoices.destroy();
      }

      document.getElementById("player").disabled = false;
      document.getElementById("year").readOnly = true;
      document.getElementById("player").style.display = "inline-block";
      document.getElementById("submitButton").style.display = "inline-block";
      const choices = new Choices("#player", {
        searchEnabled: true,
        placeholder: true,
        placeholderValue: "Select or type a player",
        shouldSort: false,
        position: "auto",
        removeItemButton: true,
      });
    } catch (error) {
      console.error("Error fetching players and creating dropdown:", error);
    }
  } else {
    alert("Please enter a year");
  }
}

async function submitYearTeam() {
  const yearInput = document.getElementById("year").value.trim();
  if (yearInput) {
    if (yearInput < 2012 || yearInput > 2024) {
      alert("Please enter a year between 2012 and 2024");
      return;
    } else if (yearInput == 2020) {
      alert(
        "The 2020 season was compromised due to COVID-19. Please select a different year."
      );
      return;
    }
    try {
      const response = await fetch(
        `https://www.backend.ufastats.com/api/v1/teams?years=${yearInput}`
      );
      const teams = await response.json();

      const select = document.getElementById("team");
      select.innerHTML = ""; // Clear existing options

      const defaultOption = document.createElement("option");
      defaultOption.value = "";
      defaultOption.color = "grey";
      defaultOption.textContent = "Select or type a team";
      select.appendChild(defaultOption);

      teams.data.forEach((team) => {
        const option = document.createElement("option");
        option.value = team.teamID; // Adjust based on your API response
        option.textContent = team.fullName;
        select.appendChild(option);
      });

      if (window.playerChoices) {
        window.playerChoices.destroy();
      }
      document.getElementById("team").disabled = false;
      document.getElementById("team").style.display = "inline-block";
      document.getElementById("year").readOnly = true;
      document.getElementById("submitButton").style.display = "inline-block";
      const choices = new Choices("#team", {
        searchEnabled: true,
        placeholder: true,
        placeholderValue: "Select or type a team",
        position: "auto",
        shouldSort: false,
        removeItemButton: true,
      });
    } catch (error) {
      console.error("Error fetching teams and creating dropdown:", error);
    }
  } else {
    alert("Please enter a year");
  }
}
function enablePlayerForm() {
  const yearInput = document.getElementById("year").value.trim();
  const playerField = document.getElementById("player");
  const yearButton = document.getElementById("year-submit");
  const sznField = document.getElementById("sznOrGame");

  if (yearInput) {
    yearButton.disabled = false;
    playerField.disabled = false;
    sznField.disabled = false;
  } else {
    yearButton.disabled = true;
  }
}
function enableTeamForm() {
  const yearInput = document.getElementById("year").value.trim();
  const teamField = document.getElementById("team");
  const yearButton = document.getElementById("year-submit");

  if (yearInput) {
    yearButton.disabled = false;
    teamField.disabled = false;
  } else {
    yearButton.disabled = true;
  }
}
function validateFormPlayer() {
  const playerInput = document.getElementById("player").value.trim();
  const yearInput = document.getElementById("year").value.trim();

  if (!playerInput || playerInput === "Select or type a player") {
    alert("Please select a player");
    return false;
  }
  if (!yearInput || !playerInput) {
    alert("Both fields are required.");
    return false;
  }
  return true;
}

function validateFormTeam() {
  const teamInput = document.getElementById("team").value.trim();
  const yearInput = document.getElementById("year").value.trim();

  if (!teamInput || teamInput === "Select or type a team") {
    alert("Please select a team");
    return false;
  }
  if (!yearInput || !teamInput) {
    alert("Both fields are required.");
    return false;
  }
  return true;
}
let games;
async function gameOrSzn() {
  const sznOrGame = document.getElementById("sznOrGame");
  const gamesList = document.getElementById("games");
  
  if (sznOrGame.value === "game" ) {  
    let playerID = document.getElementById("player").value.trim();
    let year = document.getElementById("year").value.trim();

    gamesList.innerHTML = ""; // Clear existing options
    const def = document.createElement("option");
    def.value = "";
    def.color = "grey";
    def.textContent = "Select or type a game";
    gamesList.appendChild(def);
    gamesList.disabled = false;
    gamesList.style.display = "inline-block";
    games = new Choices("#games", {
      searchEnabled: true,
      placeholder: true,
      placeholderValue: "Select or type a game",
      shouldSort: false,
      position: "auto",
      removeItemButton: true,
    });
    await populateGames(games, year, playerID);
  } else {
    console.log("hi");
    gamesList.disabled = true;
    
      games.destroy();
      games = null;
      gamesList.style.display = "none"; 

    // Remove all options
    while (gamesList.firstChild) {
      gamesList.removeChild(gamesList.firstChild);
    }
  }
}

async function populateGames(games, year, playerID){
try {
  const teamResponse = await fetch(
    `https://www.backend.ufastats.com/api/v1/players?playerIDs=${playerID}&years=${year}`
  );
  const teamJson = await teamResponse.json();
  team = teamJson.data[0].teams[0].teamID;
  
  const gamesResponse = await fetch(
    `https://www.backend.ufastats.com/api/v1/games?date=${year}`
  );
  const gamesJson = await gamesResponse.json();
  gamesJson.data.forEach((game) => {
    if (game.awayTeamID === team || game.homeTeamID === team){
      
      games.setChoices([
        {
          value: game.gameID,
          label: game.gameID,
          selected: false,
          disabled: false,
        },
      ], 'value', 'label', false);
    }
  });
} catch (error) {
  console.error("Error fetching teams and creating dropdown:", error);
}
}

function onPlayerInput(){
  const sznOrGameDropdown = document.getElementById('sznOrGame');
  sznOrGameDropdown.disabled = false;
  sznOrGameDropdown.style.display = "inline-block";
}
