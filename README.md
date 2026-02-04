# Document Processing Pipeline (Desafio 2)

Este projeto implementa um pipeline de processamento de documentos para ingestão, classificação e extração de dados estruturados a partir de PDFs (Notas Fiscais, Contratos e Relatórios de Manutenção), utilizando Python e Google Gemini.

## 📋 Funcionalidades

1.  **Ingestão**: Leitura automática de arquivos PDF na pasta `data/raw`.
2.  **Classificação**: Identificação do tipo de documento via LLM (Invoice, Contract, Maintenance Report).
3.  **Extração**: Conversão de dados não estruturados para JSON estruturado usando Schemas Pydantic.
4.  **Persistência**: Salvamento dos resultados em `data/processed`.

## 🛠️ Tecnologias

-   **Python 3.10+**
-   **LangChain**: Orquestração e Chains.
-   **Google Gemini (via langchain-google-genai)**: Modelo LLM para classificação e extração (Versão `gemini-2.5-flash`).
-   **Pydantic**: Validação de dados e Schemas.
-   **pypdf**: Extração de texto de PDFs.

## 🚀 Como Executar

### 1. Configuração do Ambiente

Crie um ambiente virtual e instale as dependências:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate
pip install -r requirements.txt
```

### 2. Variáveis de Ambiente

Renomeie o arquivo `.env.example` para `.env` e adicione sua chave de API do Google Gemini:

```ini
GOOGLE_API_KEY=sua_chave_aqui
```

### 3. Execução

Coloque seus arquivos PDF na pasta `data/raw`. O projeto já inclui 50 arquivos de exemplo.

Execute o pipeline:

```bash
python main.py
```

Os resultados serão salvos na pasta `data/processed` em formato JSON.

## 🏗️ Arquitetura

O pipeline segue um fluxo linear simples e robusto:

1.  **Ingestor**: Varre o diretório e extrai texto bruto.
2.  **Classifier**: O LLM recebe o texto e determina o tipo do documento.
3.  **Extractor**: Com base no tipo, uma chain específica é acionada para extrair os campos definidos nos modelos Pydantic.
4.  **Main Loop**: Itera sobre todos os documentos e trata erros individualmente, garantindo que um arquivo corrompido não pare o processo.
