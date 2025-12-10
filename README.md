# ⚖️ NEMESIS AI PROJECT 

> **Inteligência Jurídica Soberana & Multimodal**
> *Roda 100% Local. Sem nuvem. Sem custos por token.*

O **Nemesis AI** é um sistema de RAG (Retrieval-Augmented Generation) avançado, projetado para escritórios de advocacia e departamentos jurídicos que exigem privacidade total. Ele processa documentos, áudios, imagens e planilhas localmente usando o poder do **Llama 3.1**, **OpenAI Whisper** e **Tesseract OCR**.

---

## 🚀 Funcionalidades Principais

### 🧠 Cérebro & Processamento
* **Ingestão Multimodal:** Lê e cruza dados de:
    * 📄 **PDFs:** Nativos (texto digital) e Digitalizados (OCR Híbrido com PyMuPDF).
    * 🖼️ **Imagens:** JPG, PNG (OCR com pré-processamento para Dark Mode/Contraste).
    * 🎧 **Áudio:** WAV, MP3 (Transcrição offline de alta precisão via Whisper Base).
    * 📊 **Planilhas:** XLSX, CSV (Análise de dados tabulares via Pandas).
* **Correção de Big Data:** Sistema de "Batch Processing" para ingerir planilhas gigantes (+10k linhas) sem estourar a memória do banco vetorial (limite de 5461 tokens do ChromaDB contornado).
* **Prompt Anti-Recusa:** Engenharia de prompt "Jailbreak" que impede a IA de dizer "não vejo imagens", forçando a análise técnica da transcrição OCR.

### 🖥️ Interface & UX (Streamlit)
* **Visual Premium:** Layout estilo "Gemini/ChatGPT" com tema escuro e responsivo.
* **Gestão de Casos:**
    * Menu contextual (⋮) para cada caso.
    * 📌 **Fixar** casos prioritários no topo.
    * ✏️ **Renomear** pastas de casos.
    * 🗑️ **Soft Delete (Lixeira Inteligente):** Sistema de exclusão segura que evita o erro `[WinError 32]` do Windows, ocultando o caso visualmente e limpando o disco apenas na reinicialização do app.
* **Feedback Visual:** Indicador de "Foco Ativo" e Debug de texto bruto para auditoria do que o robô leu.

### 📝 Saída
* **Gerador de Peças:** Botão automático para baixar a resposta da IA formatada em documento **Word (.docx)** pronto para edição.

---

## 🛠️ Pré-requisitos de Sistema

Antes de rodar o Python, seu computador precisa ter estas ferramentas instaladas:

1.  **Ollama** (O Motor da IA)
    * Instale e rode no terminal: `ollama run llama3.1`
2.  **Tesseract OCR** (Para ler imagens/PDFs escaneados)
    * Baixe a versão Windows (UB-Mannheim).
    * **Importante:** Instale no caminho padrão `C:\Program Files\Tesseract-OCR`. O Nemesis busca esse caminho automaticamente.
3.  **FFmpeg** (Para o módulo de Áudio/Whisper)
    * Instale via Chocolatey (PowerShell Admin): `choco install ffmpeg`
    * Ou baixe o binário e adicione ao PATH do Windows manualmente.

---

## 📦 Instalação

1.  **Crie seu ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

2.  **Instale as dependências do projeto:**
    ```bash
    pip install streamlit langchain-community langchain-chroma langchain-ollama chromadb
    pip install pytesseract pymupdf Pillow
    pip install openai-whisper pandas openpyxl python-docx tabulate
    pip install SpeechRecognition
    ```

## ▶️ Como Rodar

No terminal, dentro da pasta do projeto onde está o arquivo `nemesis_app.py`:

```bash
streamlit run nemesis_app.py
```

# 📚 Guia de Uso Rápido

## 1. Criando um Caso
Use a barra lateral para criar um **"Novo Caso"** (ex: `Cliente_Silva`).
> O sistema cria automaticamente um banco de dados vetorial isolado para este cliente na pasta `./banco_de_dados_nemesis`.

## 2. Ingestão de Arquivos
No painel central, expanda a seção **"📎 Anexar"**.
1.  **Arraste** PDFs, Imagens, Áudios ou Excel.
2.  Clique em **Processar**.
3.  **Aguarde:** O sistema fará OCR, transcrição de áudio e indexação vetorial.
4.  **Debug:** Verifique a caixa *"👁️ Ver Dados Brutos"* para confirmar o texto exato que o robô extraiu.

## 3. O Interceptador de Perguntas
Ao perguntar *"O que tem na imagem?"* ou *"Resuma o áudio"*, o Nemesis intercepta sua pergunta e envia para a IA:
> *"O usuário quer saber o conteúdo visual/auditivo. Use a transcrição abaixo como se fosse a mídia real."*

Isso garante que o **Llama 3.1** responda tecnicamente sem alucinações de recusa ("Não tenho olhos").

## 4. Exportação
Após a resposta da IA, clique no botão **"📄 Baixar Resposta em Word"** que aparece logo abaixo do texto para salvar a minuta.

---

## 🔧 Solução de Problemas Comuns

| Erro | Causa Provável | Solução |
| :--- | :--- | :--- |
| **WinError 32 (Arquivo em uso)** | O Windows bloqueou a exclusão da pasta do banco de dados (SQLite travado). | **Resolvido na v10.2.** O Nemesis usa o *Soft Delete*. O caso sumiu da tela? Está resolvido. O arquivo físico será apagado automaticamente na próxima vez que você abrir o app. |
| **ValueError: Batch size > 5461** | Você subiu um Excel muito grande. | **Resolvido na v18.1.** O sistema agora fatia a gravação em lotes de 4000 linhas automaticamente. |
| **TesseractNotFoundError** | O executável não está no PATH ou não foi instalado. | Verifique se instalou em `C:\Program Files\Tesseract-OCR`. O código está chumbado para buscar lá. |
| **FileNotFoundError (Whisper)** | Faltou o FFmpeg no sistema. | Instale o FFmpeg no Windows (`choco install ffmpeg`) e reinicie o terminal. |
| **IA diz "Não vejo imagem"** | O OCR falhou ou a imagem está vazia/preta. | Verifique a aba *"👁️ Ver Dados Brutos"*. Se estiver vazia, a imagem tem baixa qualidade. Se tiver texto, a IA responderá. |

---

## 🏗️ Estrutura do Código (Monolito)

O arquivo `nemesis_app.py` contém toda a lógica condensada para facilitar a portabilidade:

* **Configuração:** Detecção automática de caminhos e drivers.
* **Frontend:** Interface Streamlit com CSS customizado (Dark Mode).
* **Backend Visão:** OCR Tesseract + PyMuPDF (Lógica Híbrida).
* **Backend Áudio:** Whisper (OpenAI Local - Modelo Base).
* **Backend Dados:** Pandas + Tabulate (Conversão Markdown).
* **Core RAG:** ChromaDB + LangChain + Ollama (Llama 3.1).

---

> **Desenvolvido por Nelson Carvalho & Nemesis Team**
>
> *Versão v18.1 - Stable Build*
---

