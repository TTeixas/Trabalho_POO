from abc import ABC, abstractmethod
from typing import List
import pygame

# =========================
# CLASSE BASE: ARMA
# =========================
class Arma(ABC):
    def __init__(self, nome: str, dano: float):
        self.nome = nome
        self.dano = dano

    @abstractmethod
    def attack(self) -> None:
        pass

    def __str__(self) -> str:
        return f"{self.nome} (Dano: {self.dano})"


# =========================
# CLASSE BASE: PODER
# =========================
class Poder(ABC):
    def __init__(self, nome: str, dano: float):
        self.nome = nome
        self.dano = dano
    
    @abstractmethod
    def lancar(self, alvo) -> None:
        pass

    def __str__(self):
        return f"{self.nome} (Dano: {self.dano})"


# =========================
# CLASSE BASE: ITEM
# =========================
class Item(ABC):
    def __init__(self, nome: str):
        self.nome = nome

    @abstractmethod
    def aplicar_bonus(self, personagem) -> None:
        pass

    def __str__(self) -> str:
        return self.nome


# =========================
# CLASSE BASE: PERSONAGEM
# =========================
class Personagem(ABC):
    def __init__(self, nome: str):
        self.nome = nome
        self.vida_maxima = 100
        self.vida_atual = self.vida_maxima
        self.defesa = 0
        self.move_speed = 1.0
        self.armas: List[Arma] = []
        self.itens: List[Item] = []
        self.rect = pygame.Rect(0, 0, 40, 40)

    def add_arma(self, a: Arma) -> None:
        self.armas.append(a)
        
    def add_item(self, i: Item) -> None:
        self.itens.append(i)
        i.aplicar_bonus(self)
    
    def desenhar_barra_vida(self, tela, x, y):
        barra_x = x
        barra_y = y - 10
        largura_total = 40
        altura = 5
        proporcao = self.vida_atual / self.vida_maxima
        largura_atual = int(largura_total * proporcao)

        # Fundo vermelho
        pygame.draw.rect(tela, (150, 0, 0), (barra_x, barra_y, largura_total, altura))
        # Vida verde
        pygame.draw.rect(tela, (0, 255, 0), (barra_x, barra_y, largura_atual, altura))
        # Contorno branco
        pygame.draw.rect(tela, (255, 255, 255), (barra_x-1, barra_y-1, largura_total+2, altura+2), 1)

    @abstractmethod
    def bonus_passivo(self) -> None:
        pass

    def __str__(self) -> str:
        txt = f"Personagem: {self.nome}\n"
        txt += f"HP Máximo: {self.vida_maxima:.2f}\n"
        txt += f"Defesa: {self.defesa:.2f}\n"
        txt += f"Velocidade: {self.move_speed:.2f}\n"

        if self.armas:
            txt += "Armas:\n"
            for arma in self.armas:
                txt += f"  - {arma}\n"
        else:
            txt += "Armas: Nenhuma\n"

        if self.itens:
            txt += "Itens:\n"
            for item in self.itens:
                txt += f"  - {item}\n"
        else:
            txt += "Itens: Nenhum\n"

        return txt


