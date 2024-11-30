import psutil
import tkinter as tk
from tkinter import ttk, messagebox
from collections import defaultdict

categorias_monitoradas = {
    "Navegador": ["chrome", "safari", "msedge", "firefox", "opera", "vivaldi", "brave"],
    "Launcher": ["steam", "battle.net", "origin", "riot", "ubisoftconnect", "epicgames"],
    "App de Música": ["spotify", "applemusic", "amazonmusic", "youtubemusic", "deezer", "tidal"],
    "Outros": ["loom", "hamachi"]
}

ordem_categorias = ["Navegador", "Launcher", "App de Música", "Outros"]
processos_selecionados = set()

def listar_processos():
    processos = defaultdict(lambda: {'categoria': None, 'contador': 0})
    for processo in psutil.process_iter(['pid', 'name']):
        try:
            nome_processo = processo.info['name'].lower()
            for categoria, apps in categorias_monitoradas.items():
                if any(app in nome_processo for app in apps):
                    processos[nome_processo]['categoria'] = categoria
                    processos[nome_processo]['contador'] += 1
                    break
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    processos_ordenados = sorted(
        [(nome, dados['categoria'], dados['contador']) for nome, dados in processos.items()],
        key=lambda x: (ordem_categorias.index(x[1]), -x[2], x[0].lower())
    )

    atualizar_treeview(processos_ordenados)
    janela.after(2000, listar_processos)

def atualizar_treeview(processos_ordenados):
    for item in tree.get_children():
        tree.delete(item)
    
    for nome, categoria, contador in processos_ordenados:
        marcador = "Selecionado" if nome in processos_selecionados else ""
        tree.insert("", "end", values=(marcador, categoria, f"{contador} tarefa(s)", nome))

def marcar_deselecionar(event):
    item = tree.focus()
    if not item:
        return
    
    valores = tree.item(item, "values")
    marcador = valores[0]
    nome_processo = valores[3]

    if marcador == "":
        tree.item(item, values=("Selecionado", *valores[1:]))
        processos_selecionados.add(nome_processo)
    else:
        tree.item(item, values=("", *valores[1:]))
        processos_selecionados.discard(nome_processo)

def encerrar_selecionados():
    if not processos_selecionados:
        messagebox.showwarning("Aviso", "Nenhum processo selecionado para encerrar.")
        return

    resposta = messagebox.askyesno("Confirmação", "Tem certeza que deseja encerrar os processos selecionados?")
    if resposta:
        for nome_processo in processos_selecionados.copy():
            try:
                for processo in psutil.process_iter(['pid', 'name']):
                    if nome_processo.lower() in processo.info['name'].lower():
                        processo.terminate()
                        processos_selecionados.discard(nome_processo)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        messagebox.showinfo("Sucesso", "Processos selecionados foram encerrados.")
        listar_processos()

def exibir_ajuda():
    ajuda_texto = (
        "Como usar este App:\n"
        "1. O aplicativo lista todos os processos em execução no seu sistema.\n"
        "2. Para selecionar um processo, dê dois cliques sobre ele.\n"
        "3. Os processos selecionados aparecerão com a marca 'Selecionado'.\n"
        "4. Para encerrar os processos selecionados, basta clicar no botão 'Encerrar Selecionados'.\n\n"
        "Inf. A lista de processos é atualizada automaticamente a cada 2 segundos.\n"
    )
    
    janela_ajuda = tk.Toplevel(janela)
    janela_ajuda.title("Ajuda")
    janela_ajuda.geometry("600x200")
    
    label_ajuda = tk.Label(janela_ajuda, text=ajuda_texto, justify="left", padx=10, pady=10)
    label_ajuda.pack(fill="both", expand=True)

janela = tk.Tk()
janela.title("Gerenciador de Apps, Navegadores, Lançadores e Outros")
janela.geometry("800x500")

tree = ttk.Treeview(janela, columns=("Selecionar", "Categoria", "Tarefas", "Nome do Processo"), show="headings")
tree.heading("Selecionar", text="Selecionar")
tree.heading("Categoria", text="Categoria")
tree.heading("Tarefas", text="Tarefas")
tree.heading("Nome do Processo", text="Nome do Processo")
tree.column("Selecionar", width=120, anchor="center")
tree.pack(fill="both", expand=True)

frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=10)

botao_encerrar_selecionados = tk.Button(frame_botoes, text="Encerrar Selecionados", command=encerrar_selecionados)
botao_encerrar_selecionados.pack(side=tk.LEFT, padx=10)

botao_ajuda = tk.Button(frame_botoes, text="Ajuda", command=exibir_ajuda)
botao_ajuda.pack(side=tk.LEFT, padx=10)

tree.bind("<Double-1>", marcar_deselecionar)

listar_processos()
janela.mainloop()
