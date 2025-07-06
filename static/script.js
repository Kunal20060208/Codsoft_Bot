// static/script.js (Updated)

document.addEventListener("DOMContentLoaded", function () {
  function runTask(task) {
    const output = document.getElementById("output");
    if (output) {
      output.innerHTML = `Running <strong>${task}</strong> module...`;

      setTimeout(() => {
        switch (task) {
          case "chatbot":
            output.innerHTML = "Chatbot says: Hello! I'm Codsoft Bot, your AI buddy!";
            break;
          case "tictactoe":
            output.innerHTML = "Tic Tac Toe: Coming soon as interactive web game!";
            break;
          case "caption":
            output.innerHTML = "Upload an image feature coming soon... Stay tuned!";
            break;
          case "recommend":
            output.innerHTML = "Top Picks: Inception, Interstellar, Avengers...";
            break;
          case "face":
            output.innerHTML = "Face Detection: Requires camera permission. Coming soon!";
            break;
          default:
            output.innerHTML = "Unknown task selected.";
        }
      }, 1000);
    }
  }

  const video = document.getElementById('video');
  if (video) {
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(stream => {
        video.srcObject = stream;
      })
      .catch(err => {
        alert("Failed to access webcam: " + err);
        console.error("Webcam error:", err);
      });
  }

  const board = document.getElementById('board');
  const status = document.getElementById('status');
  if (board && status) {
    let cells = Array(9).fill(null);
    let currentPlayer = 'X';

    function checkWinner() {
      const wins = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
      ];
      for (let combo of wins) {
        const [a, b, c] = combo;
        if (cells[a] && cells[a] === cells[b] && cells[a] === cells[c]) {
          return cells[a];
        }
      }
      return cells.includes(null) ? null : 'Draw';
    }

    function handleClick(i, cell) {
      if (cells[i] || checkWinner()) return;
      cells[i] = currentPlayer;
      cell.textContent = currentPlayer;
      const winner = checkWinner();
      if (winner) {
        status.textContent = winner === 'Draw' ? 'It\'s a Draw!' : `${winner} wins!`;
      }
      currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
    }

    function renderBoard() {
      board.innerHTML = '';
      cells.forEach((value, i) => {
        const cell = document.createElement('div');
        cell.className = 'cell';
        cell.textContent = value || '';
        cell.onclick = () => handleClick(i, cell);
        board.appendChild(cell);
      });
    }

    renderBoard();
    document.getElementById('reset')?.addEventListener('click', () => {
      cells.fill(null);
      currentPlayer = 'X';
      status.textContent = '';
      renderBoard();
    });
  }

  const chatBox = document.getElementById('chatBox');
  const chatForm = document.getElementById('chatForm');
  const userInput = document.getElementById('userInput');
  if (chatForm && chatBox && userInput) {
    const responses = {
      hello: "Hello! How can I assist you?",
      name: "I'm Codsoft Bot, your AI assistant.",
      bye: "Goodbye! Come back soon."
    };

    chatForm.onsubmit = (e) => {
      e.preventDefault();
      const input = userInput.value.trim();
      if (!input) return;

      chatBox.innerHTML += `<p class='message user'><strong>You:</strong> ${input}</p>`;

      let response = "I'm still learning to respond to that.";
      for (let keyword in responses) {
        if (input.toLowerCase().includes(keyword)) {
          response = responses[keyword];
          break;
        }
      }

      chatBox.innerHTML += `<p class='message bot'><strong>Codsoft Bot:</strong> ${response}</p>`;
      userInput.value = "";
      chatBox.scrollTop = chatBox.scrollHeight;
    };
  }
});

document.addEventListener("contextmenu", e => e.preventDefault());

document.querySelectorAll("input[type='text'], input[type='file']").forEach(input => {
  input.value = "";
  input.autocomplete = "off";
});
