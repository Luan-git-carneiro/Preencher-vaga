# preencher_vaga.py: Script principal para automação de formulários de vagas

import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config import INFOS_PESSOAIS  # Importa configs

def main():
    try:
        # Attach ao Chrome existente
        options = Options()
        options.debugger_address = "127.0.0.1:9222"
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        print("Conectado à sessão do navegador!")
        time.sleep(random.uniform(2, 5))  # Delay simulado
        
        # Lógicas futuras aqui
        
        input("Pressione Enter para continuar...")  # Mantém aberta
    except Exception as e:
        print(f"Erro: {e}. Verifique Chrome com --remote-debugging-port=9222.")

if __name__ == "__main__":
    main()