import curses
import time
import random

PADDLE_WIDTH = 25
BALL_SPEED = 0.1  # Lower is faster; raise for slower ball
BRICK_ROWS = 5
BRICK_COLS = 12

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(0)
    sh, sw = stdscr.getmaxyx()

    # Paddle setup
    paddle_x = sw // 2 - PADDLE_WIDTH // 2
    paddle_y = sh - 2

    # Ball setup
    ball_x = sw // 2
    ball_y = paddle_y - 1
    ball_dx = random.choice([-1, 1])
    ball_dy = -1

    # Bricks setup
    bricks = set()
    brick_width = sw // BRICK_COLS
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            bx = col * brick_width
            by = 2 + row
            bricks.add((by, bx))

    score = 0
    playing = True

    while playing:
        stdscr.clear()
        # Draw bricks
        for by, bx in bricks:
            for i in range(brick_width-1):
                if bx+i < sw-1:
                    stdscr.addch(by, bx+i, "#")
        # Draw paddle
        for i in range(PADDLE_WIDTH):
            if 0 <= paddle_x + i < sw-1:
                stdscr.addch(paddle_y, paddle_x + i, "=")
        # Draw ball
        if 0 < ball_y < sh and 0 < ball_x < sw-1:
            stdscr.addch(ball_y, ball_x, "O")
        # Draw score
        stdscr.addstr(0, 2, f"Score: {score}")

        stdscr.refresh()
        time.sleep(BALL_SPEED)

        # Input
        key = stdscr.getch()
        if key == curses.KEY_LEFT and paddle_x > 0:
            paddle_x -= 2
        elif key == curses.KEY_RIGHT and paddle_x + PADDLE_WIDTH < sw-1:
            paddle_x += 2
        elif key == ord('q'):
            break

        # Move ball
        ball_x += ball_dx
        ball_y += ball_dy

        # Ball collision: left/right wall
        if ball_x <= 0 or ball_x >= sw-2:
            ball_dx *= -1
            ball_x += ball_dx
        # Ball collision: top wall
        if ball_y <= 1:
            ball_dy *= -1
            ball_y += ball_dy

        # Ball collision: paddle
        if ball_y == paddle_y - 1 and paddle_x <= ball_x < paddle_x + PADDLE_WIDTH:
            ball_dy *= -1
            # Ball direction changes depending on where it hit the paddle
            if ball_x < paddle_x + PADDLE_WIDTH // 2:
                ball_dx = -1
            else:
                ball_dx = 1

        # Ball collision: bricks
        hit_brick = None
        for by, bx in bricks:
            if by == ball_y and bx <= ball_x < bx + brick_width-1:
                hit_brick = (by, bx)
                break
        if hit_brick:
            bricks.remove(hit_brick)
            score += 10
            ball_dy *= -1

        # Ball falls below paddle (lose)
        if ball_y > paddle_y:
            stdscr.addstr(sh//2, sw//2 - 5, "GAME OVER!")
            stdscr.refresh()
            time.sleep(2)
            playing = False

        # Win condition
        if not bricks:
            stdscr.addstr(sh//2, sw//2 - 4, "YOU WIN!")
            stdscr.refresh()
            time.sleep(2)
            playing = False

curses.wrapper(main)