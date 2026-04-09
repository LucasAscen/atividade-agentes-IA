from src.ambiente import get_quadrante


#  AGENTE BDI
class BDI:
    def __init__(self, bombeiros, seq, intel):
        self.fogos   = [] 
        self.vitimas = []  
        self.bombeiros = bombeiros   
        self.seq       = seq
        self.intel     = intel

    # Atualização de crenças via relatórios dos drones 
    def atualizar_crencas(self, eventos):
        for tipo, pos in eventos:
            if tipo == "F" and pos not in self.fogos:
                self.fogos.append(pos)
            elif tipo == "V" and pos not in self.vitimas:
                self.vitimas.append(pos)

    # Ciclo de intenções 
    def executar_intencoes(self):
        self._plano_incendio()
        self._plano_resgate()

    #  Plano de Incêndio 

    def _plano_incendio(self):
        fogos_por_quadrante: dict[str, list] = {}
        for pos in self.fogos:
            q = get_quadrante(*pos)
            fogos_por_quadrante.setdefault(q, []).append(pos)

        fogos_pendentes = []

        for q, focos in fogos_por_quadrante.items():
            bombeiro_local = self.bombeiros[q]

            for i, pos in enumerate(focos):
                if i == 0 and not bombeiro_local.ocupado:
                    bombeiro_local.receber_despacho(pos)
                else:

                    despachado = False
                    for outro_q, outro_b in self.bombeiros.items():
                        if outro_q != q and not outro_b.ocupado:
                            outro_b.receber_despacho(pos)
                            despachado = True
                            break
                    if not despachado:
                        fogos_pendentes.append(pos)

        self.fogos = fogos_pendentes

    def _plano_resgate(self):
        if not self.vitimas:
            return
        novas = list(self.vitimas)  
        self.seq.receber_lista(novas)
        self.intel.receber_lista(novas)
        self.vitimas = []
