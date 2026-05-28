import pygame
import random
import sys
pygame.init()

width, height = 1500, 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Uno")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 60)

small_font = pygame.font.SysFont(None, 28)

game_state = "menu"
draw_count = 4
max_draws = 3
start_time = 0
game_time = 60

play_button = pygame.Rect(350, 250, 300, 80)
quit_button = pygame.Rect(350, 370, 300, 80)

draw_rect = pygame.Rect(300, 250, 80, 120)

card_rects = []
player = None
bot = None
deck = None
top_card = None

colors = ["Red", "Green", "Blue", "Yellow"]
values = [str(i) for i in range(0, 10)] + ["Skip", "Reverse", "+2", "Wild", "+4"]

color_map = {
            "Red": (255, 0, 0),
            "Green": (0, 200, 0),
            "Blue": (0, 0, 255),
            "Yellow": (255, 180, 40)
}


class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value
    def match(self, other):
        return (
            self.color == other.color or
            self.value == other.value
        )

class Deck:
    def __init__(self):
        self.cards = []
        for color in colors:
            for value in values:

                self.cards.append(
                    Card(color, value)
                )
                self.cards.append(
                    Card(color, value)
                )
        random.shuffle(self.cards)
    def draw(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        return None




class Player:

    def __init__(self, name):

        self.name = name
        self.hand = []
    def draw_card(self, deck):
        card = deck.draw()
        if card:
            self.hand.append(card)

def draw_menu():
    screen.fill((30, 130, 30))
    title = font.render(
        "UNO",
        True,
        (255, 255, 255)
    )
    title_rect = title.get_rect(
        center=(500, 120)
    )
    screen.blit(title, title_rect)

    pygame.draw.rect(
        screen,
        (255, 0, 0),
        play_button,
        border_radius=20
    )
    play_text = font.render(
        "PLAY",
        True,
        (255, 255, 255)
    )
    play_rect = play_text.get_rect(
        center=play_button.center
    )
    screen.blit(play_text, play_rect)
    
    pygame.draw.rect(
        screen,
        (255, 0, 0),
        quit_button,
        border_radius=20
    )
    pygame.draw.rect(
        screen,
        (255, 0, 0),
        quit_button,
        border_radius=20
    )
    quit_text = font.render(
        "QUIT",
        True,
        (255, 255, 255)
    )
    quit_rect = quit_text.get_rect(
        center=quit_button.center
    )
    screen.blit(quit_text, quit_rect)

def draw_game():
    global card_rects
    screen.fill((0, 100, 0))
    card_rects = []
    seconds_passed = (
        pygame.time.get_ticks() - start_time
    ) // 1000

    time_left = max(
        0,
        game_time - seconds_passed
    )
    timer_text = font.render(
        str(time_left),
        True,
        (255, 255, 255)
    )
    screen.blit(timer_text, (850, 20))
    pygame.draw.rect(
        screen,
        (50, 50, 50),
        draw_rect,
        border_radius=20
    )
    
    pygame.draw.rect(
        screen,
        (50, 50, 50),
        draw_rect,
        border_radius=20
    )

    pygame.draw.rect(
        screen,
        (255, 255, 255),
        draw_rect,
        3,
        border_radius=20
    )
    draw_text = small_font.render(
        "DRAW",
        True,
        (255, 255, 255)
    )
    draw_text_rect = draw_text.get_rect(
        center=draw_rect.center
    )
    screen.blit(draw_text, draw_text_rect)
    top_rect = pygame.Rect(460, 250, 80, 120)

    pygame.draw.rect(
        screen,
        color_map[top_card.color],
        top_rect,
        border_radius=20
    )

    pygame.draw.rect(
        screen,
        (255, 255, 255),
        top_rect,
        3,
        border_radius=20
    )

    top_text = small_font.render(
        str(top_card.value),
        True,
        (255, 255, 255)
    )

    top_text_rect = top_text.get_rect(
        center=top_rect.center
    )

    screen.blit(top_text, top_text_rect)
    color_text = small_font.render(
        top_card.color,
        True,
        color_map[top_card.color]
    )
    color_rect = color_text.get_rect(
        center=(500, 420)
    )
    screen.blit(color_text, color_rect)
    color_text = small_font.render(
        top_card.color,
        True,
        color_map[top_card.color]
    )
    color_rect = color_text.get_rect(
        center=(500, 420)
    )
    screen.blit(color_text, color_rect)


    card_rects.clear()
    for i, card in enumerate(player.hand):
        x = 80 + i * 90
        y = 600
        rect = pygame.Rect(
            x,
            y,
            80,
            120
        )
        card_rects.append(rect)

        pygame.draw.rect(
            screen,
            color_map[card.color],
            rect,
            border_radius=20
        )
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            rect,
            3,
            border_radius=20
        )
        card_text = small_font.render(
            str(card.value),
            True,
            (255, 255, 255)
        )
        text_rect = card_text.get_rect(
            center=rect.center
        )
        screen.blit(card_text, text_rect)

def draw_game_over():
    screen.fill((0, 0, 0))
    over_text = font.render(
        "TIME OVER",
        True,
        (255, 0, 0)
    )
    over_rect = over_text.get_rect(
        center=(500, 300)
    )
    screen.blit(over_text, over_rect)

    cards_left = font.render(
        f"Cards Left: {len(player.hand)}",
        True,
        (255, 255, 255)
    )
    screen.blit(cards_left, (250, 400))
#WIN SCREEN 
def draw_win():
    screen.fill((0, 0, 0))
    win_text = font.render(
        "YOU WIN!",
        True,
        (0, 255, 0)
    )
    win_rect = win_text.get_rect(
        center=(500, 350)
    )
    screen.blit(win_text, win_rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "menu":
                if play_button.collidepoint(event.pos):
                    deck = Deck()
                    player = Player("You")
                    bot = Player("Bot")
                    for i in range(7):
                        player.draw_card(deck)
                        bot.draw_card(deck)
                    top_card = deck.draw()
                    start_time = pygame.time.get_ticks()
                    game_state = "game"
                game_state = "game"
            elif quit_button.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
            elif game_state == "game":
                if draw_rect.collidepoint(event.pos):
                    if len(player.hand) < 15:
                        player.draw_card(deck)
                for i, rect in enumerate(card_rects):
                    if rect.collidepoint(event.pos):
                        selected_card = player.hand[i]
                        if selected_card.match(top_card):
                            top_card = selected_card
                            player.hand.pop(i)
                            if len(player.hand) == 0:
                                game_state = "win"
    if game_state == "game":
        seconds_passed = (
            pygame.time.get_ticks() - start_time
        ) // 1000
        if seconds_passed >= game_time:
            game_state = "game_over"
    if game_state == "menu":
        draw_menu()
    elif game_state == "game":
        if player and top_card:
            draw_game()
    elif game_state == "game_over":
        draw_game_over()
    elif game_state == "win":
        draw_win()
    pygame.display.flip()
    clock.tick(60)
