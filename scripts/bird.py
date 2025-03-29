import pygame as pg

class Bird:
    def __init__(self, game):
        self.game = game
        self.image = pg.image.load("data/images/bird.png").convert_alpha()
        self.image = pg.transform.scale(self.image, [55, 35])
        self.pos: list[int | float] = [100, 250]
        self.velocity: list[int | float] = [0, 0]
        # self.dead = False
        self.jumping = 0

    def rect(self) -> pg.Rect:
        return self.image.get_rect(topleft=self.pos)

    def jump(self) -> None:
        self.jumping += 1
        # self.velocity[1] = -6

    def home_screen_reset(self):
        self.image = pg.transform.scale(self.image, [110, 70])
        self.velocity = [0, 0]
        self.pos = [self.game.SCREEN_WIDTH / 2 - 55, self.game.SCREEN_HEIGHT / 2 - 35 - 10]
        self.render(self.game.screen)

    def update(self) -> None:
        # Score and collision check.
        for pipe_group in self.game.pipes:
            for pipe in pipe_group:
                if self.rect().colliderect(pipe.rect()):
                    self.game.playing = False
                    return None
                elif self.rect().left > pipe.rect().left and self.rect().right < pipe.rect().right:
                    self.game.score += 1/12

        if self.rect().centery > self.game.SCREEN_HEIGHT-40 or self.rect().centery < 0:
            self.game.playing = False
            return None

        # Jumping check
        if self.jumping:
            self.velocity[1] = max(self.velocity[1] - self.jumping, -5)
            if self.velocity[1] == -5:
                self.jumping = 0
        else:
            self.velocity[1] = min(self.velocity[1] + 0.3, 10)

        self.pos[0] += self.velocity[0]  # Always 0
        self.pos[1] += self.velocity[1]

    def render(self, surf: pg.Surface) -> None:
        image = pg.transform.rotate(self.image, -5 * self.velocity[1])
        surf.blit(image, [self.pos[0], self.pos[1] - 3])
        pg.draw.rect(surf, "black", self.rect(), 2)
