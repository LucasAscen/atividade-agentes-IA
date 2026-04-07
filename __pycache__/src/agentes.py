import random
from src.ambiente import TAM


#  AGENTE REATIVO SIMPLESn - Drone

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
        """retorna o que está na célula atual, sem memória."""
        x, y = self.pos
        cel   = ambiente.grid[x][y]
        if cel == "F":
            return [("F", (x, y))]
        elif cel == "V":
            return [("V", (x, y))]
        return []


#  AGENTE REATIVO BASEADO EM MODELOS — Bombeiro

class Bombeiro:
    def __init__(self, quadrante):
        self.quadrante = quadrante
        self.ocupado   = False
        self.alvo      = None
        inicio = {
            "Q1": (1, 1), "Q2": (1, 5),
            "Q3": (5, 1), "Q4": (5, 5),
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

#  AGENTE BASEADO EM OBJETIVOS — Socorrista Sequencial
class SocorristaSequencial:
    def __init__(self):
        self.pos            = (0, 0)
        self.lista          = []          # fila FIFO
        self.alvo_atual     = None
        self.passos         = 0
        self.distancia_total = 0
        self.resgates       = 0

    def receber_lista(self, novas):
        for v in novas:
            if v != self.alvo_atual and v not in self.lista:
                self.lista.append(v)

    def agir(self, ambiente):
        if not self.alvo_atual and self.lista:
            self.alvo_atual = self.lista.pop(0)
        if not self.alvo_atual:
            return None

        x, y   = self.alvo_atual
        px, py = self.pos
        if px != x:
            px += 1 if x > px else -1
        elif py != y:
            py += 1 if y > py else -1
        self.passos          += 1
        self.distancia_total += 1
        self.pos = (px, py)

        if self.pos == (x, y):
            salvou          = ambiente.salvar_vitima(x, y)
            self.alvo_atual = None
            if salvou:
                self.resgates += 1
                return ("salvou", (x, y))
        return None


#  AGENTE BASEADO EM UTILIDADE

class SocorristaInteligente:
    def __init__(self):
        self.pos             = (TAM - 1, TAM - 1)
        self.lista           = []
        self.alvo_atual      = None
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

        x, y   = self.alvo_atual
        px, py = self.pos
        if px != x:
            px += 1 if x > px else -1
        elif py != y:
            py += 1 if y > py else -1
        self.passos          += 1
        self.distancia_total += 1
        self.pos = (px, py)

        if self.pos == (x, y):
            salvou          = ambiente.salvar_vitima(x, y)
            self.alvo_atual = None
            if salvou:
                self.resgates += 1
                return ("salvou", (x, y))
        return None
