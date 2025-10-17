# Watsonx-Analyst---IBM-Annual-Report-2024

# WatsonX Analyst: Assistente de IA para Análise de Relatórios Corporativos

Este repositório contém o código-fonte do "WatsonX Analyst", um assistente de IA interativo projetado para analisar e responder a perguntas complexas sobre documentos corporativos densos, utilizando o Relatório Anual de 2024 da IBM como fonte de conhecimento.

O projeto foi desenvolvido como uma demonstração prática de habilidades em IA Generativa, com foco no ecossistema da IBM, para o processo seletivo de Especialista em GenAI.

**Autor:** Marlon ([Link para seu LinkedIn])

---

## 📸 Demonstração da Interface

A aplicação possui uma interface web interativa construída com Gradio, permitindo que qualquer usuário faça perguntas em linguagem natural.
<img width="1579" height="669" alt="Captura de tela 2025-10-17 103951" src="https://github.com/user-attachments/assets/1c2e8d4f-968b-44be-b38e-73ab7f514c5c" />


---

## 🎯 Objetivo do Projeto

O objetivo principal é resolver um problema de negócio comum: a extração rápida e precisa de insights estratégicos a partir de documentos longos e não estruturados. Em vez de horas de leitura manual, um analista pode obter respostas para perguntas sobre finanças, estratégia e riscos em segundos.

---

## 🛠️ Stack Tecnológica

Este projeto utiliza uma stack moderna focada no ecossistema de IA da IBM:

* **Plataforma de IA:** IBM watsonx.ai
* **LLM (Modelo de Linguagem):** `ibm/granite-34b-instruct`
* **Modelo de Embedding:** `ibm/slate-30m-eng`
* **Framework de Orquestração:** LangChain
* **Banco de Dados Vetorial:** ChromaDB (com persistência em disco)
* **Interface de Usuário:** Gradio
* **Linguagem:** Python 3.10


---

## 🏗️ Arquitetura: Geração Aumentada por Recuperação (RAG)

O projeto é implementado com uma arquitetura RAG, que funciona em duas fases:

1.  **Fase de Indexação (Offline):**
    * O PDF do Relatório Anual da IBM é carregado.
    * O texto é dividido em pedaços de texto menores (chunks).
    * O modelo de embedding **IBM Slate** converte cada chunk em um vetor numérico.
    * Esses vetores são armazenados e indexados no **ChromaDB** e salvos em disco para execuções futuras.

2.  **Fase de Inferência (Tempo Real):**
    * O usuário envia uma pergunta através da interface Gradio.
    * A pergunta é convertida em um vetor.
    * O ChromaDB realiza uma busca por similaridade para encontrar os chunks mais relevantes do relatório.
    * Os chunks recuperados (contexto) e a pergunta original são enviados ao LLM **IBM Granite**.
    * O LLM gera uma resposta baseada no contexto fornecido, que é então exibida ao usuário.

---

## 🚀 Como Executar o Projeto Localmente

Siga os passos abaixo para configurar e executar a aplicação em seu ambiente.

### 1. Pré-requisitos
* Python 3.10 ou superior.
* Uma conta na IBM Cloud com acesso ao watsonx.ai.

### 2. Clonar o Repositório
```bash
git clone [URL-DO-SEU-REPOSITÓRIO-AQUI]
cd [NOME-DA-PASTA-DO-REPOSITÓRIO]
