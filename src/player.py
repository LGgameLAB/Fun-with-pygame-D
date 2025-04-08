import pygame, pymunk
from pygame import Vector2 as Vec
import src.settings as settings
import src.fx as fx
from src.sprites import Spider
from shapely.geometry import Point, Polygon
import numpy as np

class Player(pygame.sprite.Sprite):

    # movement speed and dampening rate
    speed = 50
    damp = 0.92

    def __init__(self, game):
        self.game = game
        super().__init__((game.sprites, game.screen.spritelayer))

        self.vel = Vec(1, 0)
        self.pos = Vec(100, 100)
        self.radius = 5
        # self.particles = fx.GlowParticles(game)
        # game.screen.spritelayer.add(self.particles)

        # self.pet = Spider(game)
        self.wall = Polygon([(200, 200), (220, 200), (200, 220)])

    def detect_collision(self):

        # Create a polygon (a square for this example)

        # Create a circle as a buffered point (approximated polygon)
        circle_center = Point(*self.pos)  # Center of the circle
        circle = circle_center.buffer(self.radius)  # Creates a circular polygon

        # Find intersection points
        intersection = self.wall.intersection(circle)

        # If there's a collision, compute the normal vector
        if not intersection.is_empty:
            # Get the first collision point (assuming only one for simplicity)
            collision_point = list(intersection.geoms)[0] if intersection.geom_type == 'MultiPoint' else intersection
            collision_coords = np.array(collision_point.exterior.coords[0])
            
            # Find the nearest polygon edge
            nearest_edge = None
            min_distance = float("inf")
            
            for i in range(len(self.wall.exterior.coords) - 1):
                p1 = np.array(self.wall.exterior.coords[i])
                p2 = np.array(self.wall.exterior.coords[i + 1])
                
                # Project the collision point onto the edge and compute distance
                edge_vector = p2 - p1
                point_vector = collision_coords - p1
                t = np.dot(point_vector, edge_vector) / np.dot(edge_vector, edge_vector)
                t = np.clip(t, 0, 1)  # Clamp projection to the edge
                
                nearest_point = p1 + t * edge_vector
                distance = np.linalg.norm(collision_coords - nearest_point)
                
                if distance < min_distance:
                    min_distance = distance
                    nearest_edge = nearest_point
            
            # Compute normal (collision point - nearest point on polygon)
            n = self.pos - nearest_edge
            normal_vector = Vec(*n)
            if normal_vector.length() > 0:
                normal_vector.normalize_ip()  # Normalize

            return collision_coords, normal_vector
        else:
            return False


    def move(self):
        keys = pygame.key.get_pressed()

        """
        Checks key presses and sets velocity to move player
        
        uses velocity damping to control movement
        Alternative movement:
         self.body.apply_impulse_at_local_point((0, self.speed), (0, 0))

        """

        self.vel = self.damp*self.vel

        if settings.checkKey("up"):
            self.vel += (0, -self.speed)
        if settings.checkKey("down"):
            self.vel += (0, self.speed)
        if settings.checkKey("left"):
            self.vel += (-self.speed, 0)
        if settings.checkKey("right"):
            self.vel += (self.speed, 0)

        if self.vel.length() > self.speed:
            self.vel *= 0.717
        
        old_pos = self.pos.copy()
        self.pos += self.vel * self.game.clock.get_time() / 1000
        collision = self.detect_collision()
        while collision:
            self.pos = old_pos + collision[1]
            collision = self.detect_collision()


    def update(self) -> None:
        self.move()
        #self.particles.update_position(self.body.position)#pygame.mouse.get_pos())

        
    def draw(self, win: pygame.Surface, transform = None):
        x, y = self.pos
        if not transform:
            # pygame.draw.rect(win, settings.GREEN, (x-7.5, y-7.5, 15, 15))
            pygame.draw.circle(win, settings.GREEN, (x,y), self.radius)
        else: 
            x, y = transform(self.body.position)
            pygame.draw.rect(win, settings.WHITE, (x-7.5, y-7.5, 15, 15))

        pygame.draw.polygon(win, settings.RED, self.wall.exterior.coords)
