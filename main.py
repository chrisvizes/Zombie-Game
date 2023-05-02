import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up screen dimensions
screen_width = 1400
screen_height = 900

# Set up the game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Circle Game")


class Circle:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

    def update_position(self, dx, dy):
        # Update position of the circle
        new_x = self.x + dx
        new_y = self.y + dy

        # Check boundaries of the screen
        if self.radius <= new_x <= screen_width - self.radius:
            self.x = new_x
        if self.radius <= new_y <= screen_height - self.radius:
            self.y = new_y


class Zombie:
    def __init__(self, x, y, radius, color, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = speed

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

    def update(self, player_x, player_y):
        dx = player_x - self.x
        dy = player_y - self.y
        distance = (dx**2 + dy**2) ** 0.5

        follow_range = 200

        if distance <= follow_range:
            if distance != 0:
                self.x += self.speed * dx / distance
                self.y += self.speed * dy / distance

            self.color = (255, 0, 0)  # Change color to red when following the player
        else:
            self.color = (
                0,
                255,
                0,
            )  # Change color back to green when not following the player


class Child:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)


class Exit:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))


def check_collision(circle1, circle2):
    dx = circle1.x - circle2.x
    dy = circle1.y - circle2.y
    distance = (dx**2 + dy**2) ** 0.5
    return distance <= (circle1.radius + circle2.radius)


def display_score(screen, font, score):
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))  # Adjust the position as needed


def reset_game():
    global player, zombies, children, exit_sprite, score, game_over

    player = Circle(screen_width // 2, screen_height // 2, 10, (255, 255, 255))

    zombies = []
    min_distance_to_player = 400

    while len(zombies) < 20:
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)
        distance_to_player = ((x - player.x) ** 2 + (y - player.y) ** 2) ** 0.5

        if distance_to_player >= min_distance_to_player:
            zombies.append(Zombie(x, y, 10, (0, 255, 0), 1))

    children = []
    for _ in range(4):
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)
        children.append(Child(x, y, 10, (0, 0, 255)))

    min_distance_from_player = 400
    while True:
        exit_x = random.randint(0, screen_width)
        exit_y = random.randint(0, screen_height)
        distance_to_player = (
            (exit_x - player.x) ** 2 + (exit_y - player.y) ** 2
        ) ** 0.5
        if distance_to_player >= min_distance_from_player:
            break

    exit_sprite = Exit(exit_x, exit_y, 40, 40, (255, 0, 0))

    score = 0
    game_over = False


def check_exit_collision(circle, exit):
    dx = circle.x - (exit.x + exit.width / 2)
    dy = circle.y - (exit.y + exit.height / 2)
    distance = (dx**2 + dy**2) ** 0.5
    return distance <= (circle.radius + max(exit.width, exit.height) / 2)


def update_fog_of_war(surface, player_x, player_y, radius):
    gradient_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    gradient = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)

    for i in range(radius * 2):
        alpha = 255 - int(255 * i / (radius * 2))
        pygame.draw.line(gradient, (0, 0, 0, alpha), (0, i), (radius * 2, i))

    gradient_surf.blit(gradient, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    surface.blit(
        gradient_surf,
        (player_x - radius, player_y - radius),
        special_flags=pygame.BLEND_RGBA_MIN,
    )

    pygame.draw.circle(surface, (0, 0, 0, 255), (player_x, player_y), radius)
    surface.set_colorkey((0, 0, 0, 255))


def start_screen():
    start_font = pygame.font.Font(None, 48)
    start_text = start_font.render("Press ENTER to start", True, (255, 255, 255))
    start_button = start_text.get_rect(center=(screen_width // 2, screen_height // 2))

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(start_text, start_button)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
                if event.key == pygame.K_ESCAPE:
                    running = False
                    return False

        pygame.display.flip()
        pygame.time.Clock().tick(60)


reset_game()


def main():
    if not start_screen():
        return

    player = Circle(screen_width // 2, screen_height // 2, 10, (255, 255, 255))

    # Initialize 20 zombies with random positions
    zombies = []
    for _ in range(20):
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)
        zombies.append(Zombie(x, y, 10, (0, 255, 0), 1))

    # Initialize 4 children with random positions
    children = []
    for _ in range(4):
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)
        children.append(Child(x, y, 10, (0, 0, 255)))

    fog_of_war_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    fog_of_war_radius = 200

    # Initialize the exit sprite with a random position far from the player's start position
    min_distance_from_player = 400
    while True:
        exit_x = random.randint(0, screen_width)
        exit_y = random.randint(0, screen_height)
        distance_to_player = (
            (exit_x - player.x) ** 2 + (exit_y - player.y) ** 2
        ) ** 0.5
        if distance_to_player >= min_distance_from_player:
            break

    exit_sprite = Exit(exit_x, exit_y, 40, 40, (255, 0, 0))

    score = 0
    game_over = False
    running = True

    pygame.font.init()
    font = pygame.font.Font(
        None, 36
    )  # You can replace None with a specific font file if desired

    while running and not game_over:
        # Main game loop
        if check_exit_collision(player, exit_sprite):
            game_over = True

        for zombie in zombies:
            if check_collision(player, zombie):
                game_over = True
                break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_over:
                    reset_game()
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Update game state
        for zombie in zombies:
            zombie.update(player.x, player.y)

        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0

        if keys[pygame.K_LEFT]:
            dx = -5
        if keys[pygame.K_RIGHT]:
            dx = 5
        if keys[pygame.K_UP]:
            dy = -5
        if keys[pygame.K_DOWN]:
            dy = 5

        player.update_position(dx, dy)

        for i, child in enumerate(children):
            if check_collision(player, child):
                score += 1
                del children[i]
                break

        # Draw game objects
        screen.fill((0, 0, 0))
        update_fog_of_war(fog_of_war_surface, player.x, player.y, fog_of_war_radius)

        # Draw only the visible game objects
        for zombie in zombies:
            if (
                (zombie.x - player.x) ** 2 + (zombie.y - player.y) ** 2
            ) ** 0.5 < fog_of_war_radius:
                zombie.draw(screen)
        player.draw(screen)
        for child in children:
            if (
                (child.x - player.x) ** 2 + (child.y - player.y) ** 2
            ) ** 0.5 < fog_of_war_radius:
                child.draw(screen)

        if (
            (exit_sprite.x - player.x) ** 2 + (exit_sprite.y - player.y) ** 2
        ) ** 0.5 < fog_of_war_radius:
            exit_sprite.draw(screen)

        display_score(screen, font, score)

        screen.blit(fog_of_war_surface, (0, 0))

        # Update display
        pygame.display.flip()
        pygame.time.Clock().tick(60)  # Limit FPS to 60
    if game_over:
        print(f"Game Over! Final Score: {score}")


if __name__ == "__main__":
    main()
