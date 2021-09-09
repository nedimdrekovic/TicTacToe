# TicTacToe

TicTacToe-Spiel, bei dem der Spieler gegen den Computer antritt (https://www.spielbanken.com/tic-tac-toe/).

## Spieler:
- ist solange an der Reihe bis auf ein freies Feld geklickt wird und "X" platziert wird

## Computer
- in Abhängigkeit vom Zug des Spielers wird mithilfe eines Algorithmus das für den Computer bestmögliche Feld ausgewählt und mit "O" belegt.
- als Algorithmus wird der Minimax-Algorithmus verwendet.


## Minimax-Algorithmus
- Der Computer bestimmt nach dem Zug des Spielers alle möglichen Spielvariationen, die ausgehend vom aktuellen Zug noch möglich sind.
- Jeder mögliche Variation, die zum Sieg des Spielers führt, wird der Wert "1" zugeordnet
- Jeder mögliche Variation, die zum Sieg des Computers führt, wird der Wert "-1" zugeordnet
- Ein Unentschieden ergibt den Wert "0"

Diese Variationen werden in einer Baumstruktur aufgeführt.
Der Spieler bezweckt eine Maximierung seiner Auswahl in seinem Zug und eine Minimierung im Spielzug des Computers.

<p align='center'>
    <img src="https://user-images.githubusercontent.com/73491052/132740269-4c19a718-c04c-4cf4-92a5-14dc71765a16.png" width=360>
</p>








