class Bombeiros:

    def __init__(self, posicao, quadrante):
        self.posicao = posicao
        self.quadrante = quadrante
        self.destino = None #tentativa de fazer o bombeiro se mover ao inves de teletransportar

    def se_mover(self,x,y,cidade):
        self.posicao = (x,y) #atualiza a posicao do bombeiro

        if "fogo" in cidade[x][y]:
            cidade[x][y].remove("fogo") #remove o fogo da cidade
            print(f"apagado por bombeiro na coordenada ({x}, {y})")

        else:
            print(f"bombeiro se moveu para a coordenada ({x}, {y}), mas nao encontrou fogo")

    def atualizar(self, cidade): #atualiza a posicao do bombeiro em direção ao destino, é só um teste

        if self.destino:
            dx, dy = self.destino

            x, y = self.posicao

            if x < dx:
                x += 1
            elif x > dx:
                x -= 1
            elif y < dy:
                y += 1
            elif y > dy:
                y -= 1

            self.posicao = (x, y)

            # chegou no destino
            if self.posicao == self.destino:
                if "fogo" in cidade[x][y]:
                    cidade[x][y].remove("fogo")
                    print(f"Bombeiro apagou fogo em {self.posicao}")

                self.destino = None