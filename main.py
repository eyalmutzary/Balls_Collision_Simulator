import pygame, sys
from globals import SCREEN_WIDTH, SCREEN_HEIGHT, BALL_SIZE, FPS, AMOUNT_OF_BALLS, MOUSE_BALL_SIZE
import Ball
import numpy as np
import math
from typing import Dict, Tuple, List


def generate_random_color():
	return np.random.randint(50, 255), np.random.randint(50, 255), np.random.randint(50, 255)

def handle_overlapping_balls(ball1: Ball, ball2: Ball):
	distance = np.sqrt((ball1.x - ball2.x) ** 2 + (ball1.y - ball2.y) ** 2)
	intersection_length = ball1.radius/2 + ball2.radius/2 - distance
	height_diff = ball1.y - ball2.y
	width_diff = ball1.x - ball2.x
	if width_diff == 0:
		degree = math.pi / 2
	else:
		degree = np.arctan(height_diff / width_diff)

	move_x = abs(np.cos(degree) * intersection_length)
	move_y = abs(np.sin(degree) * intersection_length)

	if ball1.x > ball2.x:
		ball1.x += move_x / 2
		ball2.x -= move_x / 2
	else:
		ball1.x -= move_x / 2
		ball2.x += move_x / 2

	if ball1.y > ball2.y:
		ball1.y += move_y / 2
		ball2.y -= move_y / 2
	else:
		ball1.y -= move_y / 2
		ball2.y += move_y / 2

	ball1.check_collision_with_borders()
	ball2.check_collision_with_borders()


def handle_ball_collision(ball1: Ball, ball2: Ball):
	dx = ball2.x - ball1.x
	dy = ball2.y - ball1.y
	distance = math.sqrt(dx ** 2 + dy ** 2)

	# Calculate the normal vector of the collision
	nx = dx / distance
	ny = dy / distance

	# Calculate the relative velocity along the normal vector
	relative_velocity = ((ball2.x_velocity - ball1.x_velocity) * nx + (ball2.y_velocity - ball1.y_velocity) * ny)


	# Update the velocities of the balls based on the collision
	ball1.x_velocity += relative_velocity * nx
	ball1.y_velocity += relative_velocity * ny
	ball2.x_velocity -= relative_velocity * nx
	ball2.y_velocity -= relative_velocity * ny


def check_ball_collision(ball1: Ball, ball2: Ball):
	distance = np.sqrt((ball1.x - ball2.x)**2 + (ball1.y - ball2.y)**2)
	if distance < ball1.radius/2 + ball2.radius/2:
		handle_overlapping_balls(ball1, ball2)
		handle_ball_collision(ball1, ball2)

def ball_animation(ball: Ball, game_ball: pygame.Rect):
	ball.update_position()
	ball.check_collision_with_borders()
	ball.update_velocity()
	game_ball.x = ball.x
	game_ball.y = ball.y

# def update_mouse_ball_velocity(mouse_ball: Ball, mouse_pos: Tuple[int, int]):
# 	x_diff = mouse_pos[0] - mouse_ball.x - BALL_SIZE//2
# 	y_diff = mouse_pos[1] - mouse_ball.y - BALL_SIZE//2
# 	x_velocity = (mouse_ball.x_velocity + (x_diff / FPS)) / 2
# 	y_velocity = (mouse_ball.y_velocity + (y_diff / FPS)) / 2
# 	mouse_ball.set_x_velocity(x_velocity)
# 	mouse_ball.set_y_velocity(y_velocity)


