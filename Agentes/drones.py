import random

class Drone:
    def __init__(self, tamanho):
        self.x = random.randint(0, tamanho - 1)
        self.y = random.randint(0, tamanho - 1)
        self.tamanho = tamanho

    def mover(self):
        direcoes = [(1,0), (-1,0), (0,1), (0,-1)]
        dx, dy = random.choice(direcoes)

        novo_x = self.x + dx
        novo_y = self.y + dy

        if 0 <= novo_x < self.tamanho:
            self.x = novo_x
        if 0 <= novo_y < self.tamanho:
            self.y = novo_y


    def observar(self, cidade, bdi):
        celula = cidade[self.x][self.y]

        if 'fogo' in celula and (self.x, self.y) not in bdi.fogos:
                print(f"Drone detectou fogo em ({self.x}, {self.y})")
                bdi.receber_fogo(self.x, self.y)#afim de evitar que o drone envie a mesma informação várias vezes, ele só envia se a coordenada ainda não estiver na lista de fogos do BDI

        if 'vitima' in celula and (self.x, self.y) not in bdi.vitimas:
                print(f"Drone detectou vítima em ({self.x}, {self.y})")
                bdi.receber_vitima(self.x, self.y)