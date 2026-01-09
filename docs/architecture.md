# Architecture

```mermaid
flowchart TD
    AndroidEntry[Android Entry Point\nsrc/main.py] --> App[SnakeApp (Kivy)]
    App --> Screens[android.app\nMenu/Game/Scores]

    Screens --> AndroidGame[GameScreen tick\ncore.new_game + step]
    Screens --> AndroidScores[scores_store]
    State --> Food[state.place_food]
    State --> Collision[Collision Rules\nWalls + Self]
```

## Notes
- The game loop owns state updates, collision checks, and speed control.
- Kivy screens provide UI, input, and audio for Android.
