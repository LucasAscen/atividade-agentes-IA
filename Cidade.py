import random 

n = 8 #matriz 8x8
cidade = [[[] for i in range(n)] for j in range(n)]

#gerar eventos aleatorios na cidade
def gerar_evento(cidade):

    eventos = ['fogo', 'vitima']
    escolha = random.choice(eventos) #escolhe um evento aleatorio

    while True: 
        x = random.randint(0, n-1)#gera coordenada x aleatoria, o mesmo vale para y
        y = random.randint(0,n-1)



        if escolha not in cidade[x][y]: #se o evento escolhido nao existir na coordenada, adiciona o evento
                cidade[x][y].append(escolha)
                print(f"Evento {escolha} gerado em ({x}, {y})")  # debug
                break

                
            
        