# =========================
# CLASSE BASE: INIMIGO
# =========================
class Inimigo(ABC):
    def __init__(self, nome: str):
        self.nome = nome
        self.vida_maxima = 150
        self.vida_atual = self.vida_maxima
        self.defesa = 10
        self.move_speed = 0.5
        self.x = 100
        self.y = 100
        self.tamanho = 40
        self.dano = 5
        self.cooldown_dano = 1000
        self.ultimo_dano = 0
        self.rect = pygame.Rect(self.x, self.y, 50, 50)

    def mover_para(self, alvo_x, alvo_y):
        if self.x < alvo_x:
            self.x += self.move_speed
        elif self.x > alvo_x:
            self.x -= self.move_speed
        if self.y < alvo_y:
            self.y += self.move_speed
        elif self.y > alvo_y:
            self.y -= self.move_speed
        self.rect.topleft = (self.x, self.y)

    def atacar(self, personagem: Personagem, tempo_atual):
        if self.rect.colliderect(personagem.rect):
            if tempo_atual - self.ultimo_dano >= self.cooldown_dano:
                personagem.vida_atual = max(0, personagem.vida_atual - self.dano)
                self.ultimo_dano = tempo_atual
                print(f"{self.nome} causou {self.dano} de dano! Vida atual: {personagem.vida_atual}")

    def __str__(self) -> str:
        txt = f"Inimigo: {self.nome}\n"
        txt += f"HP Máximo: {self.vida_maxima:.2f}\n"
        txt += f"Defesa: {self.defesa:.2f}\n"
        txt += f"Velocidade: {self.move_speed:.2f}\n"
        return txt


# =========================
# INIMIGOS ESPECÍFICOS
# =========================
class Inimigo_um(Inimigo):
    def __init__(self):
        super().__init__("Inimigo_um")
        self.cor = (255, 0, 0)


# =========================
# PERSONAGENS ESPECÍFICOS
# =========================
class Antonio(Personagem):
    def __init__(self):
        super().__init__("Antonio")
        self.add_arma(Whip())
        self.bonus_passivo()

    def bonus_passivo(self) -> None:
        self.vida_maxima += 20
        self.vida_atual = self.vida_maxima
        self.defesa += 1


# =========================
# ARMAS ESPECÍFICAS
# =========================
class Whip(Arma):
    def __init__(self):
        super().__init__("Whip", 10)
        self.cooldown = 1000
        self.duracao = 200
        self.ultimo_ataque = 0
        self.ativo = False
        self.cor = (255, 255, 255)
        self.largura = 60
        self.altura = 15
        self.rect = None

    def attack(self, tempo_atual, x, y, direcao, inimigos: List[Inimigo]):
        if not self.ativo and tempo_atual - self.ultimo_ataque >= self.cooldown:
            self.ativo = True
            self.tempo_inicio = tempo_atual
            self.ultimo_ataque = tempo_atual
            if direcao == "right":
                self.rect = pygame.Rect(x + 40, y + 10, self.largura, self.altura)
            else:
                self.rect = pygame.Rect(x - self.largura, y + 10, self.largura, self.altura)

        if self.ativo and self.rect:
            for inimigo in inimigos:
                if inimigo.vida_atual > 0 and self.rect.colliderect(inimigo.rect):
                    dano_final = max(0, self.dano - inimigo.defesa * 0.2)
                    inimigo.vida_atual = max(0, inimigo.vida_atual - dano_final)

    def update(self, tempo_atual):
        if self.ativo and tempo_atual - self.tempo_inicio >= self.duracao:
            self.ativo = False

    def draw(self, tela):
        if self.ativo and self.rect:
            pygame.draw.rect(tela, self.cor, self.rect)


# =========================
# OUTRAS ARMAS, ITENS E PODERES
# =========================
class MagicWand(Arma):
    def __init__(self):
        super().__init__("Magic Wand", 10)

    def attack(self):
        print("Projétil mágico disparado!")


class Knife(Arma):
    def __init__(self):
        super().__init__("Knife", 6.5)

    def attack(self):
        print("Faca lançada!")


class Armor(Item):
    def __init__(self):
        super().__init__("Armor")

    def aplicar_bonus(self, P: Personagem):
        P.defesa += 1


class HollowHeart(Item):
    def __init__(self):
        super().__init__("Hollow Heart")

    def aplicar_bonus(self, P: Personagem):
        P.vida_maxima += 20


class Magia(Poder):
    def __init__(self):
        super().__init__("Magia de Fogo", 10)

    def lancar(self, alvo: Inimigo):
        # exemplo de efeito
        alvo.vida_atual -= 10
