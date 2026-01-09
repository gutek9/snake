# Architecture

```mermaid
flowchart TD
    AndroidEntry["Android Entry Point<br/>src/main.py"] --> App["SnakeApp Kivy"]
    App --> Screens["android.app<br/>Menu/Game/Scores"]

    Screens --> AndroidGame["GameScreen tick<br/>core.new_game then step"]
    Screens --> AndroidScores["scores_store"]
    AndroidGame --> State["core.GameState"]
    State --> Food["state.place_food"]
    State --> Collision["Collision Rules<br/>Walls and Self"]
```

## Notes
- The game loop owns state updates, collision checks, and speed control.
- Kivy screens provide UI, input, and audio for Android.
