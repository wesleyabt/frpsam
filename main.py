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

            self.title("Samsung ADB Master - v2.0")
            self.geometry("1000x950")
            
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("blue") 

            self.logic = SamsungADBLogic()
            self.is_monitoring = False

            # Layout
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(2, weight=1)

            # ═══════════════════════════════════════════════════════════
            # HEADER
            # ═══════════════════════════════════════════════════════════
            self.header = ctk.CTkFrame(self, corner_radius=0, fg_color="#0a0e27")
            self.header.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
            self.header.grid_columnconfigure(0, weight=1)
            
            self.title_label = ctk.CTkLabel(
                self.header, 
                text="🔧 SAMSUNG ADB MASTER v2.0", 
                font=ctk.CTkFont(size=28, weight="bold"),
                text_color="#00FF00"
            )
            self.title_label.pack(side="left", padx=30, pady=15)
            
            self.subtitle_label = ctk.CTkLabel(
                self.header, 
                text="Enable ADB • Force Recognition • Remove Google Account", 
                font=ctk.CTkFont(size=11),
                text_color="#888888"
            )
            self.subtitle_label.pack(side="left", padx=30)

            # ═══════════════════════════════════════════════════════════
            # INSTRUCOES
            # ═══════════════════════════════════════════════════════════
            self.instructions_frame = ctk.CTkFrame(self, fg_color="#1a1f3a", corner_radius=10)
            self.instructions_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=15)
            self.instructions_frame.grid_columnconfigure(0, weight=1)
            
            instruction_text = """INSTRUÇÕES RÁPIDAS:
1️⃣  Conecte o celular Samsung via USB
2️⃣  Abra no celular: Discador → *#0*# (Modo de Teste)
3️⃣  Clique em "▶ EXECUTAR FLUXO COMPLETO" abaixo
4️⃣  No celular: Autorize "Permitir depuração USB" quando solicitado
5️⃣  Aguarde a conclusão automática"""

            self.instructions_label = ctk.CTkLabel(
                self.instructions_frame,
                text=instruction_text,
                font=ctk.CTkFont(size=11),
                text_color="#CCCCCC",
                justify="left"
            )
            self.instructions_label.pack(padx=20, pady=15)

            # ═══════════════════════════════════════════════════════════
            # BOTOES PRINCIPAIS
            # ═══════════════════════════════════════════════════════════
            self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
            self.button_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=15)
            self.button_frame.grid_columnconfigure(0, weight=1)

            # Botão GRANDE - Fluxo Completo
            self.btn_full_workflow = ctk.CTkButton(
                self.button_frame, 
                text="▶ EXECUTAR FLUXO COMPLETO", 
                fg_color="#00AA00",
                hover_color="#00DD00",
                text_color="#000000",
                font=ctk.CTkFont(size=16, weight="bold"),
                height=60,
                command=self.start_full_workflow
            )
            self.btn_full_workflow.grid(row=0, column=0, sticky="ew", pady=10)

            # Botões secundários em linha
            self.secondary_frame = ctk.CTkFrame(self.button_frame, fg_color="transparent")
            self.secondary_frame.grid(row=1, column=0, sticky="ew", pady=10)
            self.secondary_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="equal")

            self.btn_enable_adb = ctk.CTkButton(
                self.secondary_frame, 
                text="1. Habilitar ADB", 
                fg_color="#1f1f3f",
                hover_color="#2f2f5f",
                text_color="#00FF00",
                font=ctk.CTkFont(size=12, weight="bold"),
                height=45,
                command=self.start_enable_adb
            )
            self.btn_enable_adb.grid(row=0, column=0, sticky="ew", padx=5)

            self.btn_force_recon = ctk.CTkButton(
                self.secondary_frame, 
                text="2. Forçar Reconexão", 
                fg_color="#1f1f3f",
                hover_color="#2f2f5f",
                text_color="#FFAA00",
                font=ctk.CTkFont(size=12, weight="bold"),
                height=45,
                command=self.start_force_recognition
            )
            self.btn_force_recon.grid(row=0, column=1, sticky="ew", padx=5)

            self.btn_remove_google = ctk.CTkButton(
                self.secondary_frame, 
                text="3. Remover Google", 
                fg_color="#1f1f3f",
                hover_color="#2f2f5f",
                text_color="#FF6666",
                font=ctk.CTkFont(size=12, weight="bold"),
                height=45,
                command=self.start_remove_google
            )
            self.btn_remove_google.grid(row=0, column=2, sticky="ew", padx=5)

            # ═══════════════════════════════════════════════════════════
            # STATUS / PROGRESSO
            # ═══════════════════════════════════════════════════════════
            self.status_frame = ctk.CTkFrame(self, fg_color="#1a1f3a", corner_radius=10)
            self.status_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=10)
            self.status_frame.grid_columnconfigure(0, weight=1)

            self.status_label = ctk.CTkLabel(
                self.status_frame,
                text="Status: Aguardando ação...",
                font=ctk.CTkFont(size=11),
                text_color="#FFAA00"
            )
            self.status_label.pack(padx=15, pady=10)

            # ═══════════════════════════════════════════════════════════
            # CONSOLE / LOG
            # ═══════════════════════════════════════════════════════════
            self.console_label = ctk.CTkLabel(
                self,
                text="📋 CONSOLE DE SAÍDA",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#00FF00"
            )
            self.console_label.grid(row=4, column=0, sticky="w", padx=20, pady=(15, 5))

            self.console_frame = ctk.CTkFrame(self, fg_color="#000000", corner_radius=5)
            self.console_frame.grid(row=5, column=0, sticky="nsew", padx=20, pady=(0, 20))
            self.console_frame.grid_columnconfigure(0, weight=1)
            self.console_frame.grid_rowconfigure(0, weight=1)
            
            self.log_box = ctk.CTkTextbox(
                self.console_frame, 
                font=ctk.CTkFont(family="Consolas", size=10), 
                text_color="#00FF00",
                fg_color="#000000"
            )
            self.log_box.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
            self.log_box.configure(state="disabled")
            
            # Config de linhas da grid
            self.grid_rowconfigure(5, weight=1)
            
        except Exception as e:
            self.log(f"Erro na inicialização: {str(e)}")
            with open("error_log.txt", "a") as f: 
                f.write(traceback.format_exc())

    def log(self, message):
        """Adiciona mensagem ao console"""
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"{message}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")
        self.update()

    def update_status(self, status_text, color="#FFAA00"):
        """Atualiza label de status"""
        self.status_label.configure(text=status_text, text_color=color)
        self.update()

    def start_full_workflow(self):
        """Executa fluxo completo em thread"""
        self.btn_full_workflow.configure(state="disabled", text="⏳ PROCESSANDO...")
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")
        
        self.update_status("Status: Iniciando fluxo completo...", "#FFAA00")
        
        thread = threading.Thread(target=self._run_full_workflow)
        thread.daemon = True
        thread.start()

    def _run_full_workflow(self):
        """Executa o fluxo completo"""
        success = self.logic.execute_full_workflow(self.log)
        
        self.btn_full_workflow.configure(state="normal", text="▶ EXECUTAR FLUXO COMPLETO")
        
        if success:
            self.update_status("✓ PROCESSO CONCLUÍDO COM SUCESSO!", "#00FF00")
        else:
            self.update_status("✗ Processo interrompido - Verifique os logs", "#FF6666")

    def start_enable_adb(self):
        """Executa apenas a etapa de habilitar ADB"""
        self.btn_enable_adb.configure(state="disabled")
        self.update_status("Status: Habilitando ADB...", "#FFAA00")
        
        thread = threading.Thread(target=lambda: self._run_enable_adb())
        thread.daemon = True
        thread.start()

    def _run_enable_adb(self):
        """Executa habilitar ADB"""
        self.logic.enable_adb_via_at(self.log)
        self.btn_enable_adb.configure(state="normal")

    def start_force_recognition(self):
        """Executa apenas a etapa de forçar reconhecimento"""
        self.btn_force_recon.configure(state="disabled")
        self.update_status("Status: Forçando reconhecimento...", "#FFAA00")
        
        thread = threading.Thread(target=lambda: self._run_force_recon())
        thread.daemon = True
        thread.start()

    def _run_force_recon(self):
        """Executa forçar reconhecimento"""
        self.logic.force_recognition(self.log)
        self.btn_force_recon.configure(state="normal")

    def start_remove_google(self):
        """Executa apenas a etapa de remover Google"""
        self.btn_remove_google.configure(state="disabled")
        self.update_status("Status: Removendo conta Google...", "#FFAA00")
        
        thread = threading.Thread(target=lambda: self._run_remove_google())
        thread.daemon = True
        thread.start()

    def _run_remove_google(self):
        """Executa remover conta Google"""
        self.logic.remove_google_account(self.log)
        self.btn_remove_google.configure(state="normal")

if __name__ == "__main__":
    app = App()
    app.mainloop()
