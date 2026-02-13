import ollama

def testar_ollama():
    try:
        response = ollama.generate(
            model='llama3.2:1b',          # ← Mudança aqui
            prompt="Teste simples: Escreva uma frase motivacional para uma candidatura de emprego."
        )
        print("✅ Ollama com modelo leve funcionando!")
        print("Resposta:", response['response'])
    except Exception as e:
        print("❌ Erro:", e)

if __name__ == "__main__":
    testar_ollama()