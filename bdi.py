#aqui sera o cerebro de todos os agentes 
from Agentes.drones import observar_drone
from Cidade import cidade, gerar_evento
from Agentes.bombeiros import Bombeiros

class BDI:

    
    def __init__(self):
        self.fogos = set()
        self.vitimas = set()
        self.b1 = Bombeiros((0,0), "Q1")
        self.b2 = Bombeiros((0,7), "Q2")
        self.b3 = Bombeiros((7,0), "Q3")
        self.b4 = Bombeiros((7,7), "Q4")

    def receber_fogo(self, x, y):
        celula_fogos = (x, y)
        self.fogos.add(celula_fogos)
        print(f'Fogo detectado na coordenada: {celula_fogos}')

    def receber_vitima(self, x, y):
        celula_vitimas = (x, y)
        self.vitimas.add(celula_vitimas)
        print(f'Vitima detectada na coordenada: {celula_vitimas}')
        # adicionar no set
        
    def descobrir_quadrante(self,x,y):
        if x < 4 and y <4:
            return 'Quadrante 1'
        elif x < 4 and y >= 4:
            return 'Quadrante 2'
        elif x >= 4 and y < 4:
            return 'Quadrante 3'
        else:
            return 'Quadrante 4'
        
    def decidir_acoes(self):
        for (x,y) in self.fogos:
            quadrante = self.descobrir_quadrante(x,y)
            print(f'Fogo no {quadrante} - Enviar equipe de combate a incêndio')
           
            if quadrante == 'Quadrante 1':
                self.b1.se_mover(x,y,cidade)
            elif quadrante == 'Quadrante 2':
                self.b2.se_mover(x,y,cidade)  
            elif quadrante == 'Quadrante 3':
                self.b3.se_mover(x,y,cidade)
            else:
                self.b4.se_mover(x,y,cidade)
        for (x,y) in self.vitimas:
            quadrante = self.descobrir_quadrante(x,y)
            print(f'Vitima no {quadrante} - Enviar equipe de resgate')

        

    def apagar_fogo(self, x,y):
        if (x,y) in self.fogos:
            self.fogos.remove((x,y))

    