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

def listar_processos():
    for item in tree.get_children():
        tree.delete(item)

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

    for nome, categoria, contador in processos_ordenados:
        tree.insert("", "end", values=(categoria, f"{contador} tarefa(s)", nome))

def encerrar_tarefa():
    selecionado = tree.selection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um processo para encerrar.")
        return

    nome_processo = tree.item(selecionado[0], 'values')[2]

    try:
        for processo in psutil.process_iter(['pid', 'name']):
            if nome_processo.lower() in processo.info['name'].lower():
                processo.terminate()
        messagebox.showinfo("Sucesso", f"Processo(s) {nome_processo} encerrado(s) com sucesso.")
        listar_processos()
    except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
        messagebox.showerror("Erro", f"Não foi possível encerrar o processo: {e}")

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
    selecionado = tree.selection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um processo para remover.")
        return

    nome_processo = tree.item(selecionado[0], 'values')[2]
    tree.delete(selecionado[0])
    messagebox.showinfo("Sucesso", f"Processo {nome_processo} removido da lista.")

def remover_categoria():
    selecionado = tree.selection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione uma categoria para remover.")
        return
    
    categoria = tree.item(selecionado[0], 'values')[0]
    
    for item in tree.get_children():
        if tree.item(item, 'values')[0] == categoria:
            tree.delete(item)
    
    messagebox.showinfo("Sucesso", f"Categoria {categoria} removida da lista.")

janela = tk.Tk()
janela.title("Gerenciador de Apps, Navegadores, Lançadores e Outros")
janela.geometry("700x400")

tree = ttk.Treeview(janela, columns=("Categoria", "Tarefas", "Nome do Processo"), show="headings")
tree.heading("Categoria", text="Categoria")
tree.heading("Tarefas", text="Tarefas")
tree.heading("Nome do Processo", text="Nome do Processo")
tree.pack(fill="both", expand=True)

frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=10)

frame_botao1 = tk.Frame(frame_botoes)
frame_botao1.pack(side=tk.LEFT, padx=20)
botao_atualizar = tk.Button(frame_botao1, text="Atualizar", command=listar_processos)
botao_atualizar.pack(side=tk.LEFT, padx=10)
botao_remover = tk.Button(frame_botao1, text="Remover Processo", command=remover_processo)
botao_remover.pack(side=tk.LEFT, padx=10)
botao_remover_categoria = tk.Button(frame_botao1, text="Remover Categoria", command=remover_categoria)
botao_remover_categoria.pack(side=tk.LEFT, padx=10)

frame_botao2 = tk.Frame(frame_botoes)
frame_botao2.pack(side=tk.LEFT, padx=20)
botao_encerrar = tk.Button(frame_botao2, text="Encerrar Tarefa", command=encerrar_tarefa)
botao_encerrar.pack(side=tk.LEFT, padx=10)
botao_encerrar_todos = tk.Button(frame_botao2, text="Encerrar Todos", command=encerrar_todos)
botao_encerrar_todos.pack(side=tk.LEFT, padx=10)

listar_processos()
janela.mainloop()
