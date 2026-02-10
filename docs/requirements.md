# Especificação de Requisitos - AutoJob Bot

Este documento segue as diretrizes da norma **IEEE 830** para especificação de requisitos de software.

## 1. Requisitos Funcionais (RF)
* **[RF001] Ativação via Comando:** O sistema deve iniciar o ciclo de preenchimento ao detectar um comando de entrada específico via CLI.
* **[RF002] Leitura de DOM:** O sistema deve realizar o mapeamento do Document Object Model (DOM) para localizar elementos de formulário (`<form>`).
* **[RF003] Extração de Rótulos:** O sistema deve extrair o texto de etiquetas (`<label>`) e atributos de acessibilidade dos campos identificados.
* **[RF004] Consulta de Base Local:** O sistema deve realizar o *matching* entre os rótulos encontrados e os dados armazenados no arquivo de configuração local.
* **[RF005] Preenchimento de Dados Estáticos:** O sistema deve inserir automaticamente informações como nome, e-mail e telefone caso existam na base local.
* **[RF006] Isolamento de Pendências:** O sistema deve identificar campos sem correspondência local para processamento via Inteligência Artificial.
* **[RF007] Integração com Ollama (IA Local):** O sistema deve enviar o contexto do usuário e a pergunta do formulário para o modelo Ollama local.
* **[RF008] Inserção de Respostas de IA:** O sistema deve capturar a saída da IA e preencher os campos dissertativos correspondentes.
* **[RF009] Gestão de Arquivos:** O sistema deve realizar o upload do currículo (PDF/DOCX) a partir do caminho especificado na configuração.

## 2. Requisitos Não-Funcionais (RNF)
* **[RNF001] Ambiente de Execução:** O sistema deve ser compatível com o sistema operacional Ubuntu.
* **[RNF002] Privacidade de Dados:** Todo o processamento de IA deve ser local (Ollama), sem envio de dados pessoais para nuvens externas.
* **[RNF003] Desempenho:** O tempo de resposta da IA para cada campo não deve exceder 30 segundos.
* **[RNF004] Portabilidade:** O projeto deve ser estruturado em Python utilizando ambientes virtuais (`venv`).