# socorrista_sequencial
class SocorristaSequencial:

    def __init__(self):
        self.posicao = (0, 0)
        self.passos = 0

    def receber_lista(self, lista):
        self.lista_resgates = list(lista)

    def calcular_distancia(self, destino):
        return abs(self.posicao[0] - destino[0]) + abs(self.posicao[1] - destino[1])

    def resgatar(self, cidade):
        for (x, y) in self.lista_resgates:
            self.passos += self.calcular_distancia((x, y))
            self.posicao = (x, y)
            if 'vitima' in cidade[x][y]:
                cidade[x][y].remove('vitima')
            print(f"[Sequencial] Resgatou vitima em ({x}, {y}) | total de passos: {self.passos}")

