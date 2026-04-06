import random

import pygame
from Cidade import cidade, gerar_evento, n
from Agentes.drones import Drone
from bdi import BDI

pygame.init()

CEL = 60
tela = pygame.display.set_mode((n*CEL, n*CEL))
clock = pygame.time.Clock()

bdi = BDI()
drone = Drone(n)

fonte = pygame.font.SysFont(None, 24)


# 🔹 UPDATE (lógica do sistema)
def atualizar():
    # gera evento com chance (não todo frame)
    if random.random() < 0.1:
        gerar_evento(cidade)

    drone.mover()
    drone.observar(cidade, bdi)

    bdi.decidir_acoes()
    for b in bdi.bombeiros.values():
        b.atualizar(cidade)


#DRAW 
def desenhar():
    #desenha o fundo
    tela.fill((240,240,240))
    total_fogos = 0
    total_vitimas = 0

    for i in range(n):
        for j in range(n):
            if "fogo" in cidade[i][j]:
                total_fogos += 1
            if "vitima" in cidade[i][j]:
                total_vitimas += 1


    ####################
    pygame.draw.rect(tela, (255,255,255), (5, 5, 200, 90)) 
    pygame.draw.rect(tela, (0,0,0), (5, 5, 200, 90), 2)     
    
    t_fogo_real = fonte.render(f"Fogos (real): {total_fogos}", True, (0,0,0))
    t_vit_real = fonte.render(f"Vitimas (real): {total_vitimas}", True, (0,0,0))

    t_fogo_bdi = fonte.render(f"Fogos (BDI): {len(bdi.fogos)}", True, (0,0,0))
    t_vit_bdi = fonte.render(f"Vitimas (BDI): {len(bdi.vitimas)}", True, (0,0,0))
    #################
    
    tela.blit(t_fogo_real, (10, 10))
    tela.blit(t_vit_real, (10, 30))
    tela.blit(t_fogo_bdi, (10, 50))
    tela.blit(t_vit_bdi, (10, 70))
    # grid e evenyos
    for i in range(n):
        for j in range(n):
            if "fogo" in cidade[i][j]:
                pygame.draw.rect(tela, (255,200,200), (j*CEL, i*CEL, CEL, CEL))

            if "vitima" in cidade[i][j]:
                pygame.draw.rect(tela, (200,200,255), (j*CEL, i*CEL, CEL, CEL))
                pygame.draw.rect(tela, (180,180,180), (j*CEL, i*CEL, CEL, CEL), 1)

            texto = ""

            if "fogo" in cidade[i][j]:#quando tentei usar elif, o programa não desenhava o V quando tinha fogo e vitima na mesma celula
                texto += "F"

            if "vitima" in cidade[i][j]:
                texto += "V"

            if texto:
                t = fonte.render(texto, True, (0,0,0))
                tela.blit(t, (j*CEL+5, i*CEL+5))

            pygame.draw.rect(tela, (180,180,180), (j*CEL, i*CEL, CEL, CEL), 1)
    # linha
    metade = (n//2)*CEL
    pygame.draw.line(tela, (0,0,0), (0, metade), (n*CEL, metade), 2)
    pygame.draw.line(tela, (0,0,0), (metade, 0), (metade, n*CEL), 2)

    # drone
    pygame.draw.circle(tela, (0,200,0), (drone.x*CEL+30, drone.y*CEL+30), 8)

    # bombeiros
    for b in bdi.bombeiros.values():
        pygame.draw.circle(tela, (255,140,0), (b.posicao[0]*CEL+30, b.posicao[1]*CEL+30), 8)

    # agentes extras
    if hasattr(bdi, "seq"):
        pygame.draw.circle(tela, (150,0,200), (bdi.seq.posicao[0]*CEL+30, bdi.seq.posicao[1]*CEL+30), 8)

    if hasattr(bdi, "ot"):
        pygame.draw.circle(tela, (0,0,0), (bdi.ot.posicao[0]*CEL+30, bdi.ot.posicao[1]*CEL+30), 8)

    # textos
    if hasattr(bdi, "seq"):
        t1 = fonte.render(f"Seq: {bdi.seq.passos}", True, (0,0,0))
        tela.blit(t1, (10,50))

    if hasattr(bdi, "ot"):
        t2 = fonte.render(f"Util: {bdi.ot.passos}", True, (0,0,0))
        tela.blit(t2, (10,70))

    pygame.display.update()



while True:

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            exit()

    atualizar()
    desenhar()

    clock.tick(5)