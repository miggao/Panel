import os
import sys
import subprocess
import threading
import time
from pathlib import Path

def check_requirements():
    # Verificar se os arquivos necessários existem
    required_files = {
        'bedrock_server': './bedrock_server',
        'playit': './playit-linux-amd64'
    }
    
    missing_files = []
    for file_name, file_path in required_files.items():
        if not os.path.exists(file_path):
            missing_files.append(file_name)
    
    if missing_files:
        print(f"Erro: Os seguintes arquivos estão faltando: {', '.join(missing_files)}")
        sys.exit(1)

def run_process(command, cwd=None):
    try:
        process = subprocess.Popen(
            command,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        for line in process.stdout:
            print(line, end='')
            
        return process.wait()
    except Exception as e:
        print(f"Erro ao executar o comando {' '.join(command)}: {e}")
        return 1

def start_playit():
    print("\n=== Iniciando Playit.gg ===")
    playit_path = './playit-linux-amd64'
    
    # Tornar o arquivo executável se necessário
    if not os.access(playit_path, os.X_OK):
        os.chmod(playit_path, 0o755)
    
    return run_process([playit_path])

def start_bedrock_server():
    print("\n=== Iniciando Minecraft Bedrock Server ===")
    server_path = './bedrock_server'
    
    # Tornar o arquivo executável se necessário
    if not os.access(server_path, os.X_OK):
        os.chmod(server_path, 0o755)
    
    return run_process([server_path])

def main():
    print("=== Iniciador de Minecraft Bedrock com Playit.gg ===")
    print("Este script iniciará o servidor Minecraft e o Playit no mesmo terminal.")
    print("Pressione Ctrl+C para parar ambos os serviços.\n")
    
    check_requirements()
    
    try:
        # Criar threads para executar ambos os processos
        playit_thread = threading.Thread(target=start_playit)
        bedrock_thread = threading.Thread(target=start_bedrock_server)
        
        # Configurar threads como daemon para que terminem quando o programa principal terminar
        playit_thread.daemon = True
        bedrock_thread.daemon = True
        
        # Iniciar threads
        playit_thread.start()
        time.sleep(2)  # Dar um tempo para o playit iniciar
        bedrock_thread.start()
        
        # Manter o programa principal rodando
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nRecebido Ctrl+C. Encerrando serviços...")
        sys.exit(0)
    except Exception as e:
        print(f"Erro inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