def get_grid_split(balls):
	"""
	:param balls: list of balls
	:return: dictionary of cells with the balls in them
	"""
	grid: Dict[Tuple[int, int], List[int]] = {}
	balls_cells: Dict[int, Tuple[int, int]] = {}
	for i in range(len(balls)):
		cell = (int(balls[i].x // BALL_SIZE), int(balls[i].y // BALL_SIZE))
		if not grid.get(cell):
			grid[cell] = []
		grid[cell].append(i)
		balls_cells[i] = cell
	return grid, balls_cells


def check_ball_collision_with_grid(ball_index: int,
								   	balls: list,
								   	grid: Dict[Tuple[int, int], List[int]],
								   	balls_cells: Dict[int, Tuple[int, int]],
									ball_counter: int
								):
	ball_cell = balls_cells[ball_index]

	for i in range(-1, 2):
		for j in range(-1, 2):
			if (indexes := grid.get((ball_cell[0] + i, ball_cell[1] + j))) is not None:
				for index in indexes:
					if index == ball_index or index > ball_counter:
						continue
					check_ball_collision(balls[ball_index], balls[index])





def init_game():
	# General setup
	pygame.init()
	clock = pygame.time.Clock()

	# Main Window
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption('Physics Engine')

	# Colors
	bg_color = pygame.Color('grey12')

	X_CENTER = SCREEN_WIDTH / 2 - (BALL_SIZE / 2)
	Y_CENTER = SCREEN_HEIGHT / 2 - (BALL_SIZE / 2)

	balls = []
	game_balls = []
	for i in range(AMOUNT_OF_BALLS):
		balls.append(
			Ball.Ball(x=20, y=20, radius=BALL_SIZE, color=generate_random_color(), x_velocity=10, y_velocity=0, enable_gravity=True))
		game_balls.append(pygame.Rect(balls[i].x, balls[i].y, balls[i].radius, balls[i].radius))

	# # Mouse ball
	# mouse_ball_position_x, mouse_ball_position_y = pygame.mouse.get_pos()[0] - MOUSE_BALL_SIZE // 2, \
	# 											   pygame.mouse.get_pos()[1] - MOUSE_BALL_SIZE // 2
	# balls.append(Ball.Ball(x=mouse_ball_position_x, y=mouse_ball_position_y, radius=MOUSE_BALL_SIZE,
	# 					   color=(255,255,255), x_velocity=2, y_velocity=2, enable_gravity=False))
	# game_balls.append(pygame.Rect(mouse_ball_position_x, mouse_ball_position_y, MOUSE_BALL_SIZE, MOUSE_BALL_SIZE))

	return balls, game_balls, screen, clock, bg_color


def run_game(balls, game_balls, screen, clock, bg_color):
	ball_counter = 0
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		for i in range(ball_counter):
			ball_animation(balls[i], game_balls[i])

		# # set mouse ball position
		# update_mouse_ball_velocity(balls[-1], pygame.mouse.get_pos())
		# balls[-1].set_x_position(pygame.mouse.get_pos()[0] - MOUSE_BALL_SIZE // 2)
		# balls[-1].set_y_position(pygame.mouse.get_pos()[1] - MOUSE_BALL_SIZE // 2)
		# game_balls[-1].x = balls[-1].x
		# game_balls[-1].y = balls[-1].y


		# * Optimized version taken from: https://www.youtube.com/watch?v=eED4bSkYCB8
		# * Non optimized version
		# ---------------------------------------------
		# for _ in range(6):
		# 	for i in range(ball_counter):
		# 		for j in range(i, ball_counter):
		# 			if i != j:
		# 				check_ball_collision(balls[i], balls[j])
		# ---------------------------------------------

		# * Optimization attempt 1: sort by the x axis
		# ---------------------------------------------
		# if ball_counter < AMOUNT_OF_BALLS:
		# 	for _ in range(6):
		# 		for i in range(ball_counter):
		# 			for j in range(i, ball_counter):
		# 				if i != j:
		# 					check_ball_collision(balls[i], balls[j])
		# else:
		# 	for i in range(2):
		# 		sorted_balls_indexes = get_sorted_balls_indexes_by_x(balls)
		# 		relevant_balls = []
		# 		for i in range(ball_counter):
		# 			relevant_balls.append(balls[sorted_balls_indexes[i]])
		# 			min_x = relevant_balls[0].x
		# 			max_x = relevant_balls[-1].x
		# 			while (max_x - min_x) > BALL_SIZE and len(relevant_balls) > 0:
		# 				relevant_balls.pop(0)
		# 				min_x = relevant_balls[0].x
		# 			for j in range(len(relevant_balls)):
		# 				for k in range(j, len(relevant_balls)):
		# 					if j != k:
		# 						check_ball_collision(relevant_balls[j], relevant_balls[k])
		# ---------------------------------------------

		# * Optimization attempt 2: split the screen into a grid
		# ---------------------------------------------
		grid, balls_cells = get_grid_split(balls)
		for _ in range(4):
			for ball_index in range(ball_counter):
				check_ball_collision_with_grid(ball_index, balls, grid, balls_cells, ball_counter)
		# ---------------------------------------------

		# Visuals
		screen.fill(bg_color)
		for i in range(ball_counter):
			pygame.draw.ellipse(screen, balls[i].color, game_balls[i])
		# # mouse ball:
		# pygame.draw.ellipse(screen, balls[-1].color, game_balls[-1])

		if ball_counter < AMOUNT_OF_BALLS:
			ball_counter += 1

		pygame.display.flip()
		clock.tick(FPS)

def main():
	balls, game_balls, screen, clock, bg_color = init_game()
	run_game(balls, game_balls, screen, clock, bg_color)


if __name__ == '__main__':
	main()