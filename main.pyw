import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
from PIL import Image, ImageTk
import socket
import pyperclip
import threading
import os
import pyautogui
import webbrowser
import sys
import time
import platform

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)

ARCH_BITS = platform.architecture()[0]

class ServerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BLUESCAN - Leitor Avançado")
        self.root.geometry("480x620")
        self.root.configure(bg="#171d23")
        self.root.resizable(False, False)

        self.icon_path = resource_path("assets/ICON.ico")
        self.image_path = resource_path("assets/LOGO.png")
        try:
            self.root.iconbitmap(self.icon_path)
        except:
            pass

        self.server_ip = "0.0.0.0"
        self.server_port = 65432
        self.server_socket = None
        self.server_thread = None
        self.running = False

        self.auto_paste_enabled = tk.IntVar(value=0)
        self.enter_auto_enabled = tk.IntVar(value=0)
        self.modo_entrada = tk.StringVar(value="paste")
        self.typing_delay_ms = tk.IntVar(value=5)
        self.code_counter = 2

        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("TNotebook", background="#171d23", borderwidth=0)
        self.style.configure("TNotebook.Tab", background="#171d23", foreground="white", padding=[10,5])
        self.style.map("TNotebook.Tab", background=[("selected", "#1d252c")], foreground=[("selected","white")])
        self.style.configure("Dark.TFrame", background="#171d23")
        self.style.configure("Dark.TCheckbutton", background="#171d23", foreground="white")

        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        arch_info = f"Plataforma: {platform.system()} {ARCH_BITS}"
        self.log_message(arch_info)

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root, style="TNotebook")
        self.notebook.pack(expand=True, fill=tk.BOTH)

        self.tab_leitor = ttk.Frame(self.notebook, style="Dark.TFrame")
        self.notebook.add(self.tab_leitor, text="Leitor")

        try:
            logo_img = Image.open(self.image_path)
            logo_img = logo_img.resize((360,100), Image.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_img)
            self.logo_label = tk.Label(self.tab_leitor, image=self.logo_photo, bg="#171d23")
        except:
            self.logo_label = tk.Label(self.tab_leitor, text="Leitor Avançado", bg="#171d23", fg="white", font=("Helvetica",16,"bold"))
        self.logo_label.pack(pady=14)

        button_frame = tk.Frame(self.tab_leitor, bg="#171d23")
        button_frame.pack(pady=8)

        self.btn_start = tk.Button(button_frame, text="INICIAR", command=self.start_server, width=12, bg="#5992fc", borderwidth=0, font=("Helvetica",10,"bold"), fg="white")
        self.btn_start.pack(side=tk.LEFT, padx=6)

        self.btn_stop = tk.Button(button_frame, text="PARAR", command=self.stop_server, state=tk.DISABLED, width=12, bg="#5992fc", borderwidth=0, font=("Helvetica",10,"bold"), fg="white")
        self.btn_stop.pack(side=tk.LEFT, padx=6)

        self.btn_port = tk.Button(button_frame, text="PORTA", command=self.change_port, width=12, bg="#5992fc", borderwidth=0, font=("Helvetica",10,"bold"), fg="white")
        self.btn_port.pack(side=tk.LEFT, padx=6)

        self.log_text = scrolledtext.ScrolledText(self.tab_leitor, width=60, height=16, bg="#28333b", fg="white")
        self.log_text.pack(pady=10)
        self.log_text.insert(tk.END, "Log de códigos de barras copiados:\n")
        self.log_text.configure(state=tk.DISABLED)

        self.chk_auto_paste = ttk.Checkbutton(self.tab_leitor, text="Colagem / Entrada Automática", variable=self.auto_paste_enabled, command=self.toggle_enter_auto, style="Dark.TCheckbutton")
        self.chk_auto_paste.pack()

        self.chk_enter_auto = ttk.Checkbutton(self.tab_leitor, text="Enter Automático", variable=self.enter_auto_enabled, state=tk.DISABLED, style="Dark.TCheckbutton")
        self.chk_enter_auto.pack(pady=2)

        self.btn_clear_log = tk.Button(self.tab_leitor, text="LIMPAR LOG", command=self.clear_log, bg="#ff9800", borderwidth=0, font=("Helvetica",10,"bold"), fg="white")
        self.btn_clear_log.pack(pady=10)

        self.tab_config = ttk.Frame(self.notebook, style="Dark.TFrame")
        self.notebook.add(self.tab_config, text="Configurações")

        tk.Label(self.tab_config, text="CONFIGURAÇÕES DO PROGRAMA:", bg="#171d23", fg="white").pack(padx=12, pady=8)

        mode_frame = tk.LabelFrame(self.tab_config, text="Modo de Entrada", bg="#171d23", fg="white", bd=0)
        mode_frame.pack(padx=12, pady=8, fill="x")

        tk.Radiobutton(mode_frame, text="Colar (CTRL+V)", variable=self.modo_entrada, value="paste", bg="#171d23", fg="white", selectcolor="#171d23").pack(anchor="w", padx=8, pady=4)
        tk.Radiobutton(mode_frame, text="Digitação Normal (pyautogui)", variable=self.modo_entrada, value="pytype", bg="#171d23", fg="white", selectcolor="#171d23").pack(anchor="w", padx=8, pady=4)

        delay_frame = tk.Frame(self.tab_config, bg="#171d23")
        delay_frame.pack(padx=12, pady=6, fill="x")

        tk.Label(delay_frame, text="Delay por caractere no modo digitação:", bg="#171d23", fg="white").pack(side=tk.LEFT, padx=(0,6))
        self.spn_delay = tk.Spinbox(delay_frame, from_=0, to=200, width=6, textvariable=self.typing_delay_ms)
        self.spn_delay.pack(side=tk.LEFT)

        self.tab_guia = ttk.Frame(self.notebook, style="Dark.TFrame")
        self.notebook.add(self.tab_guia, text="Guia")

        guide_text = """                                             
FUNÇÕES BLUESCAN:

Iniciar:
Inicia o servidor que escuta conexões na porta especificada.

Parar:
Para o servidor.

Porta:
Permite alterar a porta na qual o servidor escuta as conexões.

Colagem Automática:
Cola automaticamente o código escaneado.

Enter Automático:
Após a colagem, o ENTER é apertado em seguida.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CONFIGURAÇÃO DO DWDEMO (COLETOR):

1- Abra o DWDEMO.
2- Escolha seu método de leitura. (Recomendamos o 2D Scan)
3- Nas configurações, vá para IP OUTPUT/ADRESS e coloque o IPv4 abaixo.
"""
        tk.Label(self.tab_guia, text=guide_text, justify=tk.LEFT, bg="#171d23", fg="white").pack(padx=12, pady=12)

        self.ipv4_label = tk.Label(self.tab_guia, text=f"Endereço IPv4: {self.get_ipv4()}", font=("Helvetica",12), bg="#171d23", fg="white")
        self.ipv4_label.pack(padx=12, pady=8)

        self.tab_sobre = ttk.Frame(self.notebook, style="Dark.TFrame")
        self.notebook.add(self.tab_sobre, text="Sobre")

        tk.Label(self.tab_sobre, text="BLUESCAN - Leitor Avançado : Versão 2.0", bg="#171d23", fg="white").pack(padx=12, pady=12)
        self.btn_whatsapp = tk.Button(self.tab_sobre, text="ENTRE EM CONTATO", command=self.show_whatsapp_popup, width=20, bg="#0cc042", borderwidth=0, font=("Helvetica",10,"bold"), fg="white")
        self.btn_whatsapp.pack(pady=10)

    def get_ipv4(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("10.255.255.255", 1))
            ipv4 = s.getsockname()[0]
        except:
            ipv4 = "127.0.0.1"
        try:
            s.close()
        except:
            pass
        return ipv4

    def start_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.server_ip, self.server_port))
            self.server_socket.listen(1)
            self.running = True
            self.server_thread = threading.Thread(target=self.listen_for_connections, daemon=True)
            self.server_thread.start()
            self.clear_log()
            self.log_message("Servidor iniciado. Aguardando conexões...", "orange")
            self.btn_start.config(state=tk.DISABLED)
            self.btn_stop.config(state=tk.NORMAL)
            self.btn_port.config(state=tk.DISABLED)
        except Exception as e:
            self.log_message(f"Erro ao iniciar o servidor: {e}", "orange")

    def stop_server(self):
        self.running = False
        try:
            if self.server_socket:
                self.server_socket.close()
        except:
            pass
        self.log_message("Servidor parado.", "orange")
        self.btn_start.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)
        self.btn_port.config(state=tk.NORMAL)

    def listen_for_connections(self):
        while self.running:
            try:
                client_socket, _ = self.server_socket.accept()
                self.handle_client(client_socket)
            except:
                break

    def handle_client(self, client_socket):
        with client_socket:
            while self.running:
                try:
                    data = client_socket.recv(8192)
                    if not data:
                        break
                    text = data.decode("utf-8", errors="replace")
                    self.process_data(text)
                except:
                    break

    def process_data(self, data):
        self.log_message(f"Linha {self.code_counter} - Dados recebidos: {data}")
        self.code_counter += 1

        if not self.auto_paste_enabled.get():
            return

        mode = self.modo_entrada.get()
        delay = max(0.0, float(self.typing_delay_ms.get()) / 1000.0)

        try:
            if mode == "paste":
                pyperclip.copy(data)
                time.sleep(0.02)
                pyautogui.hotkey("ctrl", "v")
            elif mode == "pytype":
                pyautogui.write(data, interval=delay)

            if self.enter_auto_enabled.get():
                time.sleep(0.02)
                pyautogui.press("enter")

        except Exception as e:
            self.log_message(f"Erro ao enviar dados: {e}")

    def log_message(self, message, tag=None):
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state=tk.DISABLED)

    def clear_log(self):
        self.code_counter = 2
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.insert(tk.END, "Log de códigos de barras copiados:\n")
        self.log_text.configure(state=tk.DISABLED)

    def change_port(self):
        if self.running:
            messagebox.showinfo("Informação", "Pare o servidor antes de alterar a porta.")
            return
        new_port = simpledialog.askinteger("Alterar Porta", "Digite a nova porta:", initialvalue=self.server_port)
        if new_port:
            self.server_port = new_port
            self.log_message(f"Porta alterada para: {self.server_port}")

    def toggle_enter_auto(self):
        if self.auto_paste_enabled.get():
            self.chk_enter_auto.config(state=tk.NORMAL)
        else:
            self.chk_enter_auto.config(state=tk.DISABLED)

    def show_whatsapp_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("WhatsApp")
        popup.geometry("250x100")
        popup.configure(bg="#171d23")

        label = tk.Label(popup, text="(22) 97404-0083", bg="#171d23", fg="white", font=("Helvetica",12,"bold"))
        label.pack(pady=15)

        btn = tk.Button(popup, text="Enviar Mensagem", command=lambda: self.send_message_and_close(popup), bg="#0cc042", fg="white", borderwidth=0)
        btn.pack(pady=5)

    def send_message_and_close(self, popup):
        webbrowser.open("https://wa.me/5522974040083?text=Olá!%20Estou%20usando%20o%20Leitor%20Avançado%20e%20preciso%20de%20ajuda!")
        popup.destroy()

    def on_close(self):
        if messagebox.askyesno("Sair", "Deseja fechar o aplicativo?"):
            if self.running:
                self.stop_server()
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ServerApp(root)
    root.mainloop()
