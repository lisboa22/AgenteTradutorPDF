import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import fitz
import os
from googletrans import Translator
import threading
import asyncio

# --- Funções de Extração e Criação de PDF ---

def extrair_texto_do_pdf(caminho_do_arquivo):
    """
    Extrai todo o texto de um arquivo PDF e retorna uma lista de strings.
    
    Args:
        caminho_do_arquivo (str): O caminho para o arquivo PDF.

    Returns:
        list: Uma lista de strings, onde cada string é o texto de uma página.
              Retorna None em caso de erro.
    """
    texto_por_pagina = []
    try:
        documento = fitz.open(caminho_do_arquivo)
        print(f"Lendo documento com {documento.page_count} páginas...")
        for num_pagina in range(documento.page_count):
            pagina = documento.load_page(num_pagina)
            texto = pagina.get_text("text")
            texto_por_pagina.append(texto)
        documento.close()
        return texto_por_pagina
    except Exception as e:
        print(f"Ocorreu um erro ao extrair o texto do PDF: {e}")
        return None

def criar_pdf_traduzido(texto_traduzido, caminho_de_saida):
    """
    Cria um novo documento PDF a partir de uma lista de strings.
    
    Args:
        texto_traduzido (list): A lista de strings com o texto traduzido.
        caminho_de_saida (str): O caminho para salvar o novo arquivo PDF.

    Returns:
        bool: True se o arquivo foi criado com sucesso, False caso contrário.
    """
    try:
        novo_documento = fitz.open()
        print(f"\nCriando o novo PDF traduzido: {caminho_de_saida}")
        for texto in texto_traduzido:
            pagina = novo_documento.new_page(width=595, height=842)
            rect = fitz.Rect(50, 50, 545, 792)
            pagina.insert_text(rect.tl, texto, fontsize=12, fontname="helv", rotate=0)
        novo_documento.save(caminho_de_saida, garbage=4, deflate=True)
        novo_documento.close()
        print(f"\nDocumento traduzido salvo com sucesso em: {caminho_de_saida}")
        return True
    except Exception as e:
        print(f"Ocorreu um erro ao criar o PDF traduzido: {e}")
        return False

# --- Função de Tradução (única opção) ---

async def traduzir_com_googletrans(texto_por_pagina):
    """Traduz uma lista de textos usando a biblioteca googletrans de forma assíncrona."""
    translator = Translator()
    texto_traduzido_por_pagina = []
    print("\nIniciando a tradução com googletrans...")
    try:
        for texto in texto_por_pagina:
            if texto.strip():
                # A função 'translate' é uma corrotina e deve ser aguardada.
                traducao = await translator.translate(texto, src='en', dest='pt')
                texto_traduzido_por_pagina.append(traducao.text)
            else:
                texto_traduzido_por_pagina.append("")
        print("Tradução concluída com sucesso.")
        return texto_traduzido_por_pagina
    except Exception as e:
        print(f"Erro na tradução com googletrans: {e}")
        return None

# --- Interface Gráfica ---

class TradutorPDFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tradutor de PDF")
        self.root.geometry("800x650")
        self.root.protocol("WM_DELETE_WINDOW", self.fechar_programa)

        self.caminho_do_pdf_original = None
        self.texto_por_pagina = None
        self.texto_traduzido = None
        self.traducao_thread = None

        self.caminho_frame = ttk.Frame(root, padding="10")
        self.caminho_frame.pack(fill=tk.X)
        
        self.btn_carregar = ttk.Button(self.caminho_frame, text="Carregar PDF em Inglês", command=self.carregar_pdf)
        self.btn_carregar.pack(side=tk.LEFT, padx=5)

        self.label_caminho = ttk.Label(self.caminho_frame, text="Nenhum arquivo carregado.")
        self.label_caminho.pack(side=tk.LEFT, padx=5)

        # Frame principal para as caixas de texto
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        # Caixa de Texto Original
        self.label_original = ttk.Label(self.main_frame, text="Texto Original (Inglês):")
        self.label_original.pack(fill=tk.X, pady=(10, 0))
        self.texto_original = tk.Text(self.main_frame, height=15, wrap=tk.WORD, state=tk.DISABLED)
        self.texto_original.pack(expand=True, fill=tk.BOTH)

        # Botões de tradução e salvar
        self.traducao_frame = ttk.Frame(self.main_frame)
        self.traducao_frame.pack(fill=tk.X, pady=10)

        self.btn_traduzir = ttk.Button(self.traducao_frame, text="Traduzir Texto", command=self.traduzir_texto)
        self.btn_traduzir.pack(side=tk.LEFT, padx=5)

        self.btn_salvar = ttk.Button(self.traducao_frame, text="Salvar PDF Traduzido", command=self.salvar_pdf_traduzido)
        self.btn_salvar.pack(side=tk.RIGHT, padx=5)

        # Caixa de Texto Traduzida
        self.label_traduzido = ttk.Label(self.main_frame, text="Texto Traduzido (Português):")
        self.label_traduzido.pack(fill=tk.X, pady=(10, 0))
        self.texto_traduzido_widget = tk.Text(self.main_frame, height=15, wrap=tk.WORD, state=tk.DISABLED)
        self.texto_traduzido_widget.pack(expand=True, fill=tk.BOTH)

    def fechar_programa(self):
        """Encerra o programa de forma segura."""
        self.root.destroy()
        self.root.quit()

    def carregar_pdf(self):
        """Abre a janela de diálogo para o usuário selecionar um arquivo PDF."""
        caminho_do_arquivo = filedialog.askopenfilename(
            title="Selecione um arquivo PDF em Inglês",
            filetypes=[("Arquivos PDF", "*.pdf")]
        )
        if caminho_do_arquivo:
            self.caminho_do_pdf_original = caminho_do_arquivo
            self.label_caminho.config(text=os.path.basename(caminho_do_arquivo))
            
            self.texto_por_pagina = extrair_texto_do_pdf(self.caminho_do_pdf_original)
            if self.texto_por_pagina:
                texto_completo = "\n".join(self.texto_por_pagina)
                self.texto_original.config(state=tk.NORMAL)
                self.texto_original.delete("1.0", tk.END)
                self.texto_original.insert(tk.END, texto_completo)
                self.texto_original.config(state=tk.DISABLED)
                messagebox.showinfo("Sucesso", "PDF carregado com sucesso!")
            else:
                messagebox.showerror("Erro", "Não foi possível extrair o texto do PDF.")

    def traduzir_texto(self):
        """Inicia a tradução em uma thread separada para não travar a GUI."""
        if not self.texto_por_pagina:
            messagebox.showwarning("Aviso", "Por favor, carregue um PDF primeiro.")
            return
        
        # Desabilita o botão para evitar cliques múltiplos
        self.btn_traduzir.config(state=tk.DISABLED)
        self.label_traduzido.config(text="Traduzindo... Por favor, aguarde.")

        # Inicia a tradução em uma thread separada
        self.traducao_thread = threading.Thread(target=self._executar_traducao)
        self.traducao_thread.start()

        # Verifica periodicamente se a tradução terminou
        self.root.after(100, self._verificar_traducao_concluida)

    def _executar_traducao(self):
        """Função que será executada na thread de tradução."""
        try:
            # Executa a corrotina de tradução de forma síncrona dentro da thread
            self.texto_traduzido = asyncio.run(traduzir_com_googletrans(self.texto_por_pagina))
        except Exception as e:
            print(f"Erro ao executar a tradução assíncrona: {e}")
            self.texto_traduzido = None

    def _verificar_traducao_concluida(self):
        """Verifica se a thread de tradução terminou e atualiza a GUI."""
        if self.traducao_thread.is_alive():
            # Se a thread ainda estiver rodando, verifica novamente em 100ms
            self.root.after(100, self._verificar_traducao_concluida)
        else:
            # A thread terminou, então atualiza a interface
            self.btn_traduzir.config(state=tk.NORMAL)
            self.label_traduzido.config(text="Texto Traduzido (Português):")

            if self.texto_traduzido:
                texto_completo_traduzido = "\n".join(self.texto_traduzido)
                self.texto_traduzido_widget.config(state=tk.NORMAL)
                self.texto_traduzido_widget.delete("1.0", tk.END)
                self.texto_traduzido_widget.insert(tk.END, texto_completo_traduzido)
                self.texto_traduzido_widget.config(state=tk.DISABLED)
                messagebox.showinfo("Sucesso", "Tradução concluída!")
            else:
                messagebox.showerror("Erro", "A tradução falhou. Verifique os logs do console.")

    def salvar_pdf_traduzido(self):
        """Salva o texto traduzido em um novo arquivo PDF."""
        if not self.texto_traduzido:
            messagebox.showwarning("Aviso", "Por favor, traduza o texto primeiro.")
            return

        nome_original = os.path.basename(self.caminho_do_pdf_original)
        nome_traduzido = f"{os.path.splitext(nome_original)[0]}_traduzido.pdf"
        caminho_de_saida = os.path.join(os.getcwd(), nome_traduzido)
        
        if criar_pdf_traduzido(self.texto_traduzido, caminho_de_saida):
            messagebox.showinfo("Sucesso", f"Arquivo salvo com sucesso em:\n{caminho_de_saida}")
        else:
            messagebox.showerror("Erro", "Não foi possível salvar o arquivo traduzido.")

# --- Execução ---

if __name__ == "__main__":
    root = tk.Tk()
    app = TradutorPDFApp(root)
    root.mainloop()
