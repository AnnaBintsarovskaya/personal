import pygame
import sys
import random

pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

# Colors
BG = (0, 0, 0)
SQUARE_COLOR = (255, 255, 255)

# Square settings
x, y = 150, 100
size = 250
thickness = 6

# Hole settings (bottom side)
hole_start = 80
hole_width = 90

# Ball settings
BALL_RADIUS = 10



def create_ball():
    vx_options = [3, 4, 5, 7]
    vy_options = [3, 4, 5, 7]

    vx = random.choice(vx_options)

    # Remove vx from vy options to guarantee they are not equal
    vy_choices = [v for v in vy_options if v != vx]
    vy = random.choice(vy_choices)

    return {
        "x": x + size // 2,
        "y": y + size // 2,
        "vx": vx,
        "vy": vy,
        "radius": BALL_RADIUS,
        "color": (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
    }


# Start with one ball
balls = [create_ball()]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BG)

    # Draw square outline
    pygame.draw.line(screen, SQUARE_COLOR, (x, y), (x + size, y), thickness)  # top
    pygame.draw.line(screen, SQUARE_COLOR, (x, y), (x, y + size), thickness)  # left
    pygame.draw.line(screen, SQUARE_COLOR, (x + size, y), (x + size, y + size), thickness)  # right

    # Bottom with hole
    pygame.draw.line(
        screen,
        SQUARE_COLOR,
        (x, y + size),
        (x + hole_start, y + size),
        thickness
    )
    pygame.draw.line(
        screen,
        SQUARE_COLOR,
        (x + hole_start + hole_width, y + size),
        (x + size, y + size),
        thickness
    )

    hole_left = x + hole_start
    hole_right = hole_left + hole_width

    new_balls = []

    for ball in balls[:]:
        # Move ball
        ball["x"] += ball["vx"]
        ball["y"] += ball["vy"]

        r = ball["radius"]

        # Left wall
        if ball["x"] - r <= x:
            ball["x"] = x + r
            ball["vx"] *= -1

        # Right wall
        if ball["x"] + r >= x + size:
            ball["x"] = x + size - r
            ball["vx"] *= -1

        # Top wall
        if ball["y"] - r <= y:
            ball["y"] = y + r
            ball["vy"] *= -1

        # Bottom wall (with hole)
        if ball["y"] + r >= y + size:
            if hole_left <= ball["x"] <= hole_right:
                # Ball escaped → spawn two new balls
                balls.remove(ball)
                new_balls.append(create_ball())
                new_balls.append(create_ball())
                continue
            else:
                ball["y"] = y + size - r
                ball["vy"] *= -1

    balls.extend(new_balls)

    # Ball-ball collision
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            b1 = balls[i]
            b2 = balls[j]

            dx = b2["x"] - b1["x"]
            dy = b2["y"] - b1["y"]
            distance = (dx ** 2 + dy ** 2) ** 0.5
            min_dist = b1["radius"] + b2["radius"]

            if distance < min_dist:
                # Simple elastic collision for same mass
                # Swap velocities
                b1["vx"], b2["vx"] = b2["vx"], b1["vx"]
                b1["vy"], b2["vy"] = b2["vy"], b1["vy"]

                # Push balls apart so they are no longer overlapping
                overlap = min_dist - distance
                if distance != 0:
                    b1["x"] -= (dx / distance) * overlap / 2
                    b1["y"] -= (dy / distance) * overlap / 2
                    b2["x"] += (dx / distance) * overlap / 2
                    b2["y"] += (dy / distance) * overlap / 2

    # Draw balls
    for ball in balls:
        pygame.draw.circle(
            screen,
            ball["color"],
            (int(ball["x"]), int(ball["y"])),
            ball["radius"]
        )

    pygame.display.flip()
    clock.tick(60)
