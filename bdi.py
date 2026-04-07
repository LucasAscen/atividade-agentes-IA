from Agentes.bombeiros import Bombeiros
from Agentes.socorrista_sequencial import SocorristaSequencial
from Agentes.socorrista_otimizador import SocorristaOtimizador
from Cidade import cidade, hospital


class BDI:

    def __init__(self):

        self.fogos = set()
        self.vitimas = set()
        self.resgate_ativo = False

        # bombeiros por quadrante
        self.bombeiros = {
            "Q1": Bombeiros((0,0),"Q1"),
            "Q2": Bombeiros((0,7),"Q2"),
            "Q3": Bombeiros((7,0),"Q3"),
            "Q4": Bombeiros((7,7),"Q4")
        }

        self.seq = SocorristaSequencial()
        self.ot = SocorristaOtimizador()


    def receber_fogo(self,x,y):
        self.fogos.add((x, y))

    def receber_vitima(self,x,y):
        self.vitimas.add((x, y))

    def quadrante(self,x,y):

        if x < 4 and y < 4: return "Q1"
        if x < 4 and y >=4: return "Q2"
        if x >=4 and y <4: return "Q3"
        return "Q4"


    def limpar_crencas(self):

        self.fogos = {f for f in self.fogos if "fogo" in cidade[f[0]][f[1]]}
        self.vitimas = {v for v in self.vitimas if "vitima" in cidade[v[0]][v[1]]}


    def decidir_acoes(self):

        self.limpar_crencas()

        fogos_por_q = {"Q1":[],"Q2":[],"Q3":[],"Q4":[]}

        for f in self.fogos:
            fogos_por_q[self.quadrante(*f)].append(f)


        # bombeiros atuam
        for q,fogos in fogos_por_q.items():

            for f in fogos:

                # definir destino
                if self.bombeiros[q].destino is None:
                    self.bombeiros[q].destino = f


            # apoio extra se houver mais de 1 fogo
            if len(fogos) > 1:

                for q2, b in self.bombeiros.items():

                    if q2 != q and b.destino is None:
                        b.destino = fogos[1]
                        break


        # fazendo os diabos andar
        for b in self.bombeiros.values():
            b.atualizar(cidade)


        self.limpar_crencas()


        # enviar vítimas para os dois socorristas
        if len(self.vitimas) >= 4 and not self.resgate_ativo:
            self.resgate_ativo = True
            import random
            lista = list(self.vitimas)
            random.shuffle(lista)

            self.seq.receber_lista(lista)
            self.ot.receber_lista(lista)

            self.seq.resgatar(cidade,hospital)
            self.ot.resgatar(cidade,hospital)
        if not self.vitimas:
            self.resgate_ativo = False

        self.limpar_crencas()