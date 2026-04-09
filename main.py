import pygame
import random
from src.ambiente import Ambiente, TAM, HOSPITAL
from src.agentes  import Drone, Bombeiro, SocorristaSequencial, SocorristaInteligente
from src.bdi      import BDI
from src.utils    import CELL, PAINEL, FPS, COR

LARGURA    = TAM * CELL + PAINEL
ALTURA     = TAM * CELL
MAX_TURNOS = 300


def main():
    pygame.init()
    tela  = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption
    clock = pygame.time.Clock()

    fonte_p = pygame.font.SysFont("Arial", 12)
    fonte_m = pygame.font.SysFont("Arial", 13, bold=True)
    fonte_g = pygame.font.SysFont("Arial", 15, bold=True)

    ambiente  = Ambiente()
    drones    = [Drone(i) for i in range(3)]
    bombeiros = {
        "Q1": Bombeiro("Q1"), "Q2": Bombeiro("Q2"),
        "Q3": Bombeiro("Q3"), "Q4": Bombeiro("Q4"),
    }
    seq   = SocorristaSequencial()
    intel = SocorristaInteligente()
    bdi   = BDI(bombeiros, seq, intel)

    turno      = 0
    fogos_apag = 0
    encerrado  = False

    def desenhar_grid():
        for x in range(TAM):
            for y in range(TAM):
                rect = pygame.Rect(y * CELL, x * CELL, CELL, CELL)
                cel  = ambiente.grid[x][y]
                if cel == "F":
                    cor = COR["fogo"]
                elif cel == "V":
                    cor = COR["vitima"]
                elif cel == "H":
                    cor = COR["hospital"]
                else:
                    cor = COR["bg"]
                pygame.draw.rect(tela, cor, rect)
                pygame.draw.rect(tela, COR["grid"], rect, 1)

        meio = 4 * CELL
        pygame.draw.line(tela, COR["quadrante"], (meio, 0), (meio, ALTURA), 3)
        pygame.draw.line(tela, COR["quadrante"], (0, meio), (TAM * CELL, meio), 3)

        offset = 6
        labels = [
            ("Q1", offset,              offset),
            ("Q2", offset,              TAM*CELL//2 + offset),
            ("Q3", TAM*CELL//2 + offset, offset),
            ("Q4", TAM*CELL//2 + offset, TAM*CELL//2 + offset),
        ]
        for lbl, ly, lx in labels:
            s = fonte_m.render(lbl, True, COR["quadrante"])
            tela.blit(s, (lx, ly))

        hx, hy = HOSPITAL
        s = fonte_m.render("H+", True, COR["hosp_txt"])
        tela.blit(s, (hy*CELL + CELL//2 - 10, hx*CELL + CELL//2 - 8))

    def desenhar_agentes():
        for d in drones:
            cx = d.pos[1] * CELL + CELL // 2
            cy = d.pos[0] * CELL + CELL // 2
            pygame.draw.circle(tela, COR["drone"], (cx, cy), 8)
            pygame.draw.circle(tela, COR["drone_borda"], (cx, cy), 8, 2)
            tela.blit(fonte_p.render(f"D{d.id}", True, COR["drone_txt"]), (cx - 8, cy - 22))

        for q, b in bombeiros.items():
            cx = b.pos[1] * CELL + CELL // 2
            cy = b.pos[0] * CELL + CELL // 2
            pygame.draw.rect(tela, COR["bombeiro"], (cx - 9, cy - 9, 18, 18))
            pygame.draw.rect(tela, COR["bombeiro_borda"], (cx - 9, cy - 9, 18, 18), 2)
            tela.blit(fonte_p.render(q, True, COR["bombeiro_txt"]), (cx - 8, cy - 23))

        cx = seq.pos[1] * CELL + CELL // 2
        cy = seq.pos[0] * CELL + CELL // 2
        pygame.draw.polygon(tela, COR["seq"], [(cx, cy-12), (cx-10, cy+9), (cx+10, cy+9)])
        pygame.draw.polygon(tela, COR["seq_borda"], [(cx, cy-12), (cx-10, cy+9), (cx+10, cy+9)], 2)
        lbl = "SEQ→H" if seq.indo_hospital else "SEQ"
        tela.blit(fonte_p.render(lbl, True, COR["seq_txt"]), (cx - 14, cy - 26))

        cx = intel.pos[1] * CELL + CELL // 2
        cy = intel.pos[0] * CELL + CELL // 2
        pygame.draw.polygon(tela, COR["intel"], [(cx, cy-12), (cx-10, cy+9), (cx+10, cy+9)])
        pygame.draw.polygon(tela, COR["intel_borda"], [(cx, cy-12), (cx-10, cy+9), (cx+10, cy+9)], 2)
        lbl = "OTM→H" if intel.indo_hospital else "OTM"
        tela.blit(fonte_p.render(lbl, True, COR["intel_txt"]), (cx - 14, cy - 26))

    def desenhar_painel():
        px = TAM * CELL
        pygame.draw.rect(tela, COR["painel"], (px, 0, PAINEL, ALTURA))
        pygame.draw.line(tela, COR["painel_borda"], (px, 0), (px, ALTURA), 2)

        def txt(s, x, y, cor=COR["texto"], f=fonte_p):
            tela.blit(f.render(s, True, cor), (x, y))

        def linha(y):
            pygame.draw.line(tela, COR["separador"], (lx, y), (lx + PAINEL - 24, y), 1)

        lx = px + 14
        ly = 14

        ly += 24
        status = f"Turno  {turno} / {MAX_TURNOS}" + ("   [ENCERRADO]" if encerrado else "")
        txt(status, lx, ly, COR["alerta"] if encerrado else COR["subtitulo"]); ly += 16
        linha(ly); ly += 10

        # SEQ
        txt("Sequencial  (FIFO)", lx, ly, COR["seq_txt"], fonte_m); ly += 18
        txt(f"Resgates      {seq.resgates}",        lx, ly, COR["seq_val"]); ly += 15
        txt(f"Passos        {seq.passos}",           lx, ly, COR["texto"]); ly += 15
        txt(f"Distância     {seq.distancia_total}",  lx, ly, COR["texto"]); ly += 14
        estado = "indo ao hospital" if seq.indo_hospital else (f"alvo {seq.alvo_atual}" if seq.alvo_atual else "aguardando")
        txt(f"Estado: {estado}", lx, ly, COR["subtitulo"]); ly += 14
        linha(ly); ly += 10

        # OTM
        txt("Otimizador  (Utilidade)", lx, ly, COR["intel_txt"], fonte_m); ly += 18
        txt(f"Resgates      {intel.resgates}",       lx, ly, COR["intel_val"]); ly += 15
        txt(f"Passos        {intel.passos}",          lx, ly, COR["texto"]); ly += 15
        txt(f"Distância     {intel.distancia_total}", lx, ly, COR["texto"]); ly += 14
        estado = "indo ao hospital" if intel.indo_hospital else (f"alvo {intel.alvo_atual}" if intel.alvo_atual else "aguardando")
        txt(f"Estado: {estado}", lx, ly, COR["subtitulo"]); ly += 14
        linha(ly); ly += 10

        # Comparativo
        txt("Comparativo", lx, ly, COR["titulo"], fonte_m); ly += 18
        dr = seq.resgates        - intel.resgates
        dp = seq.passos          - intel.passos
        dd = seq.distancia_total - intel.distancia_total

        def dcor(v):
            return COR["pior"] if v > 0 else COR["melhor"] if v < 0 else COR["texto"]

        txt(f"Resgates    {dr:+d}",   lx, ly, dcor(-dr)); ly += 15
        txt(f"Passos      {dp:+d}",   lx, ly, dcor(dp));  ly += 15
        txt(f"Distância   {dd:+d}",   lx, ly, dcor(dd));  ly += 13
        txt("verde = OTM melhor", lx, ly, COR["subtitulo"]); ly += 16

        if intel.distancia_total == 0 and seq.distancia_total == 0:
            vt, vc = "—", COR["texto"]
        elif intel.distancia_total < seq.distancia_total:
            vt, vc = "OTM vence", COR["melhor"]
        elif seq.distancia_total < intel.distancia_total:
            vt, vc = "SEQ vence", COR["pior"]
        else:
            vt, vc = "Empate", COR["titulo"]
        txt(f"Líder: {vt}", lx, ly, vc, fonte_m); ly += 18
        linha(ly); ly += 10

        txt(f"Fogos apagados: {fogos_apag}", lx, ly, COR["fogo_txt"]); ly += 18
        linha(ly); ly += 10

        # Legenda
        txt("Legenda", lx, ly, COR["titulo"], fonte_m); ly += 16
        for cor, label in [
            (COR["fogo"],     "  Fogo"),
            (COR["vitima"],   "  Vítima"),
            (COR["hospital"], "  Hospital"),
            (COR["drone"],    "  Drone"),
            (COR["bombeiro"], "  Bombeiro"),
            (COR["seq"],      "  SEQ — sequencial"),
            (COR["intel"],    "  OTM — otimizador"),
        ]:
            pygame.draw.rect(tela, cor, (lx, ly + 2, 10, 10))
            txt(label, lx, ly, COR["texto"]); ly += 14

    rodando   = True
    encerrado = False

    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                rodando = False

        if not encerrado:
            turno += 1
            if random.random() < 0.30:
                ambiente.gerar_evento()

            todos_eventos = []
            for d in drones:
                d.mover()
                todos_eventos.extend(d.observar(ambiente))

            bdi.atualizar_crencas(todos_eventos)
            bdi.executar_intencoes()

            for q, b in bombeiros.items():
                resultado = b.agir(ambiente)
                if resultado:
                    fogos_apag += 1
                    print(f"[T{turno:04d}] Bombeiro {q} apagou fogo em {resultado[1]}")

            r = seq.agir(ambiente)
            if r:
                print(f"[T{turno:04d}] SEQ resgatou vítima de {r[1]} → hospital")

            r = intel.agir(ambiente)
            if r:
                print(f"[T{turno:04d}] OTM resgatou vítima de {r[1]} → hospital")

            if turno >= MAX_TURNOS:
                encerrado = True

        tela.fill(COR["bg"])
        desenhar_grid()
        desenhar_agentes()
        desenhar_painel()
        pygame.display.flip()
        clock.tick(FPS)

    
    print("RELATÓRIO FINAL — Smart City / UFMA IA")
   
    print(f"{'Métrica':<28} {'SEQ':>10} {'OTM':>10}")
  
    print(f"{'Resgates':<28} {seq.resgates:>10} {intel.resgates:>10}")
    print(f"{'Passos totais':<28} {seq.passos:>10} {intel.passos:>10}")
    print(f"{'Distância total':<28} {seq.distancia_total:>10} {intel.distancia_total:>10}")
    print(f"{'Fogos apagados (total)':<28} {fogos_apag:>10}")
 
    if intel.distancia_total < seq.distancia_total:
        winner = "OTIMIZADOR"
    elif seq.distancia_total < intel.distancia_total:
        winner = "SEQUENCIAL"
    else:
        winner = "EMPATE"
    print(f"Menor distância total: {winner}")
   
    pygame.quit()


if __name__ == "__main__":
    main()

