import pygame
from Cidade import cidade, gerar_evento, n
from Agentes.drones import Drone
from bdi import BDI

pygame.init()

CEL = 60
tela = pygame.display.set_mode((n*CEL,n*CEL))
clock = pygame.time.Clock()

bdi = BDI()
drone = Drone(n)

fonte = pygame.font.SysFont(None,24)


while True:

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            exit()

    gerar_evento(cidade)

    drone.mover()
    drone.observar(cidade,bdi)

    bdi.decidir_acoes()


    tela.fill((255,255,255))

    for i in range(n):
        for j in range(n):

            pygame.draw.rect(tela,(200,200,200),(i*CEL,j*CEL,CEL,CEL),1)

            if "fogo" in cidade[i][j]:
                pygame.draw.circle(tela,(255,0,0),(i*CEL+30,j*CEL+30),8)

            if "vitima" in cidade[i][j]:
                pygame.draw.circle(tela,(0,0,255),(i*CEL+30,j*CEL+30),8)


    pygame.draw.circle(tela,(0,200,0),(drone.x*CEL+30,drone.y*CEL+30),8)


    for b in bdi.bombeiros.values():

        pygame.draw.circle(tela,(255,140,0),(b.posicao[0]*CEL+30,b.posicao[1]*CEL+30),8)


    pygame.draw.circle(tela,(150,0,200),(bdi.seq.posicao[0]*CEL+30,bdi.seq.posicao[1]*CEL+30),8)

    pygame.draw.circle(tela,(0,0,0),(bdi.ot.posicao[0]*CEL+30,bdi.ot.posicao[1]*CEL+30),8)


    t1 = fonte.render(f"Seq: {bdi.seq.passos}",True,(0,0,0))
    t2 = fonte.render(f"Util: {bdi.ot.passos}",True,(0,0,0))

    tela.blit(t1,(10,10))
    tela.blit(t2,(10,30))


    pygame.display.update()

    clock.tick(2)