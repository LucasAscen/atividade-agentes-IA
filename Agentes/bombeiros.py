from Agentes.drones import observar_drone
from Cidade import cidade, gerar_evento

class Bombeiros:

    def __init__(self, posicao, quadrante):
        self.posicao = posicao
        self.quadrante = quadrante
        

    def se_mover(self,x,y,cidade):
        self.posicao = (x,y) #atualiza a posicao do bombeiro

        if "fogo" in cidade[x][y]:
            cidade[x][y].remove("fogo") #remove o fogo da cidade
            print(f"apagado por bombeiro na coordenada ({x}, {y})")

        else:
            print(f"bombeiro se moveu para a coordenada ({x}, {y}), mas nao encontrou fogo")

