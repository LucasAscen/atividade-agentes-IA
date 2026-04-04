from Agentes.drones import observar_drone
from bdi import BDI
from Cidade import cidade, gerar_evento

def main():
    bdi = BDI()
    
    for i in range(6):  # Gerar 6 eventos aleatórios na cidade
        print(f"\n--- TURNO {i+1} ---")
        
        # 1. O ambiente muda (gera fogo/eventos)
        gerar_evento(cidade)
        
        
        # 2. O drone observa o ambiente e reporta para o BDI
        observar_drone(cidade, bdi)
        
        # 3. O BDI decide as ações a serem tomadas com base nas informações recebidas
        bdi.decidir_acoes()

    print("\n============================")
    print("Simulacao concluída.")
    print("============================")


if __name__ == "__main__":
    main()