
# Import modules
import pygame
import math
import random
pygame.init()

# Initialize constants
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

display_width = 800
display_height = 600
player_size = 10
fd_fric = 0.5
bd_fric = 0.1
player_max_speed = 20
player_max_rtspd = 10
bullet_speed = 15
saucer_speed = 5
small_saucer_accuracy = 10

# Make surface and display
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Asteroids")
timer = pygame.time.Clock()
bg = pygame.image.load("sprites/fundo-3.png")
def background(bg):
    size = pygame.transform.scale(bg, (display_width, display_height))
    gameDisplay.blit(size, (0, 0))

# Create function to draw texts
def drawText(msg, color, x, y, s, center=True):
    screen_text = pygame.font.Font("sprites/BitPap.ttf", s).render(msg, True, color)
    if center:
        rect = screen_text.get_rect()
        rect.center = (x, y)
    else:
        rect = (x, y)
    gameDisplay.blit(screen_text, rect)


# Create funtion to chek for collision
def isColliding(x, y, xTo, yTo, size):
    if x > xTo - size and x < xTo + size and y > yTo - size and y < yTo + size:
        return True
    return False


# Create class asteroid
class Asteroid:
    def __init__(self, x, y, t):
        self.x = x
        self.y = y

        # Definir o tamanho com base no tipo de asteroide
        if t == "Large":
            self.size = 100  # tamanho real da imagem
        elif t == "Normal":
            self.size = 50  # tamanho real da imagem
        else:
            self.size = 25  # tamanho real da imagem
        self.t = t

        # Carregar a imagem e redimensioná-la de acordo com o tipo
        self.image = pygame.image.load("sprites/asteroid.png")
        self.image = pygame.transform.scale(self.image, (self.size, self.size))  # ajustar o tamanho real da imagem

        # Calcular a hitbox com base nas dimensões da imagem
        self.hitbox = self.image.get_rect(topleft=(self.x - 12, self.y - 12))

        # Definir a velocidade e direção
        self.speed = random.uniform(0.5, (40 - self.size) * 2 / 15)
        self.dir = random.randrange(0, 360) * math.pi / 180

    def updateAsteroid(self):
        # Movimentar o asteroide
        self.x += self.speed * math.cos(self.dir)
        self.y += self.speed * math.sin(self.dir)

        # Verificar se o asteroide saiu da tela e reposicioná-lo
        if self.x > display_width:
            self.x = 0
        elif self.x < 0:
            self.x = display_width
        if self.y > display_height:
            self.y = 0
        elif self.y < 0:
            self.y = display_height

        # Atualizar a posição da hitbox com base na nova posição do asteroide
        self.hitbox.topleft = (self.x, self.y)

        # Desenhar a hitbox (opcional, para depuração)
        pygame.draw.rect(gameDisplay, (255, 0, 0), self.hitbox, 2)
        # Desenhar o asteroide
        gameDisplay.blit(self.image, (int(self.x), int(self.y)))

# Create class bullet
class Bullet:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.dir = direction
        self.life = 30

    def updateBullet(self):
        # Moving
        self.x += bullet_speed * math.cos(self.dir * math.pi / 180)
        self.y += bullet_speed * math.sin(self.dir * math.pi / 180)

        # Drawing
        #pygame.draw.circle(gameDisplay, white, (int(self.x), int(self.y)), 3)
        player_bullet = pygame.image.load("sprites/pixil-frame-0.png")
        gameDisplay.blit(player_bullet, (int(self.x), int(self.y)))

        # Wrapping
        if self.x > display_width:
            self.x = 0
        elif self.x < 0:
            self.x = display_width
        elif self.y > display_height:
            self.y = 0
        elif self.y < 0:
            self.y = display_height
        self.life -= 1


