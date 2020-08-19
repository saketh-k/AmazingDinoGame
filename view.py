import pygame
import model
import time


# Set aspect ratio
# actually resize when window resizes
#

pygame.init()


def main():
    dino = pygame.image.load('DINO.png')

    initial_width = 800
    initial_height = 600

    is_running = True

    gameDisplay = pygame.display.set_mode([initial_width, initial_height])
    pygame.display.set_caption('I AM A SICK PROGRAMMER')
    gameModel = model.GameModel()
    gameModel.makeNewCactus()

    def draw_text(text, center_x, center_y, gameDisplay, font_size):
        font = pygame.font.SysFont("Comic Sans MS", font_size)
        text = font.render(text, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (center_x, center_y)
        gameDisplay.blit(text, text_rect)

    while is_running:
        gameDisplay.fill((240, 178, 255))
        if not gameModel.game_over:
            gameModel.doTick()
        for cactus in gameModel.cacti:
            gameDisplay.blit(cactus.image, cactus.rect.topleft)
        for ptero in gameModel.ptero:
            gameDisplay.blit(ptero.image, ptero.rect.topleft)
        gameDisplay.blit(gameModel.dino.image, gameModel.dino.rect.topleft)
        time.sleep(0.015)
        draw_text("Score: " + str(gameModel.dino_score), 700, 20, gameDisplay, 25)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                gameModel.dino.accel = 2
                gameModel.dino.jump(-21)

            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                gameModel.dino.accel = 1

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                gameModel.dino.start_squat()

            elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                gameModel.dino.stop_squat()

            elif event.type == pygame.QUIT:
                is_running = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and gameModel.game_over:
                is_running = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and gameModel.game_over:
                main()

        if gameModel.game_over:
            draw_text("Game Over, Loser", 400, 300, gameDisplay, 32)

        pygame.display.flip()
    pygame.quit()


main()

