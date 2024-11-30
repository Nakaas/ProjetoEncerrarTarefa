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

def encerrar_todos():
    try:
        for processo in psutil.process_iter(['pid', 'name']):
            nome_processo = processo.info['name'].lower()
            for categoria, apps in categorias_monitoradas.items():
                if any(app in nome_processo for app in apps):
                    processo.terminate()
                    break
        messagebox.showinfo("Sucesso", "Todos os processos monitorados foram encerrados.")
        listar_processos()
    except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
        messagebox.showerror("Erro", f"Não foi possível encerrar alguns processos: {e}")

def remover_processo():
    item = tree.focus()
    if item:
        nome_processo = tree.item(item, "values")[3]
        tree.delete(item)
        messagebox.showinfo("Sucesso", f"Processo {nome_processo} removido da lista.")

def remover_categoria():
    item = tree.focus()
    if item:
        categoria = tree.item(item, "values")[1]
        for i in tree.get_children():
            if tree.item(i, "values")[1] == categoria:
                tree.delete(i)
        messagebox.showinfo("Sucesso", f"Categoria {categoria} removida da lista.")

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

tree.bind("<Double-1>", marcar_deselecionar)

frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=10)

botao_encerrar_selecionados = tk.Button(frame_botoes, text="Encerrar Selecionados", command=encerrar_selecionados)
botao_encerrar_selecionados.pack(side=tk.LEFT, padx=10)
botao_encerrar_todos = tk.Button(frame_botoes, text="Encerrar Todos", command=encerrar_todos)
botao_encerrar_todos.pack(side=tk.LEFT, padx=10)
botao_remover_processo = tk.Button(frame_botoes, text="Remover Processo", command=remover_processo)
botao_remover_processo.pack(side=tk.LEFT, padx=10)
botao_remover_categoria = tk.Button(frame_botoes, text="Remover Categoria", command=remover_categoria)
botao_remover_categoria.pack(side=tk.LEFT, padx=10)

listar_processos()
janela.mainloop()
