import pygame
import pyBaba
import config
import sprite_loader
import sys

game = pyBaba.Game("../../Resources/Maps/BabaIsYou.txt")
screen_size = (game.GetMap().GetWidth() * config.BLOCK_SIZE,
               game.GetMap().GetHeight() * config.BLOCK_SIZE)
screen = pygame.display.set_mode(
    (screen_size[0], screen_size[1]), pygame.DOUBLEBUF)


def draw_obj(x_pos, y_pos):
    objects = game.GetMap().At(y_pos, x_pos)

    for obj_type in objects.GetTypes():
        if pyBaba.IsTextType(obj_type):
            obj_image = sprite_loader.sprite_loader.text_images[obj_type]
        else:
            if obj_type == pyBaba.ObjectType.ICON_EMPTY:
                continue
            obj_image = sprite_loader.sprite_loader.icon_images[obj_type]
        obj_rect = obj_image.get_rect()
        obj_rect.topleft = (x_pos * config.BLOCK_SIZE,
                            y_pos * config.BLOCK_SIZE)
        screen.blit(obj_image, obj_rect)


def draw():
    for y_pos in range(game.GetMap().GetHeight()):
        for x_pos in range(game.GetMap().GetWidth()):
            draw_obj(x_pos, y_pos)


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()

    action_dic = {"Direction.UP": pyBaba.Direction.UP, "Direction.DOWN": pyBaba.Direction.DOWN,
                  "Direction:LEFT": pyBaba.Direction.LEFT, "Direction.RIGHT": pyBaba.Direction.RIGHT, "Direction.NONE": pyBaba.Direction.NONE}
    action_file = open("./action.txt", 'r')
    actions = action_file.read().splitlines()
    action_file.close()

    clock = pygame.time.Clock()

    pygame.time.set_timer(pygame.USEREVENT, 200)

    game_over = False
    time_step = 0

    while True:
        if game_over:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if time_step < len(actions):
                    game.MovePlayer(action_dic[actions[time_step]])
                    time_step += 1
                else:
                    pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        if game.GetPlayState() == pyBaba.PlayState.WON or game.GetPlayState() == pyBaba.PlayState.LOST:
            game_over = True

        screen.fill(config.COLOR_BACKGROUND)
        draw()
        pygame.display.flip()

        clock.tick(config.FPS)
