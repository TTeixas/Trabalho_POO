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
        #Define como a arma ataca — deve ser implementado pelas subclasses.
        pass

    def __str__(self) -> str:
        return f"{self.nome} (Dano: {self.dano})"

# =========================
# CLASSE BASE: PODERES
# =========================

class Poder(ABC):
    def __init__(self, nome: str, dano: float):
        self.nome = nome
        self.dano = dano
    
    @abstractmethod
    def Poder(self):
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
        #Aplica o bônus deste item ao personagem.
        pass

    def __str__(self) -> str:
        return f"{self.nome}"


# =========================
# CLASSE BASE: PERSONAGEM
# =========================
class Personagem(ABC):
    nome: str
    vida_maxima: float
    defesa: float
    move_speed: float
    armas: List[Arma]
    itens: List[Item]

    def __init__(self, nome: str):
        self.nome = nome
        self.vida_maxima = 100
        self.vida_atual = self.vida_maxima
        self.defesa = 0
        self.move_speed = 1.0  # 100%
        self.armas: List[Arma] = []
        self.itens: List[Item] = []
        
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

        # Fundo (vermelho)
        pygame.draw.rect(tela, (150, 0, 0), (barra_x, barra_y, largura_total, altura))
        # Vida atual (verde)
        pygame.draw.rect(tela, (0, 255, 0), (barra_x, barra_y, largura_atual, altura))
        # Contorno
        pygame.draw.rect(tela, (255, 255, 255), (barra_x - 1, barra_y - 1, largura_total + 2, altura + 2), 1)
        
    @abstractmethod
    def bonus_passivo(self) -> None:
        pass
    
    def __str__(self) -> str:
        txt = f"Personagem: {self.nome}\n"
        txt += f"HP Máximo: {self.vida_maxima:.2f}\n"
        txt += f"Defesa: {self.defesa:.2f}\n"
        txt += f"Velocidade de Movimento: {self.move_speed:.2f}\n"

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
    nome: str
    vida_maxima: float
    defesa: float
    move_speed: float
    

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
        self.cooldown_dano = 1000  # 1 segundo entre danos
        self.ultimo_dano = 0
        self.rect = pygame.Rect(self.x, self.y, 50, 50)

    
    def mover_para(self, alvo_x, alvo_y):
        #Movimenta o inimigo lentamente em direção ao jogador
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
    # Causa dano se estiver colidindo e cooldown já passou
        if self.rect.colliderect(personagem.rect):
            if tempo_atual - self.ultimo_dano >= self.cooldown_dano:
                personagem.vida_atual = max(0, personagem.vida_atual - self.dano)
                self.ultimo_dano = tempo_atual
                print(f"{self.nome} causou {self.dano} de dano! Vida atual do personagem: {personagem.vida_atual}")



    def __str__(self) -> str:
        txt = f"Inimigo: {self.nome}\n"
        txt += f"HP Máximo: {self.vida_maxima:.2f}\n"
        txt += f"Defesa: {self.defesa:.2f}\n"
        txt += f"Velocidade de Movimento: {self.move_speed:.2f}\n"

        return txt

# =========================
# INIMIGOS ESPECÍFICOS
# =========================

class Inimigo_um(Inimigo):
    def __init__(self):
        super().__init__("Inimigo_um")
        self.cor = (255, 0, 0)  # vermelho

        
        
 

   

# =========================
# PERSONAGENS ESPECÍFICOS
# =========================
class Antonio(Personagem):
    def __init__(self):
        super().__init__("Antonio")
        self.add_arma(Whip())  # arma inicial
        self.bonus_passivo()

    def bonus_passivo(self) -> None:
        #Antonio começa com +20 HP e +1 de Defesa.
        self.vida_maxima += 20
        self.vida_atual = self.vida_maxima  # vida cheia ao aplicar o bônus
        self.defesa += 1



# =========================
# ARMAS ESPECÍFICAS
# =========================
class Whip(Arma):
    def __init__(self):
        super().__init__("Whip", 10)
        self.cooldown = 1000      # tempo entre ataques (ms)
        self.duracao = 200        # tempo que o ataque fica ativo (ms)
        self.ultimo_ataque = 0
        self.ativo = False
        self.cor = (255, 255, 255)
        self.largura = 60
        self.altura = 15
        self.rect = None
        self.lado_direita = True  # alterna o lado do ataque

    def attack(self, tempo_atual, x, y,direcao, inimigos : Inimigo):
        #Ativa o chicote se o cooldown acabou.
        if not self.ativo and tempo_atual - self.ultimo_ataque >= self.cooldown:
            self.ativo = True
            self.tempo_inicio = tempo_atual
            self.ultimo_ataque = tempo_atual

            if direcao == "right":
                self.rect = pygame.Rect(x + 40, y + 10, self.largura, self.altura)
            elif direcao == "left":
                self.rect = pygame.Rect(x - self.largura, y + 10, self.largura, self.altura)

        for inimigo in inimigos:
            if self.rect.colliderect(inimigo.rect):
                dano_final = max(0, self.dano - inimigo.defesa * 0.2)
                inimigo.vida_atual = max(0, inimigo.vida_atual - dano_final)
                print(f"{inimigo.nome} levou {dano_final:.1f} de dano! Vida restante: {inimigo.vida_atual:.1f}")

    def update(self, tempo_atual):
        #Desativa o chicote após o tempo de duração acabar.
        if self.ativo and tempo_atual - self.tempo_inicio >= self.duracao:
            self.ativo = False

    def draw(self, tela):
        #Desenha o retângulo se estiver ativo.
        if self.ativo and self.rect:
            pygame.draw.rect(tela, self.cor, self.rect)



class MagicWand(Arma):
    def __init__(self):
        super().__init__("Magic Wand", 10)

    def attack(self):
        print("A varinha dispara um projétil mágico que persegue inimigos!")


class Knife(Arma):
    def __init__(self):
        super().__init__("Knife", 6.5)

    def attack(self) -> None:
        print("Você lança uma faca em linha reta!")
        

# =========================
# ITENS ESPECÍFICOS
# =========================
class Armor(Item):
    def __init__(self):
        super().__init__("Armor")

    def aplicar_bonus(self, P : Personagem) -> None:
        P.defesa += 1

    def __str__(self) -> str:
        return f"{self.nome}"


class Hollow_heart(Item):
    def __init__(self):
        super().__init__("Hollow_heart")

    def aplicar_bonus(self, P : Personagem):
        P.vida_maxima += 20

    def __str__(self) -> str:
        return f"{self.nome}"

# =========================
# PODERES ESPECÍFICOS
# =========================

class Magia(Poder):
    def __init__(self):
        super().__init__("Magia de Fogo")
    
    def lancar_magia (self, i: Inimigo):
        i.add_poder += 10

    def __str__(self):
        return f"{self.nome}"



# =========================
# EXEMPLO DE USO
# =========================
if __name__ == '__main__':
    antonio = Antonio()
    varinha = MagicWand()
    faca = Knife()
    
    antonio.add_arma(varinha)
    antonio.add_arma(faca)
    
    
    defesa = Armor()
    vida = Hollow_heart()
    
    antonio.add_item(defesa)
    antonio.add_item(vida)
    
## TESTEEE OIOIOIOI NAOSEIMEXERNISSO    
    
    
    print(antonio)
