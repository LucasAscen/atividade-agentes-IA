import random

TAM = 8

# Hospital fixo no centro do mapa
HOSPITAL = (3, 3)

QUADRANTES = {
    "Q1": [(x, y) for x in range(0, 4) for y in range(0, 4)],
    "Q2": [(x, y) for x in range(0, 4) for y in range(4, 8)],
    "Q3": [(x, y) for x in range(4, 8) for y in range(0, 4)],
    "Q4": [(x, y) for x in range(4, 8) for y in range(4, 8)],
}

def get_quadrante(x, y):
    for q, celulas in QUADRANTES.items():
        if (x, y) in celulas:
            return q
    return None


class Ambiente:
    def __init__(self):
        self.grid = [["." for _ in range(TAM)] for _ in range(TAM)]
        hx, hy = HOSPITAL
        self.grid[hx][hy] = "H"

    def gerar_evento(self):
        x = random.randint(0, TAM - 1)
        y = random.randint(0, TAM - 1)
        if self.grid[x][y] == ".":
            self.grid[x][y] = random.choice(["F", "V"])

    def apagar_fogo(self, x, y):
        if self.grid[x][y] == "F":
            self.grid[x][y] = "."
            return True
        return False

    def salvar_vitima(self, x, y):
        if self.grid[x][y] == "V":
            self.grid[x][y] = "."
            return True
        return False