# Create class saucer
class Saucer:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.state = "Dead"
        self.type = "Large"
        self.dirchoice = ()
        self.bullets = []
        self.cd = 0
        self.bdir = 0

    def updateSaucer(self):
        # Move player
        self.x += saucer_speed * math.cos(self.dir * math.pi / 180)
        self.y += saucer_speed * math.sin(self.dir * math.pi / 180)

        # Choose random direction
        if random.randrange(0, 100) == 1:
            self.dir = random.choice(self.dirchoice)

        # Wrapping
        if self.y < 0:
            self.y = display_height
        elif self.y > display_height:
            self.y = 0
        if self.x < 0 or self.x > display_width:
            self.state = "Dead"

        # Shooting
        if self.type == "Large":
            self.bdir = random.randint(0, 360)
        if self.cd == 0:
            self.bullets.append(Bullet(self.x, self.y, self.bdir))
            self.cd = 30
        else:
            self.cd -= 1

        saucer_bullet = pygame.image.load("sprites/tirotestesaucer.png")
        gameDisplay.blit(saucer_bullet, (int(self.x), int(self.y)))

    def createSaucer(self):
        # Create saucer
        # Set state
        self.state = "Alive"

        # Set random position
        self.x = random.choice((0, display_width))
        self.y = random.randint(0, display_height)

        # Set random type
        if random.randint(0, 1) == 0:
            self.type = "Large"
            self.size = 20
        else:
            self.type = "Small"
            self.size = 10
        # Create random direction
        if self.x == 0:
            self.dir = 0
            self.dirchoice = (0, 45, -45)
        else:
            self.dir = 180
            self.dirchoice = (180, 135, -135)

        # Reset bullet cooldown
        self.cd = 0

    def drawSaucer(self):
        # Draw saucer
       saucer = pygame.image.load("sprites/pixil-frame-1.png")
       gameDisplay.blit(saucer, (self.x, self.y))




