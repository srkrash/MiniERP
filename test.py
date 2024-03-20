from datetime import datetime

def tempo_atual():
    # Obter o tempo atual
    tempo_agora = datetime.now()
    
    # Formatar o tempo no formato desejado
    tempo_formatado = tempo_agora.strftime("%Y-%m-%d %H:%M:%S")
    
    return tempo_formatado

# Exemplo de uso da função
print(tempo_atual())
