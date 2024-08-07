import pygame
import multiprocessing

def update_display(queue):
    pygame.init()
    print(pygame.font.get_fonts())
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Set the display mode to fullscreen
    screen = pygame.display.set_mode((1080, 720), pygame.RESIZABLE)
    pygame.display.set_caption('Buzzers')
    big_font = pygame.font.Font("data/fonts/SuperMario256.ttf", 104)
    small_font = pygame.font.Font("data/fonts/SuperMario256.ttf", 54)
    team_text = ""
    time_text = ""
    team_color = (255, 255, 255)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        try:
            message = queue.get_nowait()
            if isinstance(message, tuple):
                team_text, team_color = message
                # time_text = ""  # Reset the time text when a new team buzzes in
            else:
                time_text = message
        except multiprocessing.queues.Empty:
            pass

        screen.fill((0, 0, 0))
        if team_text:
            screen.fill(tuple(ti/3 for ti in team_color))
            rendered_team_text = big_font.render(team_text, True, team_color)
            team_text_rect = rendered_team_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(rendered_team_text, team_text_rect)
        if time_text and team_text:
            rendered_time_text = small_font.render(time_text, True, (255, 255, 255))
            time_text_rect = rendered_time_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))
            screen.blit(rendered_time_text, time_text_rect)
        pygame.display.flip()
        pygame.time.wait(100)

if __name__ == '__main__':
    queue = multiprocessing.Queue()
    update_display(queue)
