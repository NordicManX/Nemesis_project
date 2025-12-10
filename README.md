# ⚖️ NEMESIS AI PROJECT (Monolith v1.0)

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

---

## ▶️ Como Rodar

No terminal, dentro da pasta do projeto onde está o arquivo `nemesis_app.py`:

```bash
streamlit run nemesis_app.py
