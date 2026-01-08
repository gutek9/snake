# Architecture

```mermaid
flowchart TD
    Entry[CLI Entry Point\npython -m snake] --> Run[run()]
    Run -->|TTY check| Wrapper[curses.wrapper]
    Wrapper --> MainLoop[_main_loop]

    MainLoop --> Menu[Menu Loop\nmenu_loop]
    MainLoop --> Scores[High Scores\nrender_scores]
    MainLoop --> GameLoop[_game_loop]

    GameLoop --> Input[Input Handling\nnext_direction]
    GameLoop --> State[Game State\nmake_initial_snake + place_food]
    GameLoop --> Timing[Timing & Speed\nmonotonic + sleep]
    GameLoop --> Render[Rendering\nrender + render_center_message]
    GameLoop --> Background[Starfield\ninit/update/render]

    Render --> Border[draw_border]
    Render --> Screen[curses stdscr\naddch/addstr/refresh]
    Render --> Palette[Style\ninit_style + sprites]
    Scores --> Storage[Persistence\nload/save/record]
    Scores --> Prompt[Initials\nprompt_initials]

    Background --> Stars[background.py]
    Input --> Keys[input.py]
    State --> Food[place_food]
    State --> Collision[Collision Rules\nWalls + Self]
```

## Notes
- The game loop owns state updates, collision checks, and speed control.
- Rendering uses safe helpers to avoid curses errors on edge cases.
