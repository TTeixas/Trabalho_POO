import pygame
import random
from aa import *

pygame.init()
tela = pygame.display.set_mode((700, 700))
clock = pygame.time.Clock()
fonte = pygame.font.SysFont(None, 60)
antonio = Antonio()
bobao = Inimigo_um()
inimigos = [bobao]
spawner = inimigos
x, y = 300, 300
velocidade = 3
direcao = "right"
rodando = True
pausado = False

tempo_ultimo_spawn = 0
intervalo_spawn = 3000  # 3 segundos
max_inimigos = 10  # limite de inimigos na tela

def spawn_inimigo():
    lados = ["top", "bottom", "left", "right"]
    lado = random.choice(lados)

    if lado == "top":
        x_inimigo = random.randint(0, 760)
        y_inimigo = -40
    elif lado == "bottom":
        x_inimigo = random.randint(0, 760)
        y_inimigo = 600
    elif lado == "left":
        x_inimigo = -40
        y_inimigo = random.randint(0, 560)
    else:
        x_inimigo = 800
        y_inimigo = random.randint(0, 560)

    inimigo = Inimigo_um()
    inimigo.x = x_inimigo
    inimigo.y = y_inimigo
    inimigo.rect = pygame.Rect(inimigo.x, inimigo.y, 40, 40)
    return inimigo


while rodando:
    tempo_atual = pygame.time.get_ticks()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            rodando = False

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                pausado = not pausado   
       

    if pausado:
        texto = fonte.render("PAUSADO", True, (255, 255, 255))
        tela.blit(texto, (350, 250))
        pygame.display.update()
        clock.tick(60)
        continue  # IMPORTANTE! Pula toda lógica do jogo

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        x -= velocidade
        direcao = "left"
    elif teclas[pygame.K_RIGHT]:
        x += velocidade
        direcao = "right"
    elif teclas[pygame.K_UP]:
        y -= velocidade
    elif teclas[pygame.K_DOWN]:
        y += velocidade

    tela.fill((0, 0, 0))

    # ======= JOGADOR =======
    if antonio.vida_atual > 0:
        pygame.draw.rect(tela, (255, 255, 0), (x, y, 40, 40))
        antonio.desenhar_barra_vida(tela, x, y)
        antonio.rect = pygame.Rect(x, y, 40, 40)
    else:
    # Exemplo 1: Encerrar o jogo
        tela.fill((0,0,0))
        texto = fonte.render("GAME OVER", True, (255, 0, 0))
        tela.blit(texto, (300, 250))
        pygame.display.update()
        pygame.time.delay(3000)  # espera 3 segundos
        continue

        


    
    if tempo_atual - tempo_ultimo_spawn > intervalo_spawn and len(inimigos) < max_inimigos:
        inimigos.append(spawn_inimigo())
        tempo_ultimo_spawn = tempo_atual

        # Dificuldade progressiva: diminui intervalo de spawn
        if intervalo_spawn > 500:
            intervalo_spawn -= 50  



    # ======= INIMIGOS =======
    for inimigo in inimigos[:]:  # copia pra poder remover durante iteração
        inimigo.mover_para(x, y)
        inimigo.atacar(antonio, tempo_atual)

        # Se o inimigo ainda tiver vida, desenha
        if inimigo.vida_atual > 0:
            pygame.draw.rect(tela, inimigo.cor, inimigo.rect)
        else:
            print(f"{inimigo.nome} foi derrotado!")
            inimigos.remove(inimigo)  # remove o inimigo da lista

    # ======= ATAQUE DO PERSONAGEM =======
    for arma in antonio.armas:
        if isinstance(arma, Whip):
            arma.attack(tempo_atual, x, y, direcao, inimigos)
            arma.update(tempo_atual)
            arma.draw(tela)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
