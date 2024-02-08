const terminal = document.getElementById('terminal');
const input = document.getElementById('input');
const commandHistory = document.getElementById('command-history');
const homeMenu = document.getElementById('home-menu');
const historyContainer = document.getElementById('history');
const apiUrl = 'http://127.0.0.1:8000/api/terminal';

function appendOutput(text) {
  terminal.innerHTML += `<div>${text}</div>`;
  terminal.scrollTop = terminal.scrollHeight;
}

function appendToHistory(command) {
  const li = document.createElement('li');
  li.textContent = command;
  commandHistory.appendChild(li);
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
  console.log("clicked")
  homeMenu.classList.toggle('expanded');
  historyContainer.classList.toggle('expanded');
  content.classList.toggle('expanded');
});


function displayData(data) {
  for (const playerName in data) {
    const playerData = data[playerName];
    const container = document.createElement('div');
    //container.innerHTML = `<h3>${playerName}</h3>`;
    
    const mainTableData = playerData.slice(0, -1); // Exclude the last element
    const avgStats = playerData[playerData.length - 1]['AVG'];
    console.log(avgStats);
    const mainTable = document.createElement('table');
    mainTable.classList.add('terminal-table');
    
    // Add header row
    const headerRow = document.createElement('tr');
    for (const header of mainTableData[0]) {
      const th = document.createElement('th');
      th.textContent = header;
      headerRow.appendChild(th);
    }
    mainTable.appendChild(headerRow);
    
    // Add data rows and apply color changes
    for (let i = 1; i < mainTableData.length; i++) {
      const row = document.createElement('tr');
      const rowData = mainTableData[i];
      
      // Check each stat against its average
      for (let j = 0; j < rowData.length; j++) {
        const cell = document.createElement('td');
        cell.textContent = rowData[j];
        
        // Apply color change if the stat is greater than or equal to its average
        if (rowData[j] >= avgStats[mainTableData[0][j]]) {
          cell.style.color = 'green';
        }
        else if (rowData[j] < avgStats[mainTableData[0][j]])
        {
          cell.style.color = 'red';
        }
        
        row.appendChild(cell);
      }
      mainTable.appendChild(row);
    }
    
    container.appendChild(mainTable);
    
    // Display average stats table if it exists
    const avgStatsTable = playerData[playerData.length - 1]['AVG'];
    if (Object.keys(avgStatsTable).length > 0) {
      const avgTable = document.createElement('table');
      avgTable.classList.add('terminal-table');
      
      const headerRow = document.createElement('tr');
      const th1 = document.createElement('th');
      th1.textContent = 'Stat';
      const th2 = document.createElement('th');
      th2.textContent = 'Average';
      headerRow.appendChild(th1);
      headerRow.appendChild(th2);
      avgTable.appendChild(headerRow);
      
      for (const stat in avgStatsTable) {
        const row = document.createElement('tr');
        const cell1 = document.createElement('td');
        cell1.textContent = stat;
        const cell2 = document.createElement('td');
        cell2.textContent = avgStatsTable[stat];
        row.appendChild(cell1);
        row.appendChild(cell2);
        avgTable.appendChild(row);
      }
      
      container.appendChild(avgTable);
    }
    
    terminal.appendChild(container);
  }
}





// Modify the processCommand function to handle the "clear" command
function processCommand(command) {
  appendOutput(`<div> &gt; ${command}</div>`);
  appendToHistory(command);
  
  if (command.toLowerCase().startsWith('clr')) {
    processClearCommand(command);
  }
  else{
  fetch(apiUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ command })
  })
  .then(response => response.json())
  .then(data => {
    displayData(data)
  }
  )
  .catch(error => {
    console.error('Error:', error);
    appendOutput(`<div>Error: ${error}</div>`); // Display error if any
  });
  }
}

function handleInput() {
  const command = input.value.trim();
  if (command !== '') {
    processCommand(command);
    input.value = '';
  }
}



input.addEventListener('keydown', function(event) {
  if (event.key === 'Enter') {
    handleInput();
  }
});

input.focus();
