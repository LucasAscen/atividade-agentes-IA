#aqui jaz o agente reativo simples 
from BDI import bdi
from Cidade import cidade, gerar_evento

#basicamente um sensor ambulante limitado 

def observar_drone(cidade, bdi):
    for i in range(cidade.len()):
        for j in range(cidade[i].len()):
            if cidade[i][j]:# verifico as coordenadas 
                if 'fogo' in cidade[i][j]: #se tiver fogo, reporta o fogo
                    #cidade[x][y].reportar('fogo nessa area')
                    print(f'Fogo detectado na coordenada ({i}, {j})')
                    bdi.receber_fogo(i, j)
                if 'vitima' in cidade[i][j]:
                    #cidade[x][y].reportar('vitima nessa area')
                    print(f'Vitima detectada na coordenada ({i}, {j})')
                    bdi.receber_vitima(i, j)