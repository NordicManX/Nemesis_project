import os
import sys
import time
import shutil
import warnings

# --- DESATIVA AVISOS CHATOS ---
warnings.filterwarnings("ignore")

# --- BIBLIOTECAS DE IA E DADOS ---
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma 
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document

# --- BIBLIOTECAS DE VISÃO E ÁUDIO ---
import pytesseract
from PIL import Image, ImageOps
import fitz  # PyMuPDF
import pandas as pd
import whisper
import numpy as np

# --- CONFIGURAÇÃO ---
NOME_MODELO = "llama3.1"
PASTA_MEMORIA = "./memoria_nemesis_terminal"
CAMINHO_TESSERACT = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Configura OCR
if os.path.exists(CAMINHO_TESSERACT):
    pytesseract.pytesseract.tesseract_cmd = CAMINHO_TESSERACT
    TEM_OCR = True
else:
    TEM_OCR = False
    print("⚠️ AVISO: Tesseract não encontrado. OCR desativado.")

# --- FERRAMENTAS VISUAIS (BARRINHAS DE PROGRESSO FALSAS) ---
def print_status(msg):
    print(f"\033[94m[INFO]\033[0m {msg}")

def print_sucesso(msg):
    print(f"\033[92m[OK]\033[0m {msg}")

def print_erro(msg):
    print(f"\033[91m[ERRO]\033[0m {msg}")

# --- FUNÇÕES DE LEITURA (OCR, AUDIO, EXCEL) ---
def ler_arquivo_multimidia(caminho):
    ext = caminho.split('.')[-1].lower()
    print_status(f"Processando arquivo tipo: .{ext}")
    
    texto = ""
    
    try:
        # 1. IMAGEM
        if ext in ['jpg', 'png', 'jpeg']:
            if not TEM_OCR: return "Erro: OCR não instalado."
            img = Image.open(caminho)
            if np.mean(np.array(img.convert("L"))) < 127: 
                img = ImageOps.invert(img.convert("L"))
            texto = pytesseract.image_to_string(img, lang='por+eng')
            
        # 2. PDF (HÍBRIDO)
        elif ext == 'pdf':
            doc = fitz.open(caminho)
            for pag in doc:
                t = pag.get_text()
                if len(t) < 5 and TEM_OCR: # Se vazio, OCR
                    pix = pag.get_pixmap()
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    t = pytesseract.image_to_string(img, lang='por+eng')
                texto += t + "\n"
            doc.close()
            
        # 3. ÁUDIO (WHISPER)
        elif ext in ['wav', 'mp3']:
            print_status("Carregando modelo auditivo (Whisper)...")
            model = whisper.load_model("base")
            result = model.transcribe(caminho)
            texto = result["text"]
            
        # 4. EXCEL
        elif ext in ['xlsx', 'csv']:
            if ext == 'csv': df = pd.read_csv(caminho)
            else: df = pd.read_excel(caminho)
            texto = df.to_markdown(index=False)
            
        return texto
        
    except Exception as e:
        print_erro(f"Falha ao ler: {e}")
        return None

# --- CÉREBRO (MEMÓRIA) ---
def aprender_arquivo(caminho_arquivo):
    if not os.path.exists(caminho_arquivo):
        print_erro("Arquivo não encontrado!")
        return

    # 1. Extração
    conteudo = ler_arquivo_multimidia(caminho_arquivo)
    if not conteudo or len(conteudo.strip()) < 5:
        print_erro("Arquivo vazio ou ilegível.")
        return

    # 2. Criação do Documento
    doc = Document(
        page_content=f"--- FONTE: {os.path.basename(caminho_arquivo)} ---\n{conteudo}",
        metadata={"source": caminho_arquivo}
    )

    # 3. Chunking (Fatiamento)
    splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    chunks = splitter.split_documents([doc])
    
    print_status(f"Gerados {len(chunks)} fragmentos de memória.")

    # 4. Gravação no Banco (Com Batch Size Fix)
    vectorstore = Chroma(
        collection_name="nemesis_terminal",
        embedding_function=OllamaEmbeddings(model="all-minilm"),
        persist_directory=PASTA_MEMORIA
    )
    
    # Grava em lotes de 4000 para não travar
    BATCH_SIZE = 4000
    for i in range(0, len(chunks), BATCH_SIZE):
        lote = chunks[i : i + BATCH_SIZE]
        vectorstore.add_documents(lote)
        print_status(f"Gravando lote {i} a {i+len(lote)}...")
    
    print_sucesso("Aprendizado concluído!")

# --- MENTE (CONSULTA) ---
def consultar_nemesis(pergunta):
    # Carrega Banco
    vectorstore = Chroma(
        collection_name="nemesis_terminal",
        embedding_function=OllamaEmbeddings(model="all-minilm"),
        persist_directory=PASTA_MEMORIA
    )
    
    # Recupera Contexto
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    docs = retriever.invoke(pergunta)
    
    if not docs:
        return "⚠️ Não tenho memórias sobre isso. Me ensine algo primeiro."

    contexto = "\n\n".join([d.page_content for d in docs])
    
    # Prompt Blindado
    sistema = """
    VOCÊ É O NEMESIS CORE (CLI VERSION).
    Analise os dados técnicos abaixo e responda.
    
    DADOS RECUPERADOS:
    {context}
    
    INSTRUÇÕES:
    1. Se for tabela, analise os números.
    2. Se for transcrição de áudio ou imagem, trate como texto normal.
    3. Seja direto e técnico.
    """
    
    prompt = ChatPromptTemplate.from_template(sistema + "\nPERGUNTA: {question}")
    llm = ChatOllama(model=NOME_MODELO, temperature=0.0)
    chain = prompt | llm
    
    print("\n⚖️  Pensando...", end="", flush=True)
    resposta = chain.invoke({"context": contexto, "question": pergunta})
    return resposta.content

# --- MENU PRINCIPAL ---
if __name__ == "__main__":
    print("\n" + "="*40)
    print("   👁️  NEMESIS CORE v2.0 (TERMINAL)")
    print("="*40)
    
    while True:
        print("\n[1] Aprender Arquivo (PDF/Img/Audio/Excel)")
        print("[2] Consultar")
        print("[3] Limpar Memória")
        print("[0] Sair")
        
        opcao = input("\nEscolha > ")
        
        if opcao == '1':
            caminho = input("Digite o caminho do arquivo (ex: documento.pdf): ").replace('"', '')
            aprender_arquivo(caminho)
            
        elif opcao == '2':
            p = input("Pergunta: ")
            resp = consultar_nemesis(p)
            print("\n" + "-"*50)
            print(resp)
            print("-"*50)
            
        elif opcao == '3':
            confirmar = input("Tem certeza? Isso apaga tudo (s/n): ")
            if confirmar.lower() == 's':
                if os.path.exists(PASTA_MEMORIA):
                    shutil.rmtree(PASTA_MEMORIA)
                    print_sucesso("Memória formatada.")
                else:
                    print_status("Memória já estava vazia.")
                    
        elif opcao == '0':
            print("Encerrando protocolo...")
            break