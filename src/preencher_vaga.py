# preencher_vaga.py: Script principal para automação de formulários de vagas

import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from config import INFOS_PESSOAIS, MAPA_KEYWORDS  # Importa configs
import unicodedata

import ollama
from config import INFOS_PESSOAIS

# ====================== NOVA FUNÇÃO ======================
def gerar_resposta_ia(pergunta: str) -> str:
    """
    Gera uma resposta personalizada para perguntas dissertativas do formulário.
    
    Args:
        pergunta (str): A pergunta exata extraída do formulário
    
    Returns:
        str: Resposta profissional e personalizada
    """
    # Contexto do usuário (vindo do config.py)
    contexto = (
        f"Nome completo: {INFOS_PESSOAIS.get('nome', 'Candidato')}. "
        f"Experiências: {INFOS_PESSOAIS.get('experiencias', 'Experiência relevante')}. "
        f"Habilidades principais: {INFOS_PESSOAIS.get('habilidades', 'Python, Selenium, etc.')}. "
        "Estou buscando oportunidades na área de tecnologia."
    )

    # Prompt bem engenhado (em inglês para melhor resultado)
    prompt = f"""
    Você é um consultor de carreiras extremamente profissional e persuasivo.
    Escreva uma resposta natural, concisa e convincente (máximo 180 palavras) 
    para a seguinte pergunta de formulário de emprego:

    Pergunta: "{pergunta}"

    Use as seguintes informações pessoais do candidato:
    {contexto}

    Regras importantes:
    - Seja honesto, confiante e positivo
    - Evite clichês ("sou proativo", "trabalho em equipe")
    - Foque em conquistas e motivação real
    - Use linguagem formal, mas humana
    """

    try:
        response = ollama.generate(
            model='llama3.2:1b',      # modelo leve que estamos usando
            prompt=prompt,
            options={
                "temperature": 0.7,   # equilíbrio entre criatividade e coerência
                "num_predict": 300    # limite de tokens
            }
        )
        
        resposta_limpa = response['response'].strip()
        
        # Fallback caso a IA devolva algo muito curto ou vazio
        if len(resposta_limpa) < 30:
            return "Estou muito interessado nesta oportunidade e acredito que minhas experiências se alinham perfeitamente com os desafios da vaga."
        
        return resposta_limpa

    except Exception as e:
        print(f"⚠️  Erro ao gerar resposta com IA: {e}")
        # Resposta padrão segura
        return "Estou entusiasmado com a oportunidade e acredito que minhas habilidades em desenvolvimento e automação podem contribuir significativamente para a equipe."

def normalizar_texto(texto):
    """Remove acentos e converte para minúsculo para busca robusta."""
    if not texto: return ""
    # Remove acentos (ex: 'formação' vira 'formacao')
    texto_norm = unicodedata.normalize('NFD', texto)
    texto_norm = texto_norm.encode('ascii', 'ignore').decode('utf-8')
    return texto_norm.lower().strip()

def buscar_correspondencia_like(label_text, input_id, input_name, mapa_keywords):
    """
    Simula o 'LIKE %valor%' do SQL procurando substrings 
    dentro dos atributos do elemento.
    """
    # Normalizamos todos os alvos da busca
    alvos = [
        normalizar_texto(label_text),
        normalizar_texto(input_id),
        normalizar_texto(input_name)
    ]
    
    for chave, sinonimos in mapa_keywords.items():
        for sinonimo in sinonimos:
            # A lógica "LIKE": verifica se o sinônimo está contido em qualquer um dos alvos
            for alvo in alvos:
                if sinonimo in alvo: # Aqui acontece o LIKE '%valor%'
                    return chave
    return None




def preencher_campos_comuns(driver, form):
    """
    Percorre os inputs do formulário e realiza o preenchimento inteligente
    baseado em correspondência de padrões (LIKE).
    """
    # Localiza todos os campos de entrada e áreas de texto no formulário
    inputs = form.find_elements(By.CSS_SELECTOR, "input, textarea")
    
    for campo in inputs:
        # Pula campos ocultos ou já preenchidos
        valor_atual = campo.get_attribute("value") or ""  # Garante string vazia se None
        if not campo.is_displayed() or valor_atual.strip():  # .strip() remove espaços
            continue
            
        # Coleta metadados do campo para a busca "LIKE"
        campo_id = campo.get_attribute("id") or ""
        campo_name = campo.get_attribute("name") or ""
        campo_aria = campo.get_attribute("aria-label") or ""
        
        # Tenta encontrar a label associada ao campo
        label_text = ""
        try:
            if campo_id:
                label = form.find_element(By.CSS_SELECTOR, f"label[for='{campo_id}']")
                label_text = label.text
        except:
            # Fallback: procura label que envolva o input ou esteja próxima (opcional)
            pass

        # Executa a lógica "LIKE" para encontrar qual dado preencher
        # Agora o "LIKE" olha para 4 lugares diferentes
        alvos_texto = f"{label_text} {campo_id} {campo_name} {campo_aria}"
        # Usando a função buscar_correspondencia_like que definimos anteriormente
        chave_encontrada = buscar_correspondencia_like(alvos_texto, campo_id, campo_name, MAPA_KEYWORDS)
        
        if chave_encontrada:
            valor = INFOS_PESSOAIS.get(chave_encontrada)
            
            if valor:
                # Simula digitação humana
                if 'path_cv' == chave_encontrada:
                    # RF010: Upload de currículo
                    campo.send_keys(valor) 
                else:
                    campo.send_keys(valor)
                
                print(f"[OK] Preenchido: {chave_encontrada} no campo '{label_text or campo_id}'")
                time.sleep(random.uniform(1.2, 2.8)) # RNF003: Delay humano

def detectar_form(driver):
    forms = driver.find_elements(By.TAG_NAME, "form")
    for f in forms:
        # Só aceita o formulário se ele estiver visível na tela
        if f.is_displayed():
            return f
    return None
    

def main():
    try:
        # Attach ao Chrome existente
        options = Options()
        options.debugger_address = "127.0.0.1:9222"
        service = Service(ChromeDriverManager().install())
        
        driver = webdriver.Chrome(service=service, options=options)
        
        print("Conectado à sessão do navegador!")
        time.sleep(random.uniform(2, 5))  # Delay simulado

        form = detectar_form(driver)
        if not form:
            return  # Sai se não encontrar
        
        preencher_campos_comuns(driver, form)
        

        input("Pressione Enter para continuar...")  # Mantém aberta
    except Exception as e:
        print(f"Erro: {e}. Verifique Chrome com --remote-debugging-port=9222.")

if __name__ == "__main__":
     main()



