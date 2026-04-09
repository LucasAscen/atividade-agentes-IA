import random
from src.ambiente import TAM, HOSPITAL


# AGENTE REATIVO SIMPLES — Drone
class Drone:
    def __init__(self, drone_id):
        self.id  = drone_id
        self.pos = (random.randint(0, TAM - 1), random.randint(0, TAM - 1))

    def mover(self):
        dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        nx = max(0, min(TAM - 1, self.pos[0] + dx))
        ny = max(0, min(TAM - 1, self.pos[1] + dy))
        self.pos = (nx, ny)

    def observar(self, ambiente):
        x, y = self.pos
        cel   = ambiente.grid[x][y]
        if cel == "F":
            return [("F", (x, y))]
        elif cel == "V":
            return [("V", (x, y))]
        return []


# AGENTE REATIVO BASEADO EM MODELOS — Bombeiro
class Bombeiro:
    def __init__(self, quadrante):
        self.quadrante = quadrante
        self.ocupado   = False
        self.alvo      = None
        inicio = {
            "Q1": (0, 0),      
            "Q2": (0, TAM - 1), 
            "Q3": (TAM - 1, 0), 
            "Q4": (TAM - 1, TAM - 1), 
        }
        self.pos = inicio[quadrante]

    def receber_despacho(self, coordenada):
        self.alvo    = coordenada
        self.ocupado = True

    def agir(self, ambiente):
        if not self.alvo:
            return None
        x, y   = self.alvo
        px, py = self.pos
        if px != x:
            px += 1 if x > px else -1
        elif py != y:
            py += 1 if y > py else -1
        self.pos = (px, py)
        if self.pos == (x, y):
            apagou       = ambiente.apagar_fogo(x, y)
            self.alvo    = None
            self.ocupado = False
            if apagou:
                return ("apagou", (x, y))
        return None


def _mover_em_direcao(pos, alvo):
    px, py = pos
    x, y   = alvo
    if px != x:
        px += 1 if x > px else -1
    elif py != y:
        py += 1 if y > py else -1
    return (px, py)


# AGENTE BASEADO EM OBJETIVOS — Socorrista Sequencial (FIFO)
class SocorristaSequencial:
    def __init__(self):
        self.pos             = (0, 0)
        self.lista           = []
        self.alvo_atual      = None
        self.indo_hospital   = False
        self.passos          = 0
        self.distancia_total = 0
        self.resgates        = 0

    def receber_lista(self, novas):
        for v in novas:
            if v != self.alvo_atual and v not in self.lista:
                self.lista.append(v)

    def agir(self, ambiente):
        if self.indo_hospital:
            self.pos = _mover_em_direcao(self.pos, HOSPITAL)
            self.passos          += 1
            self.distancia_total += 1
            if self.pos == HOSPITAL:
                self.indo_hospital = False
                self.resgates += 1
                return ("resgatou", self.alvo_atual)
            return None

        if not self.alvo_atual and self.lista:
            self.alvo_atual = self.lista.pop(0)

        if not self.alvo_atual:
            return None

        self.pos = _mover_em_direcao(self.pos, self.alvo_atual)
        self.passos          += 1
        self.distancia_total += 1

        if self.pos == self.alvo_atual:
            salvou = ambiente.salvar_vitima(*self.alvo_atual)
            if salvou:
                self.indo_hospital = True
            else:
                self.alvo_atual = None
        return None


# AGENTE BASEADO EM UTILIDADE — Socorrista Otimizador
class SocorristaInteligente:
    def __init__(self):
        self.pos             = (TAM - 1, TAM - 1)
        self.lista           = []
        self.alvo_atual      = None
        self.indo_hospital   = False
        self.passos          = 0
        self.distancia_total = 0
        self.resgates        = 0

    def receber_lista(self, novas):
        for v in novas:
            if v != self.alvo_atual and v not in self.lista:
                self.lista.append(v)

    def _dist(self, v):
        return abs(v[0] - self.pos[0]) + abs(v[1] - self.pos[1])

    def _mais_proxima(self):
        return min(self.lista, key=self._dist)

    def agir(self, ambiente):
        if self.indo_hospital:
            self.pos = _mover_em_direcao(self.pos, HOSPITAL)
            self.passos          += 1
            self.distancia_total += 1
            if self.pos == HOSPITAL:
                self.indo_hospital = False
                self.resgates += 1
                return ("resgatou", self.alvo_atual)
            return None

        if self.lista:
            melhor = self._mais_proxima()
            if self.alvo_atual is None:
                self.alvo_atual = melhor
                self.lista.remove(melhor)
            elif self._dist(melhor) < self._dist(self.alvo_atual):
                self.lista.append(self.alvo_atual)
                self.lista.remove(melhor)
                self.alvo_atual = melhor

        if not self.alvo_atual:
            return None

        self.pos = _mover_em_direcao(self.pos, self.alvo_atual)
        self.passos          += 1
        self.distancia_total += 1

        if self.pos == self.alvo_atual:
            salvou = ambiente.salvar_vitima(*self.alvo_atual)
            if salvou:
                self.indo_hospital = True
            else:
                self.alvo_atual = None
        return None