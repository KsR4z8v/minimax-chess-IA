# ♟️ Chess AI with Minimax and Alpha-Beta Pruning

This project is a chess engine that uses the **Minimax algorithm** enhanced with **Alpha-Beta pruning** to make intelligent decisions. It simulates a two-player game and evaluates moves several turns ahead to select the most strategic path.

## 🧠 AI Overview

The chess AI uses the **Minimax algorithm**, a classic decision-making technique in game theory, to evaluate all possible moves. To improve efficiency, **Alpha-Beta pruning** is implemented to eliminate branches that won’t affect the final decision, significantly reducing computation time.

### ✅ Key Features

- 🔁 Turn-based chess engine with legal move generation
- ♟️ AI decision-making using **Minimax with Alpha-Beta pruning**
- 📈 Evaluation function based on material and positional advantage
- ⚡ Adjustable search depth for difficulty levels
- 🧪 Console or graphical interface integration (optional)

## 🔍 How It Works

- **Minimax** recursively simulates game states, assuming both players play optimally.
- **Alpha-Beta pruning** skips unnecessary branches to speed up the search.
- The **evaluation function** scores each position to guide decision-making.

```text
+-------------------------+
|      Current State      |
+-------------------------+
          |
          v
  [Generate Legal Moves]
          |
          v
     [Recursive Minimax]
          |
          v
  [Alpha-Beta Pruning]
          |
          v
  [Best Move Selection]
