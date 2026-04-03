#aqui sera o cerebro de todos os agentes 
from Agentes.drones import observar_drone
from Cidade import cidade, gerar_evento

class BDI:

    
    def __init__(self):
        self.fogos = set()
        self.vitimas = set()
        

    def receber_fogo(self, x, y):
        celula_fogos = (x, y)
        self.fogos.add(celula_fogos)
        print(f'Fogo detectado na coordenada: {celula_fogos}')

    def receber_vitima(self, x, y):
        celula_vitimas = (x, y)
        self.vitimas.add(celula_vitimas)
        print(f'Vitima detectada na coordenada: {celula_vitimas}')
        # adicionar no set
        
    def descobrir_quadrante(x,y):
        if x < 10 and y <10:
            return 'Quadrante 1'
        elif x < 10 and y >= 10:
            return 'Quadrante 2'
        elif x >= 10 and y < 10:
            return 'Quadrante 3'
        else:
            return 'Quadrante 4'
        
    def decidir_acoes(self):
        for (x,y) in self.fogos:
            quadrante = self.descobrir_quadrante(x,y)
            print(f'Fogo no {quadrante} - Enviar equipe de combate a incêndio')
        for (x,y) in self.vitimas:
            quadrante = self.descobrir_quadrante(x,y)
            print(f'Vitima no {quadrante} - Enviar equipe de resgate')

    def apagar_fogo(self, x,y):
        if (x,y) in self.fogos:
            self.fogos.remove((x,y))
            