# Architecture

```mermaid
flowchart TD
    Entry[CLI Entry Point\npython -m snake] --> Run[run()]
    Run -->|TTY check| Wrapper[curses.wrapper]
    Wrapper --> MainLoop[terminal.game:_main_loop]

    AndroidEntry[Android Entry Point\nsrc/main.py] --> App[SnakeApp (Kivy)]
    App --> Screens[android.app\nMenu/Game/Scores]

    MainLoop --> Menu[terminal.menu]
    MainLoop --> Scores[terminal.scores]
    MainLoop --> GameLoop[terminal.game:_game_loop]

    GameLoop --> Input[terminal.input]
    GameLoop --> State[core.new_game + step]
    GameLoop --> Timing[Timing & Speed\nmonotonic + sleep]
    GameLoop --> Render[terminal.rendering]
    GameLoop --> Background[terminal.background]

    Screens --> AndroidGame[GameScreen tick\ncore.new_game + step]
    Screens --> AndroidScores[scores_store]

    Render --> Border[draw_border]
    Render --> Screen[curses stdscr\naddch/addstr/refresh]
    Render --> Palette[Style\ninit_style + sprites]
    Scores --> Storage[scores_store]
    Scores --> Prompt[prompt_initials]

    Background --> Stars[background.py]
    Input --> Keys[input.py]
    State --> Food[state.place_food]
    State --> Collision[Collision Rules\nWalls + Self]
```

## Notes
- The game loop owns state updates, collision checks, and speed control.
- Rendering uses safe helpers to avoid curses errors on edge cases.
