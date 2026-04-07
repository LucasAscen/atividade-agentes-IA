# socorrista_sequencial
class SocorristaSequencial:

    def __init__(self):
        self.posicao = (0, 0)
        self.passos = 0

    def receber_lista(self, lista):
        self.lista_resgates = list(lista)

    def calcular_distancia(self, destino):
        return abs(self.posicao[0] - destino[0]) + abs(self.posicao[1] - destino[1])

    def resgatar(self, cidade, hospital):

        for destino in self.lista_resgates:

            # ir até a vítima
            while self.posicao != destino:
                x, y = self.posicao
                dx, dy = destino

                if x < dx:
                    x += 1
                elif x > dx:
                    x -= 1

                if y < dy:
                    y += 1
                elif y > dy:
                    y -= 1

                self.posicao = (x, y)
                self.passos += 1

            # chegou na vítima
            x, y = self.posicao
            if 'vitima' in cidade[x][y]:
                cidade[x][y].remove('vitima')
                print(f"[Sequencial] Pegou vítima em {self.posicao}")

        # 🔥 AGORA vai ao hospital só UMA VEZ no final
        while self.posicao != hospital:
            x, y = self.posicao
            hx, hy = hospital

            if x < hx:
                x += 1
            elif x > hx:
                x -= 1

            if y < hy:
                y += 1
            elif y > hy:
                y -= 1

            self.posicao = (x, y)
            self.passos += 1

        print(f"[Sequencial] Entregou todas no hospital | passos: {self.passos}")