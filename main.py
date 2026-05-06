import pygame
import random
import time

# Configuration
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
LANE_HEIGHT = 50
ROAD_TOP = 200
CAR_LENGTH = 40
CAR_WIDTH = 20
VERTICAL_LANE_WIDTH = 60
SPAWN_INTERVAL = 2  # seconds
TRAFFIC_LIGHT_INTERVAL = 10  # seconds

# Colors
WHITE = (255, 255, 255)
GREY = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)

def draw_dashed_line(surface, color, start_pos, end_pos, width=1, dash_length=5):
    x1, y1 = start_pos
    x2, y2 = end_pos
    dl = dash_length
    if x1 == x2:  # vertical line
        ycoords = list(range(y1, y2, dl * 2))
        for y in ycoords:
            pygame.draw.line(surface, color, (x1, y), (x1, min(y + dl, y2)), width)
    elif y1 == y2:  # horizontal line
        xcoords = list(range(x1, x2, dl * 2))
        for x in xcoords:
            pygame.draw.line(surface, color, (x, y1), (min(x + dl, x2), y1), width)

class TrafficLight:
    def __init__(self, x, y, lane='upper', group='horizontal'):
        self.x = x
        self.y = y
        self.lane = lane
        self.group = group
        self.state = 'green'
        self.last_switch_time = time.time()

    def update(self, sync_group):
        now = time.time()
        if now - self.last_switch_time >= TRAFFIC_LIGHT_INTERVAL:
            self.state = 'green' if self.state == 'red' else 'red'
            self.last_switch_time = now
            for light in sync_group:
                light.state = 'red' if self.state == 'green' else 'green'
                light.last_switch_time = now

    def draw(self, screen):
        color = GREEN if self.state == 'green' else RED
        pygame.draw.circle(screen, color, (self.x, self.y), 10)
        time_remaining = max(0, int(TRAFFIC_LIGHT_INTERVAL - (time.time() - self.last_switch_time)))
        font = pygame.font.SysFont(None, 20)
        timer_text = font.render(str(time_remaining), True, WHITE)
        screen.blit(timer_text, (self.x + 12, self.y - 8))

