from abc import ABC, abstractmethod
from typing import List

# =========================
# CLASSE BASE: ARMA
# =========================
class Arma(ABC):
    def __init__(self, nome: str, dano: float):
        self.nome = nome
        self.dano = dano

    @abstractmethod
    def attack(self) -> None:
        """Define como a arma ataca — deve ser implementado pelas subclasses."""
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
        """Aplica o bônus deste item ao personagem."""
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
        self.defesa = 0
        self.move_speed = 1.0  # 100%
        self.armas: List[Arma] = []
        self.itens: List[Item] = []
        
    def add_arma(self, a: Arma) -> None:
        self.armas.append(a)
        
    def add_item(self, i: Item) -> None:
        self.itens.append(i)
        i.aplicar_bonus(self)
        
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
    poderes: List[Poder]

    def __init__(self, nome: str):
        self.nome = nome
        self.vida_maxima = 150
        self.defesa = 10
        self.move_speed = 1.0  # 100%
    
    def add_poder (self, p: Poder):
        self.poderes.append(p)

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
        self.add_poder()
        
 

   

# =========================
# PERSONAGENS ESPECÍFICOS
# =========================
class Antonio(Personagem):
    def __init__(self):
        super().__init__("Antonio")
        self.add_arma(Whip()) #Todo personagem começa com 1 arma basica 
        self.bonus_passivo()

    def bonus_passivo(self) -> None:
        """Antonio começa com +20 HP e +1 de Defesa."""
        self.vida_maxima += 20
        self.defesa += 1


# =========================
# ARMAS ESPECÍFICAS
# =========================
class Whip(Arma):
    def __init__(self):
        super().__init__("Whip", 10)

    def attack(self) -> None:
        print("Você chicoteia os inimigos à sua frente!")


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
    
    
    
    
    print(antonio)