from tkinter import ttk
from bot_leo import bot_response
import tkinter as tk

# Insere texto na caixinha de texto
def send_message(event=None):
    user_text = user_entry.get().strip()
    if user_text:
        chat_area.config(state=tk.NORMAL)
        chat_area.insert(tk.END, "Você: " + user_text + "\n\n")
        chat_area.insert(tk.END, "Bot Leo: " + bot_response(user_text) + "\n\n")
        chat_area.config(state=tk.DISABLED)
        chat_area.see(tk.END)
        user_entry.delete(0, tk.END)

# Configuração da window
root = tk.Tk()
root.title("Bot do Zoológico")
root.geometry("700x400-50+50")
root.resizable(False,False)

# Área de chat
chat_area = tk.Text(root, wrap="word", state=tk.DISABLED, width=80, height=20)
chat_area.pack(padx=10, pady=10)

# Entrada de usuário
user_entry = ttk.Entry(root, width=50)
user_entry.pack(side=tk.LEFT, padx=(30,0), pady=(0,10))
user_entry.bind("<Return>", send_message)

# Botão de enviar
send_button = ttk.Button(root, text="Enviar", command=send_message)
send_button.pack(side=tk.LEFT, padx=10, pady=(0,10))

# Mensagem de início
chat_area.config(state=tk.NORMAL)
chat_area.insert(tk.END, "Bot Leo: Olá, sou o Leo e te ajudarei com informações sobre o zoológico Hortus Animalium :)\n\n")
chat_area.config(state=tk.DISABLED)

root.mainloop()