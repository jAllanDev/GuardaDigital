from tkinter import ttk
from bot_leo import bot_response, quick_fraud_check
import tkinter as tk

# Insere texto na caixinha de texto
def send_message(event=None):
    user_text = user_entry.get().strip()
    if user_text:
        chat_area.config(state=tk.NORMAL)
        
        # Adiciona cor diferente se for mensagem de alto risco
        if quick_fraud_check(user_text):
            chat_area.insert(tk.END, "🚨 Você (MENSAGEM SUSPEITA): " + user_text + "\n\n", "warning")
        else:
            chat_area.insert(tk.END, "Você: " + user_text + "\n\n")
        
        bot_reply = bot_response(user_text)
        chat_area.insert(tk.END, "🛡️ GuardaDigital: " + bot_reply + "\n\n", "bot_response")
        chat_area.config(state=tk.DISABLED)
        chat_area.see(tk.END)
        user_entry.delete(0, tk.END)

# Configuração da window
root = tk.Tk()
root.title("GuardaDigital - Detector de Golpes e Fraudes")
root.geometry("900x500-50+50")
root.resizable(True, True)

# Configuração de cores para diferentes tipos de mensagem
style = ttk.Style()
style.theme_use('clam')

# Área de chat com scroll
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

chat_area = tk.Text(frame, wrap="word", state=tk.DISABLED, width=100, height=25, font=("Arial", 10))
scrollbar = tk.Scrollbar(frame, command=chat_area.yview)
chat_area.config(yscrollcommand=scrollbar.set)

# Tags para colorir diferentes tipos de mensagem
chat_area.tag_config("warning", foreground="red", font=("Arial", 10, "bold"))
chat_area.tag_config("bot_response", foreground="blue", font=("Arial", 10))

chat_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Frame para entrada e botão
input_frame = tk.Frame(root)
input_frame.pack(fill=tk.X, padx=10, pady=(0,10))

# Label explicativo
info_label = tk.Label(input_frame, text="Cole aqui mensagens suspeitas ou faça perguntas sobre segurança digital:", 
                     font=("Arial", 9), fg="gray")
info_label.pack(anchor="w")

# Entrada de usuário
user_entry = ttk.Entry(input_frame, width=80, font=("Arial", 10))
user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=5)
user_entry.bind("<Return>", send_message)

# Botão de enviar
send_button = ttk.Button(input_frame, text="Analisar", command=send_message)
send_button.pack(side=tk.RIGHT, padx=(10,0), pady=5)

# Mensagem de início
chat_area.config(state=tk.NORMAL)
welcome_msg = """🛡️ GuardaDigital: Olá! Sou o GuardaDigital, seu assistente de segurança digital!

Estou aqui para ajudar você a:
• Detectar golpes e fraudes
• Analisar mensagens suspeitas
• Ensinar sobre segurança digital
• Prevenir tentativas de phishing

Como usar:
• Digite "Isso é golpe?" seguido da mensagem suspeita
• Faça perguntas sobre segurança digital
• Compartilhe mensagens que recebeu para análise

Exemplo: "Isso é golpe? Me passe seu e-mail para confirmar a compra"

Estou aqui para proteger você! 🛡️

"""
chat_area.insert(tk.END, welcome_msg, "bot_response")
chat_area.config(state=tk.DISABLED)

root.mainloop()