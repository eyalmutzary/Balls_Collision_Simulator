from globals import G_FORCE, FPS, SCREEN_WIDTH, SCREEN_HEIGHT
import numpy as np
import math

def calc_drag_force (velocity, radius):
    rho = 1.2  # Air density in kg/m³ (typical value for air at room temperature and sea level)
    Cd = 0.47  # Drag coefficient for a spherical object (typical value, can vary)
    A = 0.5  # Cross-sectional area of the ball facing the fluid flow (m²)
    drag_force = 0.5 * rho * velocity**2 * A * Cd
    return drag_force


class Ball:
    def __init__(self, x, y, radius, color, x_velocity=0, y_velocity=0, enable_gravity=True):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.enable_gravity = enable_gravity

    def set_x_position(self, x):
        self.x = x
    def set_y_position(self, y):
        self.y = y
    def set_x_velocity(self, x_velocity):
        self.x_velocity = x_velocity
    def set_y_velocity(self, y_velocity):
        self.y_velocity = y_velocity
    def set_existing(self, is_existing):
        self.is_existing = is_existing
    def update_position(self):
        self.y += self.y_velocity * 2
        self.x += self.x_velocity * 2

    def update_velocity(self):
        y_drag = calc_drag_force(self.y_velocity, self.radius) * np.sign(self.y_velocity)

        if self.enable_gravity:
            x_drag = max(calc_drag_force(self.x_velocity, self.radius), 0.3) * np.sign(self.x_velocity)
            updated_y_velocity = self.y_velocity + (G_FORCE / FPS) - (y_drag / FPS)
        else:
            x_drag = calc_drag_force(self.x_velocity, self.radius) * np.sign(self.x_velocity)
            updated_y_velocity = self.y_velocity - (y_drag / FPS)

        updated_x_velocity = self.x_velocity - (x_drag / FPS)

        self.x_velocity = updated_x_velocity
        self.y_velocity = updated_y_velocity


    def check_collision_with_borders(self):
        if self.x + self.radius >= SCREEN_WIDTH or self.x <= 0:
            if (self.x + self.radius >= SCREEN_WIDTH):
                self.x = SCREEN_WIDTH - self.radius
            else:
                self.x = 0
            self.x_velocity = -self.x_velocity
        elif (self.y + self.radius >= SCREEN_HEIGHT or self.y <= 0):
            if (self.y + self.radius >= SCREEN_HEIGHT):
                self.y = SCREEN_HEIGHT - self.radius
            else:
                self.y = 0
            self.y_velocity = -self.y_velocity + np.sign(self.y_velocity)*(G_FORCE / FPS)