# Create class for shattered ship
class deadPlayer:
    def __init__(self, x, y, l):
        self.angle = random.randrange(0, 360) * math.pi / 180
        self.dir = random.randrange(0, 360) * math.pi / 180
        self.rtspd = random.uniform(-0.25, 0.25)
        self.x = x
        self.y = y
        self.lenght = l
        self.speed = random.randint(2, 8)

    def updateDeadPlayer(self):
        pygame.draw.line(gameDisplay, white,
                         (self.x + self.lenght * math.cos(self.angle) / 2,
                          self.y + self.lenght * math.sin(self.angle) / 2),
                         (self.x - self.lenght * math.cos(self.angle) / 2,
                          self.y - self.lenght * math.sin(self.angle) / 2))
        self.angle += self.rtspd
        self.x += self.speed * math.cos(self.dir)
        self.y += self.speed * math.sin(self.dir)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.red = [pygame.image.load("sprites/explosao-0.png"), pygame.image.load("sprites/explosao-1.png"),
                    pygame.image.load("sprites/explosao-2.png"), pygame.image.load("sprites/explosao-3.png"),
                    pygame.image.load("sprites/explosao-4.png"), pygame.image.load("sprites/explosao-5.png")]
        self.index = 0
        self.image = self.red[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        self.counter += 1
        explosion_speed = 4
        if self.counter >= explosion_speed:
            self.index += 1
            self.counter = 0

        if self.index < len(self.red):
            self.image = self.red[self.index]
        else:
            self.kill()

# Class player
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hspeed = 0
        self.vspeed = 0
        self.dir = -90  # Direção inicial (em graus)
        self.rtspd = 0
        self.thrust = False

        # Carregar e redimensionar a imagem do jogador
        self.image = pygame.image.load("sprites/nave.png")
        self.image = pygame.transform.scale(self.image, (40, 40))  # Redimensionar para 40x40 pixels
        self.image_orig = self.image  # Manter a imagem original para rotação

        # Criar a hitbox com base no tamanho da imagem, sem rotação
        self.hitbox = pygame.Rect(self.x - 20, self.y - 20, 40, 40)  # Hitbox 40x40 (tamanho fixo)

    def updatePlayer(self):
        # Calcular a velocidade com base na direção e na aceleração
        speed = math.sqrt(self.hspeed ** 2 + self.vspeed ** 2)
        if self.thrust:
            if speed + fd_fric < player_max_speed:
                self.hspeed += fd_fric * math.cos(self.dir * math.pi / 180)
                self.vspeed += fd_fric * math.sin(self.dir * math.pi / 180)
            else:
                self.hspeed = player_max_speed * math.cos(self.dir * math.pi / 180)
                self.vspeed = player_max_speed * math.sin(self.dir * math.pi / 180)
        else:
            # Aplicar fricção quando não houver impulso
            self.hspeed *= 0.99
            self.vspeed *= 0.99

        # Atualizar a posição do jogador
        self.x += self.hspeed
        self.y += self.vspeed

        # Verificar se o jogador saiu da tela e reposicioná-lo
        if self.x > display_width:
            self.x = 0
        elif self.x < 0:
            self.x = display_width
        if self.y > display_height:
            self.y = 0
        elif self.y < 0:
            self.y = display_height

        # Atualizar a rotação do jogador
        self.dir += self.rtspd
        self.image = pygame.transform.rotate(self.image_orig, -self.dir)  # Rotacionar a imagem conforme a direção

        # Atualizar a posição da hitbox para acompanhar o jogador, mas sem rotação
        self.hitbox.topleft = (self.x - 20, self.y - 20)  # Hitbox permanece no centro da imagem

    def drawPlayer(self):
        # Desenhar o jogador na tela
        gameDisplay.blit(self.image, (self.x - self.image.get_width() / 2, self.y - self.image.get_height() / 2))

        # Desenhar a hitbox (opcional, para depuração)
        pygame.draw.rect(gameDisplay, (255, 0, 0), self.hitbox, 2)

    def killPlayer(self):
        # Resetar o jogador para a posição inicial
        self.x = display_width / 2
        self.y = display_height / 2
        self.thrust = False
        self.dir = -90
        self.hspeed = 0
        self.vspeed = 0

def gameLoop(startingState):
    # Init variables
    gameState = startingState
    player_state = "Alive"
    player_blink = 0
    player_pieces = []
    player_pieces_frame = 7
    player_pieces_frame_cont = 0
    player_pieces_indice = 0
    player_pieces_draw = False
    player_dying_delay = 0
    player_invi_dur = 0
    hyperspace = 0
    next_level_delay = 0
    bullet_capacity = 4
    bullets = []
    asteroids = []
    stage = 3
    score = 0
    live = 2
    oneUp_multiplier = 1
    playOneUpSFX = 0
    intensity = 0
    player = Player(display_width / 2, display_height / 2)
    saucer = Saucer()
    explosion = Explosion(1, 1)

    # Main loop
    while gameState != "Exit":
        # Game menu
        while gameState == "Menu":
            gameDisplay.fill(black)
            drawText("ASTEROIDES", white, display_width / 2, display_height / 2, 100)
            drawText("Aperte qualquer botao para iniciar", white, display_width / 2, display_height / 2 + 100, 50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameState = "Exit"
                if event.type == pygame.KEYDOWN:
                    gameState = "Playing"
            pygame.display.update()
            timer.tick(5)

        # User inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameState = "Exit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.thrust = True
                if event.key == pygame.K_LEFT:
                    player.rtspd = -player_max_rtspd
                if event.key == pygame.K_RIGHT:
                    player.rtspd = player_max_rtspd
                if event.key == pygame.K_SPACE and player_dying_delay == 0 and len(bullets) < bullet_capacity:
                    bullets.append(Bullet(player.x, player.y, int(player.dir)))
                    # Play SFX

                if gameState == "Game Over":
                    if event.key == pygame.K_r:
                        gameState = "Exit"
                        gameLoop("Playing")
                if event.key == pygame.K_LSHIFT:
                    hyperspace = 30
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player.thrust = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.rtspd = 0

        # Update player
        player.updatePlayer()

        # Checking player invincible time
        if player_invi_dur != 0:
            player_invi_dur -= 1
        elif hyperspace == 0:
            player_state = "Alive"

        # Reset display
        gameDisplay.fill(black)

        background(bg)

        # Hyperspace
        if hyperspace != 0:
            player_state = "Died"
            hyperspace -= 1
            if hyperspace == 1:
                player.x = random.randrange(0, display_width)
                player.y = random.randrange(0, display_height)

        # Check for collision w/ asteroid
        for a in asteroids:
            a.updateAsteroid()
            if player_state != "Died":
                if isColliding(player.x, player.y, a.x, a.y, a.size):
                    # Create ship fragments




                    # Kill player
                    player_state = "Died"
                    player_dying_delay = 30
                    player_invi_dur = 120
                    player.killPlayer()

                    if live != 0:
                        live -= 1
                    else:
                        gameState = "Game Over"

                    # Split asteroid
                    if a.t == "Large":
                        asteroids.remove(a)
                        score += 50


        # Update ship fragments
        for f in player_pieces:
            f.updateDeadPlayer()
            if f.x > display_width or f.x < 0 or f.y > display_height or f.y < 0:
                player_pieces.remove(f)

        # Check for end of stage
        if len(asteroids) == 0 and saucer.state == "Dead":
            if next_level_delay < 30:
                next_level_delay += 1
            else:
                stage += 1
                intensity = 0
                # Spawn asteroid away of center
                for i in range(stage):
                    xTo = display_width / 2
                    yTo = display_height / 2
                    while xTo - display_width / 2 < display_width / 4 and yTo - display_height / 2 < display_height / 4:
                        xTo = random.randrange(0, display_width)
                        yTo = random.randrange(0, display_height)
                    asteroids.append(Asteroid(xTo, yTo, "Large"))
                next_level_delay = 0

        # Update intensity
        if intensity < stage * 450:
            intensity += 1

        # Saucer
        if saucer.state == "Dead":
            if random.randint(0, 6000) <= (intensity * 2) / (stage * 9) and next_level_delay == 0:
                saucer.createSaucer()
                # Only small saucers >40000
                if score >= 10000:
                    saucer.type = "Small"
        else:
            # Set saucer targer dir
            acc = small_saucer_accuracy * 4 / stage
            saucer.bdir = math.degrees(math.atan2(-saucer.y + player.y, -saucer.x + player.x) + math.radians(random.uniform(acc, -acc)))

            saucer.updateSaucer()
            saucer.drawSaucer()

            # Check for collision w/ asteroid
            for s in asteroids:
                if isColliding(saucer.x, saucer.y, s.x, s.y, s.size + saucer.size):
                    # Set saucer state
                    saucer.state = "Dead"

                    # Split asteroid
                    if a.t == "Large":
                        asteroids.remove(a)
                        # Play SFX

            # Check for collision w/ bullet
            for b in bullets:
                if isColliding(b.x, b.y, saucer.x, saucer.y, saucer.size):
                    # Add points
                    if saucer.type == "Large":
                        score += 200
                    else:
                        score += 1000

                    # Set saucer state
                    saucer.state = "Dead"

                    # Play SFX


                    # Remove bullet
                    bullets.remove(b)

            # Check collision w/ player
            if isColliding(saucer.x, saucer.y, player.x, player.y, saucer.size):
                if player_state != "Died":
                    # Create ship fragments
                    player_pieces.append(
                        deadPlayer(player.x, player.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3)))))
                    player_pieces.append(
                        deadPlayer(player.x, player.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3)))))
                    player_pieces.append(deadPlayer(player.x, player.y, player_size))

            # Saucer's bullets
            for b in saucer.bullets:
                # Update bullets
                b.updateBullet()

                # Check for collision w/ asteroids
                for a in asteroids:
                    if isColliding(b.x, b.y, a.x, a.y, a.size):
                        # Split asteroid
                        if a.t == "Large":
                            asteroids.remove(a)

                        # Remove asteroid and bullet
                        saucer.bullets.remove(b)

                        break

                # Check for collision w/ player
                if isColliding(player.x, player.y, b.x, b.y, 5):
                    if player_state != "Died":
                        # Create ship fragments
                        # Kill player
                        player_state = "Died"
                        player_dying_delay = 30
                        player_invi_dur = 120
                        player.killPlayer()

                        if live != 0:
                            live -= 1
                        else:
                            gameState = "Game Over"

                        # Play SFX


                        # Remove bullet
                        saucer.bullets.remove(b)

                if b.life <= 0:
                    try:
                        saucer.bullets.remove(b)
                    except ValueError:
                        continue

        # Bullets
        for b in bullets:
            # Update bullets
            b.updateBullet()

            # Check for bullets collide w/ asteroid
            for a in asteroids:
                if b.x > a.x - a.size and b.x < a.x + a.size and b.y > a.y - a.size and b.y < a.y + a.size:
                    # Split asteroid
                    if a.t == "Large":
                        asteroids.remove(a)
                        score += 50
                        # Play SFX
                    bullets.remove(b)

                    break

            # Destroying bullets
            if b.life <= 0:
                try:
                    bullets.remove(b)
                except ValueError:
                    continue

        # Extra live
        if score > oneUp_multiplier * 10000:
            oneUp_multiplier += 1
            live += 1
            playOneUpSFX = 60
        # Play sfx
        if playOneUpSFX > 0:
            playOneUpSFX -= 1


        # Draw player
        if gameState != "Game Over":
            if player_state == "Died":
                if hyperspace == 0:
                    if player_dying_delay == 0:
                        if player_blink < 5:
                            if player_blink == 0:
                                player_blink = 10
                            else:
                                player.drawPlayer()
                        player_blink -= 1
                    else:
                        player_dying_delay -= 1
            else:
                player.drawPlayer()
        else:
            drawText("Game Over", white, display_width / 2, display_height / 2, 100)
            drawText("Press \"R\" to restart!", white, display_width / 2, display_height / 2 + 100, 50)
            live = -1

        # Draw score
        drawText(str(score), white, 60, 20, 40, False)

        # Draw Lives
        for l in range(live + 1):
            Player(75 + l * 25, 75).drawPlayer()

        # Update screen
        pygame.display.update()

        # Tick fps
        timer.tick(30)


# Start game
gameLoop("Menu")

# End game
pygame.quit()
quit()
