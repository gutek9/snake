# Architecture

```mermaid
flowchart TD
    Entry[CLI Entry Point\npython -m snake] --> Run[run()]
    Run -->|TTY check| Wrapper[curses.wrapper]
    Wrapper --> GameLoop[_game_loop]

    GameLoop --> Input[Input Handling\n_next_direction]
    GameLoop --> State[Game State\nSnake, Food, Score]
    GameLoop --> Timing[Timing & Speed\nmonotonic + sleep]
    GameLoop --> Render[_render]

    Render --> Border[_draw_border]
    Render --> Screen[curses stdscr\naddch/addstr/refresh]

    State --> Food[_place_food]
    State --> Collision[Collision Rules\nWalls + Self]
```

## Notes
- The game loop owns state updates, collision checks, and speed control.
- Rendering uses safe helpers to avoid curses errors on edge cases.
