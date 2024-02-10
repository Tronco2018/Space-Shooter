import pygame
import sys
import random
from pygame import mixer

# Inizializzazione di Pygame
pygame.init()

# Musica di sottofondo
mixer.init()
mixer.music.load("theme.mp3")
mixer.music.play()

# Dimensioni finestra
larghezza, altezza = 600, 800

# Creazione finestra
fin = pygame.display.set_mode((larghezza, altezza))
pygame.display.set_caption("Shooter game")


# Caricamento immagine dell'icona
icona = pygame.image.load("nemici.png")

# Impostazione dell'icona della finestra
pygame.display.set_icon(icona)

# Caricamento immagini
navicella_img = pygame.image.load("navicella.png")
nemici_img = pygame.image.load("nemici.png")

# Ridimensionamento immagini
quadrato_size = 40
navicella_img = pygame.transform.scale(navicella_img, (quadrato_size, quadrato_size))
nemici_img = pygame.transform.scale(nemici_img, (quadrato_size, quadrato_size))

# Velocità di movimento del giocatore
velocita_giocatore = 1

# Velocità di movimento dei nemici
velocita_nemici = 0.5

# Velocità dei proiettili
velocita_proiettili = 2
velocita_proiettili_nemici = 1

# Punteggio
punteggio = 0

# Font
font = pygame.font.Font(None, 36)

# Caricamento effetti sonori
pygame.mixer.init()
shoot_sound = pygame.mixer.Sound("shoot.wav")
death_sound = pygame.mixer.Sound("death.wav")

# Classe per il giocatore
class Player:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def draw(self, screen):
        screen.blit(navicella_img, (self.x, self.y))

    def move(self, dx):
        # Limita il movimento del giocatore entro i limiti della finestra
        if 0 <= self.x + dx <= larghezza - self.size:
            self.x += dx

# Classe per i nemici
class Enemy:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.direction = 1  # 1 per destra, -1 per sinistra
        self.last_shot_time = 0  # Tempo dell'ultimo colpo sparato

    def draw(self, screen):
        screen.blit(nemici_img, (self.x, self.y))

    def move(self):
        self.x += self.direction * velocita_nemici

    def shoot(self):
        current_time = pygame.time.get_ticks()  # Ottieni il tempo corrente in millisecondi
        if current_time - self.last_shot_time > 3000:  # Ritardo di 3 secondi (3000 millisecondi)
            self.last_shot_time = current_time
            return True
        return False

# Classe per i proiettili sparati dalla navicella
class PlayerBullet:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.size, self.size))

    def move(self):
        self.y -= velocita_proiettili

# Classe per i proiettili sparati dai nemici
class EnemyBullet:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.size, self.size))

    def move(self):
        self.y += velocita_proiettili_nemici

# Coordinare e dimensioni del muro
muro_x = 200
muro_y = 500
muro_larghezza = 200
muro_altezza = 20

# Creazione del giocatore
player = Player(larghezza // 2 - quadrato_size // 2, 750, quadrato_size)

# Lista dei nemici
enemies = []

# Lista dei proiettili sparati dalla navicella
player_bullets = []

# Lista dei proiettili sparati dai nemici
enemy_bullets = []

# Variabile per il numero massimo di nemici sullo schermo
max_enemy_count = 4

# Funzione per generare un nuovo nemico
def generate_enemy():
    x = random.randint(0, larghezza - 40)
    y = random.randint(50, 400)  # Altezza massima per evitare che i nemici si formino troppo in alto
    enemy = Enemy(x, y, quadrato_size)
    enemies.append(enemy)

# Funzione per generare nuovi nemici se ce ne sono meno del numero massimo
def generate_enemies_if_needed():
    if len(enemies) < max_enemy_count:
        generate_enemy()

# Loop principale
running = True
while running:
    # Gestione eventi
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Sparo di un proiettile quando si preme la barra spaziatrice
                bullet = PlayerBullet(player.x + player.size // 2, player.y, 5)
                player_bullets.append(bullet)
                shoot_sound.play()  # Riproduci l'effetto sonoro dello sparo

    # Movimento del giocatore
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.move(-velocita_giocatore)
    if keys[pygame.K_d]:
        player.move(velocita_giocatore)

    # Movimento dei nemici
    for enemy in enemies:
        enemy.move()
        if enemy.x <= 0 or enemy.x >= larghezza - enemy.size:  # Inverte la direzione quando raggiunge il bordo
            enemy.direction *= -1
        if enemy.shoot():
            bullet = EnemyBullet(enemy.x + enemy.size // 2, enemy.y + enemy.size, 5)
            enemy_bullets.append(bullet)
            shoot_sound.play()  # Riproduci l'effetto sonoro dello sparo

    # Controllo collisioni con i proiettili sparati dai nemici
    for bullet in enemy_bullets:
        if bullet.x < player.x + player.size and bullet.x + bullet.size > player.x and bullet.y < player.y + player.size and bullet.y + bullet.size > player.y:
            # Collisione con la navicella
            running = False  # Il gioco finisce

    # Controllo collisioni con i proiettili sparati dalla navicella
    for bullet in player_bullets:
        for enemy in enemies:
            if bullet.x < enemy.x + enemy.size and bullet.x + bullet.size > enemy.x and bullet.y < enemy.y + enemy.size and bullet.y + bullet.size > enemy.y:
                # Collisione con un nemico
                enemies.remove(enemy)
                punteggio += 1
                player_bullets.remove(bullet)
                death_sound.play()  # Riproduci l'effetto sonoro della morte del nemico

    # Movimento dei proiettili sparati dalla navicella
    for bullet in player_bullets:
        bullet.move()

    # Movimento dei proiettili sparati dai nemici
    for bullet in enemy_bullets:
        bullet.move()

    # Genera nuovi nemici se non ce ne sono più sullo schermo
    if len(enemies) == 0:
        for _ in range(max_enemy_count):
            generate_enemy()

    # Aggiornamento schermo
    fin.fill((0, 0, 0))
    player.draw(fin)
    for enemy in enemies:
        enemy.draw(fin)
    for bullet in player_bullets:
        bullet.draw(fin)
    for bullet in enemy_bullets:
        bullet.draw(fin)
    bianco = (255, 255, 255)
    # Visualizzazione punteggio
    text = font.render("Punteggio: " + str(punteggio), True, bianco)
    fin.blit(text, (10, 10))

    # Disegna il muro
    pygame.draw.rect(fin, (0, 0, 0), (muro_x, muro_y, muro_larghezza, muro_altezza))

    pygame.display.flip()

# Uscita dal programma
pygame.quit()
sys.exit()
