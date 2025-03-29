import pygame as pg


class Pipe:
    GAP = 140

    def __init__(self, pos: list | tuple, height: int, flip: bool):

        pipe_head_length = 40

        pipe_head = pg.image.load("data/images/pipe_head.png").convert_alpha()
        pipe_body = pg.image.load("data/images/pipe_body.png").convert_alpha()
        pipe_head = pg.transform.scale(pipe_head, [110, pipe_head_length])
        pipe_body = pg.transform.scale(pipe_body, [100, max(height - pipe_head_length, 0)])

        self.image = pg.Surface([110, height])
        self.image.fill("white")

        self.image.blit(pipe_body, [5, 0])
        self.image.blit(pipe_head, [0, height-pipe_head_length])
        self.image = pg.transform.scale(self.image, [80, height])

        self.image.set_colorkey("white")
        self.pos = list(pos)
        self.flip = flip

    def rect(self) -> pg.Rect:
        return self.image.get_rect(topleft=self.pos)

    def update(self) -> bool:
        if self.rect().right <= 0:
            return True
        else:
            self.pos[0] -= 4
            return False

    def render(self, surf) -> None:
        surf.blit(pg.transform.flip(self.image, False, self.flip), self.rect())
        # pg.draw.rect(surf, "black", self.rect(), 2)
