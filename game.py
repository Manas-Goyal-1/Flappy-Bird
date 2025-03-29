import sys

import pygame as pg
from random import randint
from scripts.pipe import Pipe
from scripts.bird import Bird


class Game:
	SCREEN_WIDTH = 720
	SCREEN_HEIGHT = 480
	fps = 60

	def __init__(self):
		pg.init()
		self.screen = pg.display.set_mode([self.SCREEN_WIDTH, self.SCREEN_HEIGHT])
		self.background: pg.Surface = pg.image.load("data/images/background.jpg").convert()
		self.background = pg.transform.scale(self.background, [self.SCREEN_WIDTH, self.SCREEN_HEIGHT])

		pg.display.set_caption("Flappy Bird")

		self.clock = pg.time.Clock()
		self.bird = Bird(self)

		self.pipes: list[list[Pipe]] = []
		self.generate_pipes(3)

		self.offset = [0, 0]
		self.playing = False

		self.playing_font_base = pg.font.Font(None, 40)
		self.score = 0
		self.playing_score_message = self.playing_font_base.render(f"Score: {int(self.score)}", True, "black")

		self.home_font_base = pg.font.Font(None, 60)

		try:
			with open("high_score.txt", "r") as file:
				self.high_score = int(file.read())
		except FileNotFoundError:
			self.high_score = 0
		self.press_space_message = self.home_font_base.render("Press SPACE to Start", True, "black")

		self.jump_sound = pg.mixer.Sound("audio/jump.mp3")
		self.jump_sound.set_volume(0.2)

	def generate_pipes(self, num_pipes: int = 1):
		for i in range(1, num_pipes + 1):
			# This can probably be done way better. If it is the first pipe, it will randomly place it
			# If it is some other pipe, it will try to randomly place it but if it is too close, it will move it away.
			if self.pipes:
				last_pipe_x = self.pipes[-1][0].pos[0]
				if last_pipe_x + 250 >= 720:
					pipe_pos = (last_pipe_x + randint(250, 350), 0)
				else:
					pipe_pos = (720 + randint(0, 50), 0)
			else:
				pipe_pos = (720 + randint(240 * (i - 1), 240 * i), 0)

			pipe_height = randint(60, 260)
			pipe_group = []
			for _ in range(2):
				if _ % 2:
					pipe_group.append(Pipe(pipe_pos, pipe_height, False))
				else:
					transformation_height = (self.SCREEN_HEIGHT - 40) - (pipe_height + Pipe.GAP)
					pipe_group.append(Pipe([pipe_pos[0], pipe_height + Pipe.GAP], transformation_height, True))
			self.pipes.append(pipe_group)

	def run(self):
		pg.mixer.music.load("audio/music.wav")
		pg.mixer.music.set_volume(0.1)
		pg.mixer.music.play(-1)

		# Game loop
		while True:
			# Event Handler
			for event in pg.event.get():
				if event.type == pg.QUIT:
					pg.quit()
					sys.exit()

				# Movement
				if event.type == pg.KEYDOWN:
					if event.key in [pg.K_SPACE, pg.K_w, pg.K_UP]:
						if not self.playing:
							self.__init__()
						self.playing = True
						self.bird.jump()
						self.jump_sound.play()

			# Only happens when playing is true, so when the game is active.
			if self.playing:
				self.screen.blit(self.background, self.offset)
				self.screen.blit(self.background, [self.SCREEN_WIDTH + self.offset[0], 0])

				self.offset[0] = -1 * (abs(self.offset[0] - 4) % self.SCREEN_WIDTH)

				# Updating and rendering all the pipes.
				for pipe_group in self.pipes.copy():
					for pipe in pipe_group:
						kill = pipe.update()
						pipe.render(self.screen)
						if kill:
							self.pipes.remove(pipe_group)
							self.generate_pipes(1)
							break

				# Updating and rendering the player.
				self.bird.update()
				self.bird.render(self.screen)

				self.playing_score_message = self.playing_font_base.render(f"Score: {self.score: .0f}", True, "black")
				self.screen.blit(self.playing_score_message, [300, 50])
			else:
				self.screen.blit(self.background, [0, 0])
				self.bird.home_screen_reset()

				home_score_message = self.home_font_base.render(f"Current Score: {int(self.score)}", True, "black")
				high_score_message = self.home_font_base.render(f"High Score: {self.high_score}", True, "black")

				self.screen.blit(self.press_space_message, [150, 75])
				self.screen.blit(home_score_message, [170, 300])
				self.screen.blit(high_score_message, [200, 360])

				if int(self.score) >= self.high_score:
					with open("high_score.txt", "w") as file:
						file.write(f"{int(self.score)}")

			pg.display.update()
			self.clock.tick(60)


Game().run()

# from random import randint
#
# for i in range(200):
# 	print(f'g.fillOval({randint(0, 600)}, {randint(0, 600)}, 2, 2);')

#
# s = lambda n: 2024*(n+1)/(n**2*(n+2)**2)
# print(sum([s(x) for x in range(1, 1_000_000)]))

# from random import randint
# list = ["RED", "GREEN", "BLUE", "ORANGE", "YELLOW", "PINK"]
# for i in range(6):
# 	color = list.pop(randint(0, len(list)-1))
# 	print(f"g.setColor(Color.{color});")
# 	x = 125+60*i
# 	y = int(100+abs(2.5-i)*10)
# 	print(f"g.fillOval{x, y, 50, 80};")
# 	print(f"g.drawString{color, x+13, y-5};")
#
# 	print("g.setColor(Color.BLACK);")
# 	print(f"g.drawLine{x+25, y+80, 300, 400};")
#
# 	print()

# from random import randint
# colors = ["BLACK", "BLUE", "CYAN", "LIGHT_GRAY", "PINK", "RED", "ORANGE", "WHITE"]
# for i in range(8):
# 	color = colors.pop(randint(0, len(colors)-1))
# 	print(f"g.setColor(Color.{color});")
# 	print(f"g.fillArc{150, 150, 200, 200, 45*i, 45};")
# 	print("g.setColor(Color.BLACK);")
# 	print(f"g.drawString(\"{color}\");")
# 	print()


# import math
# operation = "cos"
#
# print(eval(f"math.{operation}(45)"))


# n = int(input("Enter a number: "))
# print("EOvdedn"[n%2::2])
#

