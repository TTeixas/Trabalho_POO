import pygame
import random
from main import *

pygame.init()
tela = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
fonte = pygame.font.SysFont(None, 60)

antonio = Antonio()
x, y = 300, 300
velocidade = 3
direcao = "right"

inimigos = []  # lista começa vazia
estado = "menu"

# ARMA
varinha = MagicWand()
adagas = Knife()
antonio.add_arma(varinha)
antonio.add_arma(adagas)

# SPAWN
tempo_ultimo_spawn = 0
intervalo_spawn = 3000
max_inimigos = 10

# tipos e pesos (mantive seu valor)
tipos_de_inimigos = [Inimigo_um, Goblin, Gigante]
pesos_inimigos = [50, 50, 100]


def resetar_jogo():
    global inimigos, x, y, intervalo_spawn, tempo_ultimo_spawn

    inimigos = []
    x, y = 300, 300
    antonio.vida_atual = antonio.vida_maxima

    intervalo_spawn = 3000
    tempo_ultimo_spawn = pygame.time.get_ticks()


# CONTROLE DE TELAS
def estados_do_jogo():
    if estado == "menu":
        tela_menu()
    elif estado == "jogando":
        atualizar_jogo()
    elif estado == "pausado":
        tela_pause()
    elif estado == "gameover":
        tela_gameover()

# FUNÇÕES DE TELAS
def tela_menu():
    tela.fill((0, 0, 0))
    titulo = fonte.render("POO game", True, (255, 255, 255))
    opc1 = fonte.render("1 - Iniciar Jogo", True, (200, 200, 200))
    opc2 = fonte.render("2 - Sair", True, (200, 200, 200))

    tela.blit(titulo, (280, 150))
    tela.blit(opc1, (250, 250))
    tela.blit(opc2, (250, 350))


def tela_pause():
    tela.fill((0, 0, 0))
    texto = fonte.render("PAUSADO", True, (255, 255, 255))
    tela.blit(texto, (300, 250))


def tela_gameover():
    tela.fill((0, 0, 0))
    texto = fonte.render("GAME OVER", True, (255, 0, 0))
    opc1 = fonte.render("1 - Voltar ao menu", True, (200, 200, 200))
    tela.blit(texto, (260, 250))
    tela.blit(opc1, (260, 350))


# FUNÇÃO DE SPAWN
tipos_de_inimigos = [Inimigo_um, Goblin, Gigante]
pesos_inimigos = [50, 30, 20]

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

    classe_inimigo = random.choices(
        tipos_de_inimigos,
        weights=pesos_inimigos,
        k=1
    )[0]

    inimigo = classe_inimigo()

    
    largura = getattr(inimigo, "largura", getattr(inimigo, "tamanho", 40))
    altura = getattr(inimigo, "altura", getattr(inimigo, "tamanho", 40))

    inimigo.x = x_inimigo
    inimigo.y = y_inimigo
    inimigo.rect = pygame.Rect(inimigo.x, inimigo.y, largura, altura)
    return inimigo



# JOGO

def atualizar_jogo():
    global x, y, direcao, tempo_ultimo_spawn, intervalo_spawn, estado

    tela.fill((0, 0, 0))
    tempo_atual = pygame.time.get_ticks()

    


    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        x -= velocidade
        direcao = "left"
    if teclas[pygame.K_RIGHT]:
        x += velocidade
        direcao = "right"
    if teclas[pygame.K_UP]:
        y -= velocidade
    if teclas[pygame.K_DOWN]:
        y += velocidade

    
    if antonio.vida_atual > 0:
        pygame.draw.rect(tela, (255, 255, 0), (x, y, 40, 40))
        antonio.desenhar_barra_vida(tela, x, y)
        antonio.rect = pygame.Rect(x, y, 40, 40)
    else:
        estado = "gameover"
        return

    
    if tempo_atual - tempo_ultimo_spawn > intervalo_spawn and len(inimigos) < max_inimigos:
        inimigos.append(spawn_inimigo())
        tempo_ultimo_spawn = tempo_atual
        if intervalo_spawn > 500:
            intervalo_spawn -= 200

    
    for inimigo in inimigos[:]:
        # mover_para deve alterar inimigo.x / inimigo.y
        inimigo.mover_para(x, y)

        # GARANTIR QUE O RECT ACOMPANHA A POSIÇÃO (caso a classe não faça)
        try:
            inimigo.rect.topleft = (int(inimigo.x), int(inimigo.y))
        except Exception:
            # caso não exista rect (proteção), criar um
            largura = getattr(inimigo, "largura", getattr(inimigo, "tamanho", 40))
            altura = getattr(inimigo, "altura", getattr(inimigo, "tamanho", 40))
            inimigo.rect = pygame.Rect(int(inimigo.x), int(inimigo.y), largura, altura)

        inimigo.atacar(antonio, tempo_atual)

        if inimigo.vida_atual > 0:
            pygame.draw.rect(tela, inimigo.cor, inimigo.rect)
        else:
            print(f"{inimigo.nome} foi derrotado!")
            inimigos.remove(inimigo)


    for arma in antonio.armas:
        if isinstance(arma, Whip):
            arma.attack(tempo_atual, x, y, direcao, inimigos)
            arma.update(tempo_atual)
            arma.draw(tela)
            
        elif isinstance(arma, MagicWand):
            if inimigos:
                alvo = inimigos[0]
                arma.attack(x, y, alvo.x, alvo.y)
            arma.atualizar(inimigos)
            arma.draw(tela)
            
            
        elif isinstance(arma, Knife):
            arma.attack(x, y)
            arma.atualizar(inimigos)
            arma.draw(tela)    
            
# LOOP PRINCIPAL

rodando = True
while rodando:

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            rodando = False

        if e.type == pygame.KEYDOWN:

            if estado == "menu":
                if e.key == pygame.K_1:
                    resetar_jogo()
                    estado = "jogando"
                elif e.key == pygame.K_2:
                    rodando = False

            elif estado == "jogando" and e.key == pygame.K_ESCAPE:
                estado = "pausado"

            elif estado == "pausado" and e.key == pygame.K_ESCAPE:
                estado = "jogando"

            elif estado == "gameover":
                if e.key == pygame.K_1:
                    resetar_jogo()
                    estado = "menu"


    estados_do_jogo()
    pygame.display.update()
    clock.tick(60)

pygame.quit()
