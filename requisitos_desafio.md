# 📋 Análise Completa do Desafio Técnico

---

## 🎯 Desafio Técnico 1: Assistente Virtual de Dados

### Objetivo
Desenvolver um **Assistente Virtual de Dados inteligente** que atue como um analista júnior, respondendo perguntas de negócio de forma independente.

**Foco principal:** Criar um sistema que:
- Não apenas "siga um roteiro"
- Navegue por incertezas
- Busque as próprias respostas em um banco de dados
- **Apresente os resultados visualmente** (gráficos/tabelas)

### Cenário
A diretoria precisa de respostas rápidas sobre operações. Atualmente, cada pergunta exige um engenheiro para escrever SQL manualmente. O sistema deve permitir perguntas em **linguagem natural** e investigar o banco de dados `anexo_desafio_1.db`.

**Exemplos de perguntas esperadas:**
- "Liste os 5 estados com maior número de clientes que compraram via app em maio."
- "Quantos clientes interagiram com campanhas de WhatsApp em 2024?"
- "Quais categorias de produto tiveram o maior número de compras em média por cliente?"
- "Qual o número de reclamações não resolvidas por canal?"
- "Qual a tendência de reclamações por canal no último ano?"

### Recursos Fornecidos
Arquivo SQLite `clientes_completo.db` com a seguinte estrutura:

| Tabela | Colunas |
|--------|---------|
| **clientes** | `id` (INT), `nome` (TEXT), `email` (TEXT), `idade` (INT), `cidade` (TEXT), `estado` (TEXT), `profissao` (TEXT), `genero` (TEXT) |
| **compras** | `id` (INT), `cliente_id` (INT), `data_compra` (TEXT), `valor` (REAL), `categoria` (TEXT), `canal` (TEXT) |
| **suporte** | `id` (INT), `cliente_id` (INT), `data_contato` (TEXT), `tipo_contato` (TEXT), `resolvido` (BOOLEAN), `canal` (TEXT) |
| **campanhas_marketing** | `id` (INT), `cliente_id` (INT), `nome_campanha` (TEXT), `data_envio` (TEXT), `canal` (TEXT), `interagiu` (BOOLEAN) |

### O Que Deve Fazer

#### 1. Motor de Inteligência (Backend Python)
- Receber pergunta do usuário e devolver resposta consultando o banco
- **Robusto** para lidar com:
  - **Perguntas complexas:** múltiplas consultas ou passos intermediários
  - **Erros de execução:** detectar SQL inválido e corrigir automaticamente
  - **Descoberta dinâmica:** entender o schema do banco sem queries hardcoded

#### 2. Interface (Frontend)
- Interface simples (ex: **Streamlit**)
- **Visualização Dinâmica:** exibir dados de forma apropriada (Tabela, Gráfico de Linha/Barra, etc.)
- **"Raciocínio":** transparência sobre como chegou à conclusão (mostrar passos/queries executadas)

### Entregáveis
- Código-fonte em **repositório aberto no GitHub**
- `README.md` contendo:
  - Instruções de execução
  - Explicação do fluxo de agentes e arquitetura escolhida
  - Exemplos de consultas testadas
  - Sugestões de melhorias ou extensões

### Stack Sugerida
- **Python**
- **LangChain / LangGraph**
- **SQLite**
- **Streamlit**

### Prazo
**5 dias corridos** a partir do envio

---

## 🎯 Desafio Técnico 2: Pipeline de Documentos

### Objetivo
Criar uma solução robusta para **ingestão, classificação e extração de informações** a partir de documentos não estruturados. Avaliar capacidade de arquitetar **pipelines de dados integrados com LLMs**, priorizando:
- **Confiabilidade**
- **Manutenibilidade**
- **Eficiência de custos**

### Cenário
A empresa possui um backlog de milhares de documentos digitalizados que precisam ser processados para alimentar o ERP com dados estruturados.

### Arquivos de Entrada
**50 arquivos PDF** fornecidos, simulando documentos digitalizados de 3 tipos:

| Tipo de Documento | Campos a Extrair |
|-------------------|------------------|
| **Nota Fiscal** | Fornecedor, CNPJ, data, lista de itens (descrição, qtd, valor) e valor total |
| **Contrato de Prestação de Serviços** | Partes (contratante/contratado), objeto do contrato, data de vigência e valor mensal |
| **Relatório de Manutenção** | Data, técnico responsável, equipamento, descrição do problema e solução aplicada |

### Pipeline de Processamento
Criar aplicação/script que processe arquivos de `data/raw`:

1. **Ingestão:** Ler os arquivos da pasta de entrada
2. **Classificação:** Identificar automaticamente o tipo de documento
3. **Roteamento:** Direcionar para o fluxo de extração adequado
4. **Extração Estruturada:** Extrair campos específicos de cada tipo (saída em **JSON estrito**)
5. **Persistência:** Salvar dados extraídos (JSON consolidado, CSV ou banco de dados)

### Requisitos Não-Funcionais
- **Eficiência:** Escalável para milhões de documentos, otimizado para latência e custo
- **Robustez:** Não falhar com arquivos anômalos; tratamento de erros adequado
- **Reprodutibilidade:** Resultados consistentes

### Entregáveis
- Código-fonte em **repositório aberto no GitHub**
- `README.md` contendo:
  - Instruções de configuração e execução
  - **Justificativa da Arquitetura:** explicar escolhas técnicas

### Stack Sugerida
- **Python**
- **LangChain / LangGraph**

### Prazo
**5 dias corridos** a partir do envio

---

## 🔍 Análise Estratégica

### Comparação dos Desafios

| Aspecto | Desafio 1 (Assistente Virtual) | Desafio 2 (Pipeline Documentos) |
|---------|--------------------------------|----------------------------------|
| **Foco Principal** | NL2SQL + Visualização | OCR + Extração Estruturada |
| **Tipo de IA** | Agente conversacional | Pipeline de processamento |
| **Frontend** | Obrigatório (Streamlit) | Não mencionado |
| **Complexidade de Dados** | Banco relacional estruturado | PDFs não estruturados |
| **Escala** | Consultas em tempo real | Processamento em batch |
| **Diferencial** | Transparência no raciocínio | Eficiência e robustez |

### Habilidades Avaliadas

**Desafio 1:**
- Desenvolvimento de agentes com LLMs
- Geração de SQL a partir de linguagem natural
- Tratamento de erros e auto-correção
- Visualização de dados
- UX/UI básica

**Desafio 2:**
- Processamento de documentos (OCR)
- Classificação automática de documentos
- Extração de entidades estruturadas
- Arquitetura de pipelines escaláveis
- Tratamento de erros em produção

---
