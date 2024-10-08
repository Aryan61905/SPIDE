const terminal = document.getElementById('terminal');
const input = document.getElementById('input');
const commandHistory = document.getElementById('command-history');
const homeMenu = document.getElementById('home-menu');
const historyContainer = document.getElementById('history');
const apiUrl = 'http://127.0.0.1:8000/api/terminal';
const searchUrl = 'http://127.0.0.1:8000/api/prompt';
var dataHistory ={};
document.addEventListener('DOMContentLoaded', function() {
  const inputField = document.getElementById('input');
  const autocompleteContainer = document.getElementById('autocomplete-container');
  
  inputField.addEventListener('input', function(event) {
    const inputValue = event.target.value.trim();
    if (inputValue.startsWith('--player') && !inputValue.includes('--stats')){
      const searchTerm = inputValue.substring(9).trim(); // Remove '--player' and trim whitespace
      fetchPlayerNames(searchTerm); // Function to fetch player names (can be AJAX call or predefined list)
    } 
    else if (inputValue.includes('--stats'))
    {
      updateAutocomplete(["PTS","AVG","TRB"]);
    }
    else {
      clearAutocomplete();
    }
  });
  
  function fetchPlayerNames(searchTerm) {
    // Replace this with your actual data fetching logic, like an AJAX call
    {
      
      fetch(searchUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ searchTerm })
      })
        .then(response => response.json())
        .then(data => {
          const matchedPlayers = data
          updateAutocomplete(matchedPlayers.slice(0, 5)); 
        })
        .catch(error => {
          console.error('Error:', error);
          appendOutput(`<div>Error: ${error}</div>`); // Display error if any
        });
    }
   // Limiting to 5 results
  }
  
  function updateAutocomplete(playerList) {
    autocompleteContainer.innerHTML = ''; // Clear previous autocomplete options
    
    playerList.forEach(player => {
      const option = document.createElement('div');
      option.textContent = player;
      option.classList.add('autocomplete-option');
      
      // Click event to populate input field
      option.addEventListener('click', function() {
        inputField.value = `--player ${player}`;
        clearAutocomplete();
      });
      
      autocompleteContainer.appendChild(option);
    });
    
    if (playerList.length > 0) {
      autocompleteContainer.style.display = 'block'; // Show autocomplete options
    } else {
      autocompleteContainer.style.display = 'none'; // Hide if no options
    }
  }
  
  function clearAutocomplete() {
    autocompleteContainer.innerHTML = '';
    autocompleteContainer.style.display = 'none';
  }
  
  // Hide autocomplete options when clicking outside the input field
  document.addEventListener('click', function(event) {
    if (!event.target.closest('#input-container')) {
      clearAutocomplete();
    }
  });
});

function appendOutput(text) {
  terminal.innerHTML += `<div>${text}</div>`;
  terminal.scrollTop = terminal.scrollHeight;
}

function appendToHistory(command,data) {
  
  const li = document.createElement('li');
  li.textContent = command;
  commandHistory.appendChild(li);
  dataHistory[command] = command
  
  for (const playerName in data){
      dataHistory[data[playerName][0]] = data[playerName]
  }
  }
  


function clearTerminal() {
  terminal.innerHTML = '';
}

function clearCommandHistory() {
  commandHistory.innerHTML = '';
}

// Add a function to clear both terminal output and command history
function clearAll() {
  clearTerminal();
  clearCommandHistory();
}

// Process the "clear" command
function processClearCommand(command) {
  const parts = command.split(' ');
  if (parts.length === 1) {
    clearAll();
    appendOutput('<div>Terminal and history cleared.</div>');
  } else if (parts.length === 2) {
    const option = parts[1].toUpperCase();
    if (option === '-T') {
      clearTerminal();
      appendOutput('<div>Terminal cleared.</div>');
    } else if (option === '-H') {
      clearCommandHistory();
      appendOutput('<div>History cleared.</div>');
    } else {
      appendOutput('<div>Invalid option. Usage: clr [-T | -H]</div>');
    }
  } else {
    appendOutput('<div>Invalid command. Usage: clr [-T | -H]</div>');
  }
}

// Get the button element
const togglePanelButton = document.getElementById('togglePanelButton');
const content = document.getElementById('content');

togglePanelButton.addEventListener('click', function() {
  // Toggle the class to expand or collapse the side panel
  homeMenu.classList.toggle('expanded');
  historyContainer.classList.toggle('expanded');
  content.classList.toggle('expanded');
});

// After generating the table content dynamically, add Swiper to each table
// After generating the table content dynamically, add Swiper to each card container






// Add event listener for input field
input.addEventListener('keydown', function(event) {
  if (event.key === 'ArrowUp')
  {
   
  }
  if (event.key === 'Enter') {
    handleInput();
  }
});

