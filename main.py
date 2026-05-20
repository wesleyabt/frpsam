import sys
import os
import traceback
import customtkinter as ctk
from samsung_logic import SamsungADBLogic
import threading
import time
from PIL import Image

class App(ctk.CTk):
    def __init__(self):
        try:
            super().__init__()

            self.title("Samsung ADB Master Tool v15.0 (Force Recognition)")
            self.geometry("950x900")
            
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("blue") 

            self.logic = SamsungADBLogic()
            self.is_monitoring = False

            # Layout
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(4, weight=1)

            # Header
            self.header = ctk.CTkFrame(self, corner_radius=0, fg_color="#1a1a1a")
            self.header.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
            self.title_label = ctk.CTkLabel(self.header, text="Samsung ADB FORCE", font=ctk.CTkFont(size=32, weight="bold"))
            self.title_label.pack(side="left", padx=20, pady=10)
            self.version_label = ctk.CTkLabel(self.header, text="v15.0 (Software Recon)", font=ctk.CTkFont(size=12))
            self.version_label.pack(side="left", pady=(20, 0))

            # Tabview
            self.tabview = ctk.CTkTabview(self)
            self.tabview.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
            self.tabview.add("Bypass & Recon")
            self.tabview.add("MTP Browser")
            self.tabview.add("QR Code Elite")

            # Tab 1: Bypass & Recon
            self.tab1_frame = self.tabview.tab("Bypass & Recon")
            
            self.btn_clean = ctk.CTkButton(self.tab1_frame, text="1. EXECUTAR CLEAN ACTIVATE", fg_color="#CC0000", command=self.start_clean_activate)
            self.btn_clean.pack(pady=10)
            
            self.btn_force = ctk.CTkButton(self.tab1_frame, text="2. FORÇAR RECONHECIMENTO (SOFTWARE)", fg_color="#CC8800", command=self.start_force_recognition)
            self.btn_force.pack(pady=10)
            
            self.btn_monitor = ctk.CTkButton(self.tab1_frame, text="3. INICIAR MONITORAMENTO ADB", fg_color="#006600", command=self.toggle_monitoring)
            self.btn_monitor.pack(pady=10)
            
            self.info_label = ctk.CTkLabel(self.tab1_frame, text="O botão 2 simula a reconexão do cabo via software.", text_color="gray")
            self.info_label.pack(pady=5)

            # Tab 2: MTP Browser
            self.tab2_frame = self.tabview.tab("MTP Browser")
            self.btn_mtp = ctk.CTkButton(self.tab2_frame, text="ABRIR NAVEGADOR (MTP)", fg_color="#0000CC", command=self.start_mtp_browser)
            self.btn_mtp.pack(pady=10)

            # Tab 3: QR Code Elite
            self.tab3_frame = self.tabview.tab("QR Code Elite")
            self.btn_gen_qr = ctk.CTkButton(self.tab3_frame, text="GERAR QR CODE ELITE", command=self.display_qr)
            self.btn_gen_qr.pack(pady=10)
            self.qr_display = ctk.CTkLabel(self.tab3_frame, text="")
            self.qr_display.pack(pady=10)

            # Console
            self.console_frame = ctk.CTkFrame(self, fg_color="#000000")
            self.console_frame.grid(row=4, column=0, sticky="nsew", padx=20, pady=20)
            self.console_frame.grid_columnconfigure(0, weight=1)
            self.console_frame.grid_rowconfigure(1, weight=1)
            self.log_box = ctk.CTkTextbox(self.console_frame, font=ctk.CTkFont(family="Consolas", size=12), text_color="#00FF00")
            self.log_box.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
            self.log_box.configure(state="disabled")
            
        except Exception as e:
            with open("error_log.txt", "a") as f: f.write(traceback.format_exc())

    def log(self, message):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"[SYSTEM] {message}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def start_clean_activate(self):
        self.log("Iniciando Clean Activate...")
        thread = threading.Thread(target=lambda: self.logic.clean_activate_at(self.log))
        thread.daemon = True
        thread.start()

    def start_force_recognition(self):
        self.log("Iniciando Força de Reconhecimento...")
        thread = threading.Thread(target=lambda: self.logic.force_recognition(self.log))
        thread.daemon = True
        thread.start()

    def start_mtp_browser(self):
        self.log("Iniciando Trigger MTP Browser...")
        thread = threading.Thread(target=lambda: self.logic.trigger_mtp_browser(self.log))
        thread.daemon = True
        thread.start()

    def toggle_monitoring(self):
        if not self.is_monitoring:
            self.is_monitoring = True
            self.btn_monitor.configure(text="PARAR MONITORAMENTO", fg_color="#AA0000")
            self.log("Monitoramento ADB iniciado.")
            thread = threading.Thread(target=self.monitor_adb)
            thread.daemon = True
            thread.start()
        else:
            self.is_monitoring = False
            self.btn_monitor.configure(text="INICIAR MONITORAMENTO", fg_color="#006600")
            self.log("Monitoramento ADB parado.")

    def monitor_adb(self):
        while self.is_monitoring:
            result = self.logic.check_adb_devices()
            if "device" in result.lower() and "list of devices attached" not in result.lower().strip():
                self.log("!!! DISPOSITIVO ADB DETECTADO !!!")
                self.log(result)
                self.is_monitoring = False
                self.btn_monitor.configure(text="INICIAR MONITORAMENTO", fg_color="#006600")
                break
            time.sleep(0.1)

    def display_qr(self):
        try:
            self.log("Gerando QR Code Elite...")
            qr_path = self.logic.generate_elite_qr()
            img = Image.open(qr_path)
            img = img.resize((250, 250))
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(250, 250))
            self.qr_display.configure(image=ctk_img, text="")
            self.log("QR Code Elite gerado!")
        except Exception as e:
            self.log(f"Erro: {str(e)}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
