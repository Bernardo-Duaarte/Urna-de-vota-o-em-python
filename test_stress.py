import requests
import json
import time
import random
from datetime import datetime
from colorama import init, Fore, Style
from concurrent.futures import ThreadPoolExecutor
import threading

# Inicializa o colorama para cores no terminal
init()

BASE_URL = "http://localhost:5000"
print_lock = threading.Lock()  # Lock para evitar mistura de prints

def print_timestamp():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]

def print_response(response, operation):
    with print_lock:
        timestamp = print_timestamp()
        print(f"\n{Fore.CYAN}[{timestamp}] === {operation} ==={Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Status: {response.status_code}{Style.RESET_ALL}")
        try:
            data = response.json()
            print(f"{Fore.GREEN}Resposta:{Style.RESET_ALL}")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        except:
            print(f"{Fore.RED}Não foi possível decodificar a resposta como JSON{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * (len(operation) + 8)}{Style.RESET_ALL}\n")

def gerar_cpf():
    return ''.join([str(random.randint(0, 9)) for _ in range(11)])

def gerar_nome():
    nomes = ["Maria", "João", "José", "Ana", "Pedro", "Paulo", "Carlos", "Sandra", "Marcos", "Julia"]
    sobrenomes = ["Silva", "Santos", "Oliveira", "Souza", "Ferreira", "Rodrigues", "Almeida", "Lima"]
    return f"{random.choice(nomes)} {random.choice(sobrenomes)}"

def cadastrar_eleitor(i):
    eleitor = {
        "cpf": gerar_cpf(),
        "nome": gerar_nome()
    }
    try:
        response = requests.post(f"{BASE_URL}/cadastrar", json=eleitor)
        print_response(response, f"Cadastro #{i+1} - {eleitor['nome']}")
        if response.status_code == 201:
            return eleitor
    except Exception as e:
        with print_lock:
            print(f"{Fore.RED}Erro ao cadastrar eleitor {eleitor['nome']}: {str(e)}{Style.RESET_ALL}")
    return None

def votar_eleitor(args):
    i, eleitor, candidato = args
    try:
        voto = {
            "cpf": eleitor["cpf"],
            "candidato_id": candidato["id"]
        }
        response = requests.post(f"{BASE_URL}/votar", json=voto)
        print_response(response, f"Voto #{i+1} - Eleitor: {eleitor['nome']}")
    except Exception as e:
        with print_lock:
            print(f"{Fore.RED}Erro ao registrar voto de {eleitor['nome']}: {str(e)}{Style.RESET_ALL}")

def teste_cadastro_paralelo(num_eleitores=50):
    print(f"\n{Fore.BLUE}🗳️ Iniciando teste de cadastro em paralelo de {num_eleitores} eleitores...{Style.RESET_ALL}")
    eleitores = []
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(cadastrar_eleitor, i) for i in range(num_eleitores)]
        for future in futures:
            eleitor = future.result()
            if eleitor:
                eleitores.append(eleitor)
    
    return eleitores

def teste_votacao_paralela(eleitores):
    print(f"\n{Fore.BLUE}🗳️ Iniciando votação em paralelo com {len(eleitores)} eleitores...{Style.RESET_ALL}")
    
    try:
        response = requests.get(f"{BASE_URL}/candidatos")
        candidatos = response.json()
        
        # Prepara os argumentos para votação
        args_list = []
        for i, eleitor in enumerate(eleitores):
            candidato = random.choice(candidatos)
            args_list.append((i, eleitor, candidato))
        
        # Executa votos em paralelo
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(votar_eleitor, args_list)
            
    except Exception as e:
        print(f"{Fore.RED}Erro ao obter lista de candidatos: {str(e)}{Style.RESET_ALL}")

def teste_tentativas_invalidas_paralelo():
    print(f"\n{Fore.BLUE}🗳️ Testando tentativas inválidas em paralelo...{Style.RESET_ALL}")
    
    def fazer_tentativa_invalida(caso):
        if caso == 0:
            # CPF inválido
            response = requests.post(f"{BASE_URL}/cadastrar", json={
                "cpf": "123",
                "nome": "Teste Inválido"
            })
            print_response(response, "Tentativa de cadastro com CPF inválido")
        elif caso == 1:
            # Nome inválido
            response = requests.post(f"{BASE_URL}/cadastrar", json={
                "cpf": "12345678901",
                "nome": "A"
            })
            print_response(response, "Tentativa de cadastro com nome inválido")
        else:
            # CPF não cadastrado
            response = requests.post(f"{BASE_URL}/votar", json={
                "cpf": "99999999999",
                "candidato_id": 1
            })
            print_response(response, "Tentativa de voto com CPF não cadastrado")
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(fazer_tentativa_invalida, range(3))

def mostrar_resultados():
    print(f"\n{Fore.BLUE}📊 Resultados da votação:{Style.RESET_ALL}")
    try:
        response = requests.get(f"{BASE_URL}/resultados")
        print_response(response, "Resultados finais")
    except Exception as e:
        print(f"{Fore.RED}Erro ao obter resultados: {str(e)}{Style.RESET_ALL}")

def main():
    try:
        print(f"{Fore.GREEN}🚀 Iniciando testes de carga em paralelo no sistema de votação...{Style.RESET_ALL}")
        
        # Teste 1: Cadastros válidos em paralelo (50 eleitores)
        eleitores = teste_cadastro_paralelo(50)
        
        # Teste 2: Tentativas inválidas em paralelo
        teste_tentativas_invalidas_paralelo()
        
        # Teste 3: Votação em paralelo
        teste_votacao_paralela(eleitores)
        
        # Teste 4: Resultados
        mostrar_resultados()
        
        print(f"\n{Fore.GREEN}✅ Testes de carga concluídos!{Style.RESET_ALL}")
        
    except requests.exceptions.ConnectionError:
        print(f"{Fore.RED}❌ Erro: Não foi possível conectar ao servidor. Certifique-se que ele está rodando na porta 5000.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Erro inesperado: {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    main() 