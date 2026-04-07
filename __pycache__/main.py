import pygame
import random
from src.ambiente import Ambiente, TAM
from src.agentes  import Drone, Bombeiro, SocorristaSequencial, SocorristaInteligente
from src.bdi      import BDI
from src.utils    import CELL, PAINEL, FPS, COR

LARGURA     = TAM * CELL + PAINEL
ALTURA      = TAM * CELL
MAX_TURNOS  = 300         


def main():
    pygame.init()
    tela  = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Smart City — Sistema de Emergências (UFMA / IA)")
    clock = pygame.time.Clock()

    fonte_p = pygame.font.SysFont("monospace", 12)
    fonte_m = pygame.font.SysFont("monospace", 13, bold=True)
    fonte_g = pygame.font.SysFont("monospace", 16, bold=True)

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
                cor  = COR["fogo"] if cel == "F" else COR["vitima"] if cel == "V" else COR["bg"]
                pygame.draw.rect(tela, cor, rect)
                pygame.draw.rect(tela, COR["grid"], rect, 1)

        pygame.draw.line(tela, COR["grid_line"], (4*CELL, 0),      (4*CELL, ALTURA), 2)
        pygame.draw.line(tela, COR["grid_line"], (0,      4*CELL), (TAM*CELL, 4*CELL), 2)

        for lbl, lx, ly in [("Q1", 0, 0), ("Q2", 0, 4), ("Q3", 4, 0), ("Q4", 4, 4)]:
            s = fonte_p.render(lbl, True, COR["grid_line"])
            tela.blit(s, (ly*CELL + 4, lx*CELL + 4))

    def desenhar_agentes():
        for d in drones:
            cx = d.pos[1] * CELL + CELL // 2
            cy = d.pos[0] * CELL + CELL // 2
            pygame.draw.circle(tela, COR["drone"], (cx, cy), 7)
            tela.blit(fonte_p.render(f"D{d.id}", True, COR["drone"]), (cx - 8, cy - 20))

        for q, b in bombeiros.items():
            cx = b.pos[1] * CELL + CELL // 2
            cy = b.pos[0] * CELL + CELL // 2
            pygame.draw.rect(tela, COR["bombeiro"], (cx - 8, cy - 8, 16, 16))
            tela.blit(fonte_p.render(q, True, COR["bombeiro"]), (cx - 8, cy - 22))

        cx = seq.pos[1] * CELL + CELL // 2
        cy = seq.pos[0] * CELL + CELL // 2
        pygame.draw.polygon(tela, COR["seq"], [(cx, cy-11), (cx-9, cy+8), (cx+9, cy+8)])
        tela.blit(fonte_p.render("SEQ", True, COR["seq"]), (cx - 12, cy - 24))

        cx = intel.pos[1] * CELL + CELL // 2
        cy = intel.pos[0] * CELL + CELL // 2
        pygame.draw.polygon(tela, COR["intel"], [(cx, cy-11), (cx-9, cy+8), (cx+9, cy+8)])
        tela.blit(fonte_p.render("OTM", True, COR["intel"]), (cx - 12, cy - 24))

    def desenhar_painel():
        px = TAM * CELL
        pygame.draw.rect(tela, COR["painel"], (px, 0, PAINEL, ALTURA))
        pygame.draw.line(tela, COR["grid"],   (px, 0), (px, ALTURA), 2)

        def txt(s, x, y, cor=COR["texto"], f=fonte_p):
            tela.blit(f.render(s, True, cor), (x, y))

        lx = px + 10
        ly = 8  
        
        txt("SMART CITY",            lx, ly,      COR["titulo"], fonte_g); ly += 22
        txt("Gestão de Emergências", lx, ly,      COR["grid_line"]);        ly += 18
        status = f"Turno: {turno}/{MAX_TURNOS}" + (" — FIM" if encerrado else "")
        txt(status, lx, ly, COR["alerta"] if encerrado else COR["texto"]);  ly += 22

        ly += 6
        txt("── SEQUENCIAL (FIFO) ──", lx, ly, COR["seq_cor"], fonte_m); ly += 18
        txt(f"Resgates : {seq.resgates}",        lx, ly, COR["seq_cor"]); ly += 16
        txt(f"Passos   : {seq.passos}",           lx, ly);                ly += 16
        txt(f"Distância: {seq.distancia_total}",  lx, ly);                ly += 20

        ly += 6
        txt("── OTIMIZADOR (UTIL.) ──", lx, ly, COR["intel_cor"], fonte_m); ly += 18
        txt(f"Resgates : {intel.resgates}",       lx, ly, COR["intel_cor"]); ly += 16
        txt(f"Passos   : {intel.passos}",          lx, ly);                  ly += 16
        txt(f"Distância: {intel.distancia_total}", lx, ly);                  ly += 20

        ly += 6
        txt("── COMPARATIVO ──", lx, ly, COR["titulo"], fonte_m); ly += 18

        dr = seq.resgates        - intel.resgates
        dp = seq.passos          - intel.passos
        dd = seq.distancia_total - intel.distancia_total

        def cor_delta(v):
            return COR["alerta"] if v > 0 else COR["ok"] if v < 0 else COR["texto"]

        txt(f"Δ resgates : {dr:+d}",   lx, ly, cor_delta(dr)); ly += 16
        txt(f"Δ passos   : {dp:+d}",   lx, ly, cor_delta(dp)); ly += 16
        txt(f"Δ distância: {dd:+d}",   lx, ly, cor_delta(dd)); ly += 16
        txt("(verde = OTM melhor)", lx, ly, COR["grid_line"]);  ly += 20

        txt(f"Fogos apagados: {fogos_apag}", lx, ly, COR["fogo"]); ly += 22

        ly += 6
        txt("── LEGENDA ──", lx, ly, COR["titulo"], fonte_m); ly += 18
        for cor, label in [
            (COR["fogo"],     "■ Fogo"),
            (COR["vitima"],   "■ Vítima"),
            (COR["drone"],    "● Drone"),
            (COR["bombeiro"], "■ Bombeiro"),
            (COR["seq"],      "▲ SEQ — FIFO"),
            (COR["intel"],    "▲ OTM — utilidade"),
        ]:
            txt(label, lx, ly, cor); ly += 15

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
                print(f"[T{turno:04d}] SEQ salvou vítima em {r[1]}")

            r = intel.agir(ambiente)
            if r:
                print(f"[T{turno:04d}] OTM salvou vítima em {r[1]}")

            if turno >= MAX_TURNOS:
                encerrado = True

        tela.fill(COR["bg"])
        desenhar_grid()
        desenhar_agentes()
        desenhar_painel()
        pygame.display.flip()
        clock.tick(FPS)

    print("\n" + "=" * 55)
    print("RELATÓRIO FINAL — Smart City / UFMA IA")
    print("=" * 55)
    print(f"{'Métrica':<28} {'SEQ':>10} {'OTM':>10}")
    print("-" * 55)
    print(f"{'Resgates':<28} {seq.resgates:>10} {intel.resgates:>10}")
    print(f"{'Passos totais':<28} {seq.passos:>10} {intel.passos:>10}")
    print(f"{'Distância total':<28} {seq.distancia_total:>10} {intel.distancia_total:>10}")
    print(f"{'Fogos apagados (total)':<28} {fogos_apag:>10}")
    print("=" * 55)
    winner = "OTIMIZADOR" if intel.passos < seq.passos else "SEQUENCIAL" if seq.passos < intel.passos else "EMPATE"
    print(f"Menor distância total: {winner}")
    print("=" * 55)
    pygame.quit()


if __name__ == "__main__":
    main()