// Add event listeners to header cells to display chart
function displayData(data) {
  for (const playerName in data) {
    if (typeof(data[playerName])!=='string'){
    const playerData = data[playerName];
    const cardContainer = document.createElement('div'); 
    cardContainer.classList.add('card-container'); 
    
    const mainTableData = playerData.slice(0, -1); 
    const avgStats = playerData[playerData.length - 1]['AVG'];
    
    
    const card = document.createElement('div');
    card.classList.add('card'); // Add a class for styling
    card.setAttribute('id',playerName+'_card');
    const rightSlider = document.createElement('div');
    rightSlider.classList.add('slider');
    rightSlider.setAttribute('id','rightSlider');
    rightSlider.innerHTML = "&nbsp;&#x25BC;";
    
    // Create a table element for the player's data
    const mainTable = document.createElement('table');
    mainTable.setAttribute('id',playerName+'_table');
    mainTable.classList.add('terminal-table');

    // Add header row to the main table
    const headerRow = document.createElement('tr');
    for (const header of mainTableData[0]) {
      const th = document.createElement('th');
      th.textContent = header;
      headerRow.appendChild(th);
    }
    
    mainTable.appendChild(headerRow);

    // Add data rows to the main table
    for (let i = 1; i < mainTableData.length; i++) {
      const row = document.createElement('tr');
      const rowData = mainTableData[i];

      // Check each stat against its average
      for (let j = 0; j < rowData.length; j++) {
        const cell = document.createElement('td');
        cell.textContent = rowData[j];

        // Apply color change if the stat is greater than or equal to its average
        if (rowData[j] >= avgStats[mainTableData[0][j]]) {
          cell.style.color =  '#00ff00'; 
          
        } else if (rowData[j] < avgStats[mainTableData[0][j]]) {
          cell.style.color = '#ff0000';
        }

        row.appendChild(cell);
      }
      mainTable.appendChild(row);
    }

    const avgHeaderRow = document.createElement('tr');
    const thAvg = document.createElement('td');
    thAvg.textContent = 'AVG';
    avgHeaderRow.appendChild(thAvg);
    mainTable.appendChild(avgHeaderRow);

  for (let j = 1; j < mainTableData[0].length; j++) {
    const header = mainTableData[0][j];
    const avgCell = document.createElement('td');
    avgCell.textContent = avgStats[header];
    avgHeaderRow.appendChild(avgCell);
}
    card.appendChild(mainTable);
    card.appendChild(rightSlider);

    cardContainer.appendChild(card);
    terminal.appendChild(cardContainer);
    
    rightSlider.addEventListener('click', function(event) {
      // Toggle the class to expand or collapse the side panel
      var cardDiv = event.target.closest('.card');
      var cardClassName = cardDiv.id;
      console.log("Clicked on card:", cardClassName.slice(0,-5));
      console.log(dataHistory[cardClassName.slice(0,-5)][0]);
      console.log(dataHistory[cardClassName.slice(0,-5)][0].slice(1));
      console.log(dataHistory[cardClassName.slice(0,-5)].slice(1,-1));
      data = dataHistory[cardClassName.slice(0,-5)].slice(1,-1);
      const xLabels = data.map(row => row[0].slice(-2)).reverse();
      const datasets = dataHistory[cardClassName.slice(0,-5)][0].slice(1).map((label, index) => ({
        label: label,
        data: data.map(row => row[index + 1]).reverse(),
        fill: false,
        borderColor: '#' + (Math.random().toString(16) + '000000').substring(2, 8).toUpperCase(),
        backgroundColor: '#' + (Math.random().toString(16) + '000000').substring(2, 8).toUpperCase(),
        
        shadowBlur: 5, // Adjust blur amount (higher for more glow)
        shadowColor: 'rgba(0, 0, 0, 0.5)', // Set shadow color with some transparency
    })
    );
    
    // Create a single chart with all datasets
    const canvas = document.createElement('canvas');
    const chartDiv = document.createElement('div');
    chartDiv.setAttribute('id','chartDiv');
    canvas.setAttribute('id','canvas');
    
    let existingCanvas = cardDiv.querySelector('canvas');

    if (existingCanvas) {
      existingCanvas.parentNode.removeChild(existingCanvas);
      rightSlider.innerHTML = "&nbsp;&#x25BC;";
      
    }
    else
    {
    chartDiv.appendChild(canvas);
    cardDiv.appendChild(chartDiv);
    rightSlider.innerHTML = "&nbsp;&#x25B2;";
    
    } // Appending canvas to body
    
    new Chart(canvas.getContext('2d'), {
        type: 'line',
        data: {
            labels: xLabels,
            datasets: datasets,
        },
        
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'X Label'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Y Label'
                    }
                }
            }
        }
    }
    );

    });
  }
  
}
}

// Function to process user input
function processCommand(command) {
  appendToHistory(command,{});
  
  if (command.toLowerCase().startsWith('clr')) {
    processClearCommand(command);
  } else {
    fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ command })
    })
      .then(response => response.json())
      .then(data => {
        clearTerminal();
        appendOutput(`<div> &gt; ${command}</div>`);
        appendToHistory(command,data);
        
        displayData(dataHistory);
        
        
      })
      .catch(error => {
        console.error('Error:', error);
        appendOutput(`<div>Error: ${error}</div>`); // Display error if any
      });
  }
}

// Function to handle user input
function handleInput() {
  const command = input.value.trim();
  if (command !== '') {
    
    processCommand(command);
    input.value = '';
  }
}



// Initial focus on input field
input.focus();