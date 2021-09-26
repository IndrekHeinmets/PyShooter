import pygame, csv, button, os
pygame.init()

class MainGame():
    def __init__(self):
        # Screen settings
        self.FPS = 120
        self.WIDTH, self.HEIGHT = 800, 640
        self.BOTTOM_MARGIN = 120
        self.SIDE_MARGIN = 300
        self.ROWS = 16
        self.MAX_COLS = 150

        # Colors
        self.BLUE = (0, 194, 162)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (200, 25, 25)

        # Font
        self.FONT = pygame.font.Font('font\\futura.ttf', 20)

        self.clock = pygame.time.Clock()
        self. screen = pygame.display.set_mode((self.WIDTH + self.SIDE_MARGIN, self.HEIGHT + self.BOTTOM_MARGIN))
        pygame.display.set_caption('Level Editor')

        # Create world data structure
        self.world_data = []

        # System variables
        self.TILE_SIZE = self.HEIGHT // self.ROWS
        self.TILE_TYPES = 22
        self.scroll_left = False
        self.scroll_right = False
        self.scroll = 0
        self.scroll_speed = 1
        self.current = 0
        self.level = 1
        self.shift_down = False
        self.file_not_found = False
        self.file_already_exists = False
        self.saved = False
        self.file_removed = False
        self.delete_conf = False
        self.entries = []

        # Load bg images
        self.sky_img = pygame.image.load('img\\background\\sky.png').convert_alpha()
        self.mountain_img = pygame.image.load('img\\background\\mountain.png').convert_alpha()
        self.pine1_img = pygame.image.load('img\\background\\pine1.png').convert_alpha()
        self.pine2_img = pygame.image.load('img\\background\\pine2.png').convert_alpha()

        # Load tile images
        self.tile_img_list = []
        for i in range(self.TILE_TYPES):
            self.img = pygame.transform.scale(pygame.image.load(f'img\\tile\\{i}.png').convert_alpha(), (self.TILE_SIZE, self.TILE_SIZE))
            self.tile_img_list.append(self.img)

        # Load UI images
        self.save_img = pygame.image.load('img\\save_btn.png').convert_alpha()
        self.load_img = pygame.image.load('img\\load_btn.png').convert_alpha()
        self.menu_img = pygame.image.load('img\\menu_ed_btn.png').convert_alpha()
        self.delete_img = pygame.image.load('img\\delete_btn.png').convert_alpha()
        self.yes_img = pygame.image.load('img\\yes_btn.png').convert_alpha()
        self.no_img = pygame.image.load('img\\no_btn.png').convert_alpha()

    def draw_text(self, text, font, text_col, x, y):
            self.img = font.render(text, True, text_col)
            self.screen.blit(self.img, (x, y))

    def draw_bg(self):
            self.screen.fill(self.BLUE)
            self.width = self.mountain_img.get_width()
            for i in range(5):
                self.screen.blit(self.sky_img, ((i * self.width) + self.scroll * 0.5, 0))
                self.screen.blit(self.mountain_img, ((i * self.width) + self.scroll * 0.6, self.HEIGHT - self.mountain_img.get_height() - 250))
                self.screen.blit(self.pine1_img, ((i * self.width) + self.scroll * 0.8,self.HEIGHT - self.pine1_img.get_height() - 120))
                self.screen.blit(self.pine2_img, ((i * self.width) + self.scroll * 0.9, self.HEIGHT - self.pine2_img.get_height()))

    def draw_grid(self):
            # Vertical lines
            for i in range(self.MAX_COLS + 1):
                pygame.draw.line(self.screen, self.WHITE, (i * self.TILE_SIZE + self.scroll, 0), (i * self.TILE_SIZE + self.scroll, self.HEIGHT))
            # Horizontal range
            for i in range(self.ROWS + 1):
                pygame.draw.line(self.screen, self.WHITE, (0, i * self.TILE_SIZE), (self.WIDTH, i * self.TILE_SIZE))

    def create_world(self):
        for row in range(self.ROWS):
            self.r = [-1] * self.MAX_COLS
            self.world_data.append(self.r)

        # Create default ground layer
        for tile in range(0, self.MAX_COLS):
            self.world_data[self.ROWS - 1][tile] = 0

    def draw_world(self):
        for self.y, row in enumerate(self.world_data):
            for self.x, tile in enumerate(row):
                if tile >= 0:
                    self.screen.blit(self.tile_img_list[tile], (self.x * self.TILE_SIZE + self.scroll, self.y * self.TILE_SIZE))

    def clear_world(self):
        self.world_data.clear()
        self.create_world()

    def load_world_data(self):
        with open(f'levels\\level{self.level}_data.csv',
                  newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    self.world_data[x][y] = int(tile)
        return self.world_data

    def save_world_file(self):
        with open(f'levels\\level{self.level}_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for row in self.world_data:
                writer.writerow(row)

    def editor_play(self):
        # Create buttons
        self.save_button = button.Button(self.WIDTH // 2, self.HEIGHT + self.BOTTOM_MARGIN - 100, self.save_img, 0.45)
        self.load_button = button.Button(self.WIDTH // 2 + 150, self.HEIGHT + self.BOTTOM_MARGIN - 100, self.load_img, 0.45)
        self.menu_button = button.Button(self.WIDTH + 95, self.HEIGHT + self.BOTTOM_MARGIN - 100, self.menu_img, 0.45)
        self.del_button = button.Button(self.WIDTH // 2 + 300, self.HEIGHT + self.BOTTOM_MARGIN - 100, self.delete_img, 0.45)
        self.yes_button = button.Button(self.WIDTH - 90, self.HEIGHT + self.BOTTOM_MARGIN - 45, self.yes_img, 0.32)
        self.no_button = button.Button(self.WIDTH - 20, self.HEIGHT + self.BOTTOM_MARGIN - 45, self.no_img, 0.32)

        self.button_list = []
        self.button_col = 0
        self.button_row = 0
        for i in range(len(self.tile_img_list)):
            self.tile_button = button.Button(self.WIDTH + 50 + (75 * self.button_col), 75 * self.button_row + 50, self.tile_img_list[i], 1.1)
            self.button_list.append(self.tile_button)
            self.button_col += 1
            if self.button_col == 3:
                self.button_row += 1
                self.button_col = 0

        self.create_world()

        self.run = True
        while self.run:

            self.clock.tick(self.FPS)

            self.draw_bg()
            self.draw_grid()
            self.draw_world()

            self.draw_text('Press UP/DOWN to change level', self.FONT, self.BLACK, 10, self.HEIGHT + self.BOTTOM_MARGIN - 105)
            self.draw_text(f'Level: {self.level}', self.FONT, self.BLACK, 10, self.HEIGHT + self.BOTTOM_MARGIN - 70)
            self.draw_text('Press SHIFT+DEL to clear level', self.FONT, self.BLACK, 10, self.HEIGHT + self.BOTTOM_MARGIN - 35)

            # Save world data
            if self.save_button.draw(self.screen):
                pygame.draw.rect(self.screen, self.RED, self.save_button.rect, 3)
                self.file_not_found = False
                self.saved = False
                self.file_removed = False
                self.entries = os.listdir('levels')
                if (f'level{self.level}_data.csv') in self.entries:
                    self.file_already_exists = True
                else:
                    self.save_world_file()
                    self.saved = True

            # Delete level file
            if self.del_button.draw(self.screen):
                pygame.draw.rect(self.screen, self.RED, self.del_button.rect, 3)
                self.saved = False
                self.file_not_found = False
                self.file_already_exists = False
                self.entries = os.listdir('levels')
                if (f'level{self.level}_data.csv') not in self.entries:
                    self.file_not_found = True
                else:
                    self.delete_conf = True

            if self.delete_conf:
                self.draw_text(f'Permanently delete level {self.level} file?', self.FONT, self.RED, self.save_button.rect.x, self.HEIGHT + self.BOTTOM_MARGIN - 40)
                if self.yes_button.draw(self.screen):
                    pygame.draw.rect(self.screen, self.RED, self.yes_button.rect, 3)
                    self.delete_conf = False
                    try:
                        os.remove(f'levels\\level{self.level}_data.csv')
                        self.file_removed = True
                    except FileNotFoundError:
                        self.file_not_found = True
                    except Exception:
                        break
                    self.file_removed = True
                if self.no_button.draw(self.screen):
                    pygame.draw.rect(self.screen, self.RED, self.no_button.rect, 3)
                    self.delete_conf = False

            # Load existing world data
            if self.load_button.draw(self.screen):
                pygame.draw.rect(self.screen, self.RED, self.load_button.rect, 3)
                self.file_already_exists = False
                self.saved = False
                self.file_removed = False
                self.scroll = 0
                try:
                    self.load_world_data()
                    self.file_not_found = False
                except FileNotFoundError:
                    self.file_not_found = True
                except Exception:
                    break

            # Function feedback messages
            if self.saved:
                self.draw_text(f'File for level {self.level} has been saved!', self.FONT, self.BLACK, self.save_button.rect.x + 60, self.HEIGHT + self.BOTTOM_MARGIN - 40)

            if self.file_removed:
                self.draw_text(f'File for level {self.level} has been deleted!', self.FONT, self.BLACK, self.save_button.rect.x + 60, self.HEIGHT + self.BOTTOM_MARGIN - 40)

            if self.file_not_found:
                self.draw_text(f'File for level {self.level} doesn\'t exist!', self.FONT, self.RED, self.save_button.rect.x + 60, self.HEIGHT + self.BOTTOM_MARGIN - 40)

            if self.file_already_exists:
                self.draw_text(f'File for level {self.level} already exists,', self.FONT, self.RED, self.save_button.rect.x, self.HEIGHT + self.BOTTOM_MARGIN - 50)
                self.draw_text('do you wish to overwrite?', self.FONT, self.RED, self.save_button.rect.x, self.HEIGHT + self.BOTTOM_MARGIN - 30)
                if self.yes_button.draw(self.screen):
                    pygame.draw.rect(self.screen, self.RED, self.yes_button.rect, 3)
                    self.file_already_exists = False
                    self.save_world_file()
                    self.saved = True
                if self.no_button.draw(self.screen):
                    pygame.draw.rect(self.screen, self.RED, self.no_button.rect, 3)
                    self.file_already_exists = False

            # Return to main menu
            if self.menu_button.draw(self.screen):
                pygame.draw.rect(self.screen, self.RED, self.menu_button.rect, 3)
                self.run = False
                self.menu = True

            # Draw tiles panel
            pygame.draw.rect(self.screen, self.BLUE, (self.WIDTH, 0, self.SIDE_MARGIN, self.HEIGHT + 10))
            # Draw tiles
            button_count = 0
            for button_count, but in enumerate(self.button_list):
                if but.draw(self.screen):
                    self.current = button_count

            # Highlight current tile
            pygame.draw.rect(self.screen, self.RED, self.button_list[self.current].rect, 3)

            # Scroll the map
            if self.scroll_left == True and self.scroll < -12:
                self.scroll += 5 * self.scroll_speed
            if self.scroll_right == True and self.scroll > -((self.MAX_COLS * self.TILE_SIZE) - self.WIDTH):
                self.scroll -= 5 * self.scroll_speed

            # Add new tiles to the world
            # Get mouse position
            self.pos = pygame.mouse.get_pos()
            self.x = (self.pos[0] - self.scroll) // self.TILE_SIZE
            self.y = self.pos[1] // self.TILE_SIZE

            # Check position is in world editor window
            if self.pos[0] < self.WIDTH and self.pos[1] < self.HEIGHT:
                # Add tile
                if pygame.mouse.get_pressed()[0] == 1:
                    if self.world_data[self.y][self.x] != self.current:
                        self.world_data[self.y][self.x] = self.current
                # Remove tile
                if pygame.mouse.get_pressed()[2] == 1:
                        self.world_data[self.y][self.x] = -1

            # Event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    self.menu = False
                # Keyboard keys pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.run = False
                    if event.key == pygame.K_RIGHT:
                        self.scroll_right = True
                    if event.key == pygame.K_LEFT:
                        self.scroll_left = True
                    if event.key == pygame.K_LSHIFT:
                        self.shift_down = True
                        self.scroll_speed = 4
                    if event.key == pygame.K_UP:
                        self.level += 1
                        self.file_not_found = False
                        self.file_already_exists = False
                        self.saved = False
                        self.file_removed = False
                    if event.key == pygame.K_DOWN and self.level > 1:
                        self.level -= 1
                        self.file_not_found = False
                        self.file_already_exists = False
                        self.saved = False
                        self.file_removed = False
                    if event.key == pygame.K_DELETE and self.shift_down:
                        self.clear_world()
                        self.scroll = 0
                        self.shift_down = False
                # Keyboard keys released
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.scroll_right = False
                    if event.key == pygame.K_LEFT:
                        self.scroll_left = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift_down = False
                        self.scroll_speed = 1

            pygame.display.update()
        return self.run, self.menu