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
            <h2>♟️ Mini Chess Board</h2>
            <div id="status">White's Turn (Click a piece to move)</div>
            <div class="board" id="board"></div>
            <button onclick="resetGame()">Reset Game</button>
        </div>

        <script>
            const pieces = {
                'r': '∜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
                'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙',
                '': ''
            };

            let board = [
                ['r','n','b','q','k','b','n','r'],
                ['p','p','p','p','p','p','p','p'],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['P','P','P','P','P','P','P','P'],
                ['R','N','B','Q','K','B','N','R']
            ];

            let turn = 'White';
            let selectedPiece = null;

            function renderBoard() {
                const boardEl = document.getElementById('board');
                boardEl.innerHTML = '';
                for (let r = 0; r < 8; r++) {
                    for (let c = 0; c < 8; c++) {
                        const square = document.createElement('div');
                        const isDark = (r + c) % 2 === 1;
                        square.className = `square ${isDark ? 'dark' : 'light'}`;
                        if (selectedPiece && selectedPiece.r === r && selectedPiece.c === c) {
                            square.classList.add('selected');
                        }
                        
                        const pieceCode = board[r][c];
                        square.innerText = pieceCode ? pieces[pieceCode] : '';
                        square.onclick = () => handleSquareClick(r, c);
                        boardEl.appendChild(square);
                    }
                }
            }

            function handleSquareClick(r, c) {
                const piece = board[r][c];
                
                if (selectedPiece) {
                    // Move piece
                    board[r][c] = board[selectedPiece.r][selectedPiece.c];
                    board[selectedPiece.r][selectedPiece.c] = '';
                    selectedPiece = null;
                    turn = turn === 'White' ? 'Black' : 'White';
                    document.getElementById('status').innerText = `${turn}'s Turn`;
                    renderBoard();
                } else if (piece) {
                    // Select piece
                    const isWhite = piece === piece.toUpperCase();
                    if ((turn === 'White' && isWhite) || (turn === 'Black' && !isWhite)) {
                        selectedPiece = { r, c };
                        renderBoard();
                    }
                }
            }

            function resetGame() {
                board = [
                    ['r','n','b','q','k','b','n','r'],
                    ['p','p','p','p','p','p','p','p'],
                    ['','','','','','','',''],
                    ['','','','','','','',''],
                    ['','','','','','','',''],
                    ['','','','','','','',''],
                    ['P','P','P','P','P','P','P','P'],
                    ['R','N','B','Q','K','B','N','R']
                ];
                turn = 'White';
                selectedPiece = null;
                document.getElementById('status').innerText = "White's Turn (Click a piece to move)";
                renderBoard();
            }

            renderBoard();
        </script>
    </body>
    </html>
    """
