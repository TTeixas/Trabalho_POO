import pygame

pygame.init()
tela = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Meu primeiro jogo em Python")

x, y = 100, 100
velocidade = 0.30
rodando = True

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        x -= velocidade
    if teclas[pygame.K_RIGHT]:
        x += velocidade
    if teclas[pygame.K_UP]:
        y -= velocidade
    if teclas[pygame.K_DOWN]:
        y += velocidade

    tela.fill((0, 0, 0))
    pygame.draw.rect(tela, (255, 0, 0), (x, y, 50, 50))
    pygame.display.update()

pygame.quit()
