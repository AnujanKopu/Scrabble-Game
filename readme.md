# Scrabble-Game  
My attempt at creating a Scrabble game.  

Menu:
![image](https://github.com/user-attachments/assets/33d8ada6-e76a-4cc1-9b32-e519239fec46)

Game Options:
![image](https://github.com/user-attachments/assets/87d69809-6758-43ed-8d66-14373b9fd6b7)

Making Moves(Green Border:
![image](https://github.com/user-attachments/assets/41482167-ffe2-444a-b94a-d1cab735031f)

Shuffling(Yellow Border):
![image](https://github.com/user-attachments/assets/7d8a91d3-822b-4637-a339-8b4e7fe688d6)

Challenging:
![image](https://github.com/user-attachments/assets/aac396d2-51a2-4b1e-ad0c-5e8b401574db)
![image](https://github.com/user-attachments/assets/4b39c07e-2aa2-4993-84a9-dd8b9afdf58a)
![image](https://github.com/user-attachments/assets/f915db5b-a45c-4343-967e-c183bbbb09a7)

## Rules  
- **First player** – The player with the deck with the lowest lexicographical value goes first.  
- **First play** – Earns **2x points**.  
- **Starting position** – The first tile must be placed on the star in the center, and all subsequent words must build off existing tiles.  
- **Word placement** – Words must be placed linearly in either a **top-down** or **left-right** direction. Any other placements will not be accepted.   

## Player Actions  
On each turn, a player can:  
- **Play a word** – Place tiles on the board, then press **`P`** to submit the play.  
- **Shuffle tiles** – Press **`S`** to activate Shuffle Mode, then click on the tiles you want to shuffle. Press **`S`** again to confirm.  
  - **(Shuffling forfeits your turn.)**  
- **Challenge a word** – Other players can press **`C`** within an **8-second challenge window** after a word is played.  
  - All words and any chain words formed will be checked against the built-in dictionary, which is accurate to the **official Scrabble dictionary**.  
  - If any word is **invalid**, the player who placed it **loses their turn**.  
  - If all words are **valid**, the player who challenged **loses their turn**.  

## Winning Conditions  
- The first player to reach the **chosen** number of points wins.  
- Points are assessed after each turn submission. 

## Extra Features  
- **UI is scrollable and draggable** to navigate the board.  
- **Window is not resizable**, but you can adjust the static size in `config.py`.  
  - **Warning**: Tile images may become blurry at very small sizes, and tiles may not scale properly in windows larger than **2600x2600**.  

## Requirements  
- This game runs on **Python 3.9**.
