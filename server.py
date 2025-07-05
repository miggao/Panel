import os
import requests
import zipfile
import subprocess
import sys
import ctypes
import shutil
from pathlib import Path

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def download_file(url, filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def install_minecraft_bedrock():
    print("=== Instalador de Minecraft Bedrock 1.21.93.1 ===")
    
    # Verificar se é Windows
    if not sys.platform.startswith('win'):
        print("Erro: Este instalador só funciona no Windows.")
        return
    
    # Verificar privilégios de administrador
    if not is_admin():
        print("Erro: Por favor, execute este script como administrador.")
        return
    
    # URLs e caminhos
    download_url = "https://minecraft.azureedge.net/bin-win/bedrock-server-1.21.93.01.zip"
    temp_dir = os.path.join(os.environ['TEMP'], 'mc_bedrock_install')
    install_dir = os.path.join(os.getenv('PROGRAMFILES'), 'Minecraft Bedrock Server')
    
    try:
        # Criar diretórios temporários
        os.makedirs(temp_dir, exist_ok=True)
        zip_path = os.path.join(temp_dir, 'bedrock-server.zip')
        
        print(f"Baixando Minecraft Bedrock Server 1.21.93.1...")
        download_file(download_url, zip_path)
        
        print("Extraindo arquivos...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(install_dir)
        
        # Configurar permissões (opcional)
        print("Configurando permissões...")
        try:
            subprocess.run(['icacls', install_dir, '/grant', 'Everyone:(OI)(CI)F', '/T'], check=True)
        except subprocess.CalledProcessError:
            print("Aviso: Não foi possível configurar permissões. Continue manualmente se necessário.")
        
        # Criar atalho na área de trabalho
        desktop = Path(os.path.join(os.path.expanduser('~'), 'Desktop'))
        shortcut_path = desktop / 'Minecraft Bedrock Server.lnk'
        
        if not shortcut_path.exists():
            try:
                from win32com.client import Dispatch
                shell = Dispatch('WScript.Shell')
                shortcut = shell.CreateShortCut(str(shortcut_path))
                shortcut.Targetpath = str(Path(install_dir) / 'bedrock_server.exe')
                shortcut.WorkingDirectory = install_dir
                shortcut.save()
                print("Atalho criado na área de trabalho.")
            except ImportError:
                print("Aviso: pywin32 não instalado. Não foi possível criar atalho.")
            except Exception as e:
                print(f"Aviso: Não foi possível criar atalho: {e}")
        
        print("\nInstalação concluída com sucesso!")
        print(f"O servidor foi instalado em: {install_dir}")
        print("\nPara iniciar o servidor, execute o arquivo 'bedrock_server.exe'")
        print("ou use o atalho criado na sua área de trabalho.")
        
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar o servidor: {e}")
    except zipfile.BadZipFile:
        print("Erro: O arquivo baixado está corrompido.")
    except Exception as e:
        print(f"Erro inesperado: {e}")
    finally:
        # Limpar arquivos temporários
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    install_minecraft_bedrock()
    input("Pressione Enter para sair...")
