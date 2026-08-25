from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def chess_game():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Mini Chess Game</title>
        <!-- Include chess.js for robust legal move validation -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/chess.js/0.10.3/chess.min.js"></script>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; margin-top: 20px; background-color: #f4f4f9; }
            .card { background: white; padding: 20px; border-radius: 12px; display: inline-block; box-shadow: 0px 4px 12px rgba(0,0,0,0.1); }
            #status { font-size: 18px; font-weight: bold; margin-bottom: 15px; color: #1e293b; }
            .board { display: grid; grid-template-columns: repeat(8, 50px); grid-template-rows: repeat(8, 50px); border: 4px solid #334155; margin: 0 auto; width: 400px; height: 400px; }
            .square { width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; font-size: 32px; cursor: pointer; user-select: none; }
            .light { background-color: #f0d9b5; }
            .dark { background-color: #b58863; }
            .selected { background-color: #7b61ff !important; }
            button { padding: 10px 20px; font-size: 16px; background-color: #0f172a; color: white; border: none; border-radius: 6px; cursor: pointer; margin-top: 15px; }
            button:hover { background-color: #334155; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>♟️ Interactive Chess Board</h2>
            <div id="status">White's Turn</div>
            <div class="board" id="board"></div>
            <button onclick="resetGame()">Reset Game</button>
        </div>

        <script>
            const game = new Chess();
            
            const pieceSymbols = {
                'p': '♟', 'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚',
                'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔'
            };

            let selectedSquare = null;

            function renderBoard() {
                const boardEl = document.getElementById('board');
                boardEl.innerHTML = '';
                
                const boardState = game.board();
                
                for (let r = 0; r < 8; r++) {
                    for (let c = 0; c < 8; c++) {
                        const square = document.createElement('div');
                        const isDark = (r + c) % 2 === 1;
                        square.className = `square ${isDark ? 'dark' : 'light'}`;
                        
                        const file = String.fromCharCode(97 + c);
                        const rank = 8 - r;
                        const squareID = file + rank;

                        if (selectedSquare === squareID) {
                            square.classList.add('selected');
                        }

                        const piece = boardState[r][c];
                        if (piece) {
                            const symbolKey = piece.color === 'w' ? piece.type.toUpperCase() : piece.type;
                            square.innerText = pieceSymbols[symbolKey] || '';
                        }

                        square.onclick = () => handleSquareClick(squareID);
                        boardEl.appendChild(square);
                    }
                }
                updateStatus();
            }

            function handleSquareClick(squareID) {
                if (selectedSquare === null) {
                    const piece = game.get(squareID);
                    if (piece && piece.color === game.turn()) {
                        selectedSquare = squareID;
                        renderBoard();
                    }
                } else {
                    const move = game.move({
                        from: selectedSquare,
                        to: squareID,
                        promotion: 'q'
                    });

                    selectedSquare = null;

                    if (move === null) {
                        const piece = game.get(squareID);
                        if (piece && piece.color === game.turn()) {
                            selectedSquare = squareID;
                        }
                    }
                    renderBoard();
                }
            }

            function updateStatus() {
                let statusMsg = '';
                const turnName = game.turn() === 'w' ? "White's Turn" : "Black's Turn";

                if (game.in_checkmate()) {
                    statusMsg = `Game Over! Checkmate. ${game.turn() === 'w' ? 'Black' : 'White'} wins!`;
                } else if (game.in_draw()) {
                    statusMsg = `Game Over! Drawn position.`;
                } else {
                    statusMsg = turnName;
                    if (game.in_check()) {
                        statusMsg += ` — CHECK!`;
                    }
                }
                document.getElementById('status').innerText = statusMsg;
            }

            function resetGame() {
                game.reset();
                selectedSquare = null;
                renderBoard();
            }

            renderBoard();
        </script>
    </body>
    </html>
    """