class Vehicle:
    def __init__(self, direction='right', origin='main'):
        self.direction = direction
        self.origin = origin
        self.spawn_time = time.time()
        self.wait_time = 0
        self.from_vertical = False

        if origin == 'main':
            self.lane_y = ROAD_TOP + (LANE_HEIGHT // 2) - (CAR_WIDTH // 2) if direction == 'right' else ROAD_TOP + LANE_HEIGHT + (LANE_HEIGHT // 2) - (CAR_WIDTH // 2)
            self.x = -CAR_LENGTH if direction == 'right' else SCREEN_WIDTH + CAR_LENGTH
        elif origin == 'top':
            self.lane_x = 300 + LANE_HEIGHT // 4 + (VERTICAL_LANE_WIDTH - CAR_WIDTH) // 2
            self.y = -CAR_LENGTH
        elif origin == 'bottom':
            self.lane_x = 900 - LANE_HEIGHT // 4 - VERTICAL_LANE_WIDTH + (VERTICAL_LANE_WIDTH - CAR_WIDTH) // 2
            self.y = SCREEN_HEIGHT + CAR_LENGTH

        self.speed = random.randint(80, 120) / 3.6
        self.color = BLUE
        self.length = CAR_LENGTH
        self.width = CAR_WIDTH
        self.stopped = False

    def update(self, dt, vehicles, traffic_lights):
        self.stopped = False

        if self.origin == 'main':
            if not self.from_vertical:
                for light in traffic_lights:
                    if light.group != 'horizontal': continue
                    if light.state == 'red':
                        if light.lane == 'upper' and self.direction == 'right' and self.x < light.x < self.x + 60:
                            self.stopped = True
                            return
                        elif light.lane == 'lower' and self.direction == 'left' and self.x > light.x > self.x - 60:
                            self.stopped = True
                            return

            for other in vehicles:
                if other == self: continue
                if other.origin == 'main' and other.lane_y == self.lane_y:
                    if self.direction == 'right' and other.x > self.x and other.x - self.x < CAR_LENGTH + 10:
                        self.stopped = True
                        return
                    elif self.direction == 'left' and other.x < self.x and self.x - other.x < CAR_LENGTH + 10:
                        self.stopped = True
                        return

            self.x += self.speed * dt if self.direction == 'right' else -self.speed * dt

        elif self.origin == 'top':
            for light in traffic_lights:
                if light.lane == 'top' and light.state == 'red' and self.y + self.length >= ROAD_TOP:
                    self.stopped = True
                    return
            for other in vehicles:
                if other == self: continue
                if other.origin == 'top' and other.lane_x == self.lane_x and other.y > self.y and other.y - self.y < CAR_LENGTH + 10:
                    self.stopped = True
                    return
            if self.y + self.length < ROAD_TOP:
                self.y += self.speed * dt
            else:
                self.origin = 'main'
                self.direction = 'right'
                self.x = 300
                self.lane_y = ROAD_TOP + (LANE_HEIGHT // 2) - (CAR_WIDTH // 2)
                self.from_vertical = True

        elif self.origin == 'bottom':
            for light in traffic_lights:
                if light.lane == 'bottom' and light.state == 'red' and self.y - self.length <= ROAD_TOP + 2 * LANE_HEIGHT:
                    self.stopped = True
                    return
            for other in vehicles:
                if other == self: continue
                if other.origin == 'bottom' and other.lane_x == self.lane_x and other.y < self.y and self.y - other.y < CAR_LENGTH + 10:
                    self.stopped = True
                    return
            if self.y > ROAD_TOP + 2 * LANE_HEIGHT:
                self.y -= self.speed * dt
            else:
                self.origin = 'main'
                self.direction = 'left'
                self.x = 900
                self.lane_y = ROAD_TOP + LANE_HEIGHT + (LANE_HEIGHT // 2) - (CAR_WIDTH // 2)
                self.from_vertical = True

    def draw(self, screen):
        if self.origin == 'main':
            rect = (self.x, self.lane_y, self.length, self.width) if self.direction == 'right' else (self.x - self.length, self.lane_y, self.length, self.width)
        elif self.origin == 'top':
            rect = (self.lane_x, self.y, self.width, self.length)
        elif self.origin == 'bottom':
            rect = (self.lane_x, self.y - self.length, self.width, self.length)
        pygame.draw.rect(screen, self.color, rect)

class TrafficSimulation:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Traffic Flow Simulation")
        self.clock = pygame.time.Clock()
        self.vehicles = []
        self.last_spawn_time = time.time()
        self.traffic_lights = [
            TrafficLight(300, ROAD_TOP - 30, 'top', 'vertical'),
            TrafficLight(900, ROAD_TOP + 2 * LANE_HEIGHT + 30, 'bottom', 'vertical'),
            TrafficLight(300 + LANE_HEIGHT // 4, ROAD_TOP, 'upper', 'horizontal'),
            TrafficLight(900 - LANE_HEIGHT // 4, ROAD_TOP + 2 * LANE_HEIGHT, 'lower', 'horizontal')
        ]
        self.font = pygame.font.SysFont(None, 24)

    def spawn_vehicle(self):
        if time.time() - self.last_spawn_time > SPAWN_INTERVAL:
            rnd = random.random()
            if rnd < 0.4:
                self.vehicles.append(Vehicle('right', 'main'))
            elif rnd < 0.8:
                self.vehicles.append(Vehicle('left', 'main'))
            elif rnd < 0.9:
                self.vehicles.append(Vehicle('down', 'top'))
            else:
                self.vehicles.append(Vehicle('up', 'bottom'))
            self.last_spawn_time = time.time()

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.traffic_lights[2].update([self.traffic_lights[0], self.traffic_lights[1]])
            self.traffic_lights[3].state = self.traffic_lights[2].state
            self.traffic_lights[3].last_switch_time = self.traffic_lights[2].last_switch_time

            self.spawn_vehicle()
            self.screen.fill(GREY)
            self.draw_road()

            for v in self.vehicles:
                v.update(dt, self.vehicles, self.traffic_lights)
                v.draw(self.screen)

            for light in self.traffic_lights:
                light.draw(self.screen)

            self.display_statistics()
            pygame.display.flip()

        pygame.quit()

    def draw_road(self):
        # Solid horizontal lines
        for i in range(3):
            y = ROAD_TOP + i * LANE_HEIGHT
            pygame.draw.line(self.screen, WHITE, (0, y), (SCREEN_WIDTH, y), 2)

        # Dashed center lines in horizontal lanes
        center_y_upper = ROAD_TOP + (LANE_HEIGHT // 2)
        center_y_lower = ROAD_TOP + LANE_HEIGHT + (LANE_HEIGHT // 2)
        draw_dashed_line(self.screen, WHITE, (0, center_y_upper), (SCREEN_WIDTH, center_y_upper))
        draw_dashed_line(self.screen, WHITE, (0, center_y_lower), (SCREEN_WIDTH, center_y_lower))

        # Vertical lane V1 (top vertical lane)
        x_top = 300 + LANE_HEIGHT // 4
        lane_width = VERTICAL_LANE_WIDTH
        pygame.draw.line(self.screen, WHITE, (x_top, 0), (x_top, ROAD_TOP), 2)
        draw_dashed_line(self.screen, WHITE, (x_top + lane_width // 2, 0), (x_top + lane_width // 2, ROAD_TOP))
        pygame.draw.line(self.screen, WHITE, (x_top + lane_width, 0), (x_top + lane_width, ROAD_TOP), 2)

        # Vertical lane V2 (bottom vertical lane) — mirrored and styled like V1
        x_bot = 900 - LANE_HEIGHT // 4 - VERTICAL_LANE_WIDTH
        pygame.draw.line(self.screen, WHITE, (x_bot, ROAD_TOP + 2 * LANE_HEIGHT), (x_bot, SCREEN_HEIGHT), 2)
        draw_dashed_line(self.screen, WHITE, (x_bot + lane_width // 2, ROAD_TOP + 2 * LANE_HEIGHT), (x_bot + lane_width // 2, SCREEN_HEIGHT))
        pygame.draw.line(self.screen, WHITE, (x_bot + lane_width, ROAD_TOP + 2 * LANE_HEIGHT), (x_bot + lane_width, SCREEN_HEIGHT), 2)

        # --- PEDESTRIAN CROSSING ---
        # Top vertical lane crossing lines
        for i in range(0, lane_width, 10):
            pygame.draw.line(self.screen, WHITE, (x_top + i, ROAD_TOP - 15), (x_top + i, ROAD_TOP + 15), 2)

        # Bottom vertical lane crossing lines (mirroring top)
        for i in range(0, lane_width, 10):
            pygame.draw.line(self.screen, WHITE, (x_bot + i, ROAD_TOP + 2 * LANE_HEIGHT - 15), (x_bot + i, ROAD_TOP + 2 * LANE_HEIGHT + 15), 2)

        # --- HORIZONTAL LANE LINES AND PEDESTRIAN CROSSINGS ---
        for i in range(0, 40, 10):
            pygame.draw.line(self.screen, WHITE, (290 - 15, ROAD_TOP + i), (290 + 15, ROAD_TOP + i), 2)
            pygame.draw.line(self.screen, WHITE, (910 - 15, ROAD_TOP + LANE_HEIGHT + i), (910 + 15, ROAD_TOP + LANE_HEIGHT + i), 2)

        # --- ARROWS ---
        arrow_font = pygame.font.SysFont(None, 40)
        # Horizontal lanes
        self.screen.blit(arrow_font.render("→", True, WHITE), (200, ROAD_TOP + 5))
        self.screen.blit(arrow_font.render("←", True, WHITE), (1000, ROAD_TOP + LANE_HEIGHT + 5))
        # Vertical lanes
        self.screen.blit(arrow_font.render("↑", True, WHITE), (x_bot + 15, SCREEN_HEIGHT - 60))
        self.screen.blit(arrow_font.render("↓", True, WHITE), (x_top + 15, 20))

        # --- LANE LABELS ---
        label_font = pygame.font.SysFont(None, 18)
        labels = {'upper': "H1", 'lower': "H2", 'top': "V1", 'bottom': "V2"}
        for light in self.traffic_lights:
            label = labels.get(light.lane, "")
            text = label_font.render(label, True, WHITE)
            self.screen.blit(text, (light.x - 12, light.y + 12))

        # Horizontal lane boundary lines for H1 and H2
        pygame.draw.line(self.screen, WHITE, (290, ROAD_TOP - 10), (290, ROAD_TOP + LANE_HEIGHT), 3)  # H1
        pygame.draw.line(self.screen, WHITE, (910, ROAD_TOP + LANE_HEIGHT), (910, ROAD_TOP + 2 * LANE_HEIGHT + 10), 3)  # H2

        # Horizontal lane boundary lines for V1 and V2 (already drawn above as vertical lanes)

    def display_statistics(self):
        if self.vehicles:
            avg_wait = sum(v.wait_time for v in self.vehicles) / len(self.vehicles)
        else:
            avg_wait = 0
        text = self.font.render(f"Vehicles: {len(self.vehicles)} | Avg Wait: {avg_wait:.1f}s", True, YELLOW)
        self.screen.blit(text, (10, 10))

if __name__ == "__main__":
    sim = TrafficSimulation()
    sim.run()