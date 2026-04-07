import random
import pygame

from Cidade import cidade, gerar_evento, n
from Agentes.drones import Drone
from bdi import BDI

pygame.init()

# ================= CONFIG =================
CEL = 60
LARGURA = n * CEL
ALTURA = n * CEL

tela = pygame.display.set_mode((LARGURA, ALTURA))
clock = pygame.time.Clock()
fonte = pygame.font.SysFont(None, 24)

bdi = BDI()
drone = Drone(n)

# ================= UPDATE =================
def atualizar():
    # Gera evento com probabilidade (não em todo frame)
    if random.random() < 0.1:
        gerar_evento(cidade)

    drone.mover()
    drone.observar(cidade, bdi)

    bdi.decidir_acoes()

    for bombeiro in bdi.bombeiros.values():
        bombeiro.atualizar(cidade)


# ================= DRAW =================
def contar_elementos():
    total_fogos = 0
    total_vitimas = 0

    for i in range(n):
        for j in range(n):
            if "fogo" in cidade[i][j]:
                total_fogos += 1
            if "vitima" in cidade[i][j]:
                total_vitimas += 1

    return total_fogos, total_vitimas


def desenhar_hud(total_fogos, total_vitimas):
    pygame.draw.rect(tela, (255, 255, 255), (5, 5, 200, 90))
    pygame.draw.rect(tela, (0, 0, 0), (5, 5, 200, 90), 2)

    textos = [
        f"Fogos (real): {total_fogos}",
        f"Vitimas (real): {total_vitimas}",
        f"Fogos (BDI): {len(bdi.fogos)}",
        f"Vitimas (BDI): {len(bdi.vitimas)}",
    ]

    for i, txt in enumerate(textos):
        render = fonte.render(txt, True, (0, 0, 0))
        tela.blit(render, (10, 10 + i * 20))


def desenhar_grid():
    for i in range(n):
        for j in range(n):
            celula = cidade[i][j]

            # Fundo por tipo
            if "fogo" in celula:
                pygame.draw.rect(tela, (255, 200, 200), (j * CEL, i * CEL, CEL, CEL))

            if "vitima" in celula:
                pygame.draw.rect(tela, (200, 200, 255), (j * CEL, i * CEL, CEL, CEL))

            # Texto (F, V ou FV)
            texto = ""
            if "fogo" in celula:
                texto += "F"
            if "vitima" in celula:
                texto += "V"

            if texto:
                t = fonte.render(texto, True, (0, 0, 0))
                tela.blit(t, (j * CEL + 5, i * CEL + 5))

            # Borda da célula
            pygame.draw.rect(tela, (180, 180, 180), (j * CEL, i * CEL, CEL, CEL), 1)


def desenhar_divisoes():
    metade = (n // 2) * CEL
    pygame.draw.line(tela, (0, 0, 0), (0, metade), (LARGURA, metade), 2)
    pygame.draw.line(tela, (0, 0, 0), (metade, 0), (metade, ALTURA), 2)


def desenhar_agentes():
    # Drone
    pygame.draw.circle(
        tela,
        (0, 200, 0),
        (drone.x * CEL + 30, drone.y * CEL + 30),
        8
    )

    # Bombeiros
    for b in bdi.bombeiros.values():
        pygame.draw.circle(
            tela,
            (255, 140, 0),
            (b.posicao[0] * CEL + 30, b.posicao[1] * CEL + 30),
            8
        )

    # Agentes extras
    if hasattr(bdi, "seq"):
        pygame.draw.circle(
            tela,
            (150, 0, 200),
            (bdi.seq.posicao[0] * CEL + 30, bdi.seq.posicao[1] * CEL + 30),
            8
        )

    if hasattr(bdi, "ot"):
        pygame.draw.circle(
            tela,
            (0, 0, 0),
            (bdi.ot.posicao[0] * CEL + 30, bdi.ot.posicao[1] * CEL + 30),
            8
        )


def desenhar_textos_agentes():
    if hasattr(bdi, "seq"):
        t1 = fonte.render(f"Seq: {bdi.seq.passos}", True, (0, 0, 0))
        tela.blit(t1, (10, 50))

    if hasattr(bdi, "ot"):
        t2 = fonte.render(f"Util: {bdi.ot.passos}", True, (0, 0, 0))
        tela.blit(t2, (10, 70))


def desenhar():
    tela.fill((240, 240, 240))

    total_fogos, total_vitimas = contar_elementos()

    desenhar_hud(total_fogos, total_vitimas)
    desenhar_grid()
    desenhar_divisoes()
    desenhar_agentes()
    desenhar_textos_agentes()

    pygame.display.update()


# ================= LOOP PRINCIPAL =================
def main():
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

        atualizar()
        desenhar()
        clock.tick(5)


if __name__ == "__main__":
    main()