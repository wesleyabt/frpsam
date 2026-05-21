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

            self.title("Samsung FRP Bypass Master - v3.0")
            self.geometry("1100x1000")
            
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("blue") 

            self.logic = SamsungADBLogic()

            # Layout
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(2, weight=1)

            # ═══════════════════════════════════════════════════════════
            # HEADER
            # ═══════════════════════════════════════════════════════════
            self.header = ctk.CTkFrame(self, corner_radius=0, fg_color="#0a1428")
            self.header.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
            self.header.grid_columnconfigure(0, weight=1)
            
            self.title_label = ctk.CTkLabel(
                self.header, 
                text="🔓 SAMSUNG FRP BYPASS MASTER v3.0", 
                font=ctk.CTkFont(size=26, weight="bold"),
                text_color="#FF6600"
            )
            self.title_label.pack(side="left", padx=30, pady=15)
            
            self.subtitle_label = ctk.CTkLabel(
                self.header, 
                text="Desbloqueio via IMEI | Método Principal 2022-2026", 
                font=ctk.CTkFont(size=11),
                text_color="#FFAA00"
            )
            self.subtitle_label.pack(side="left", padx=30)

            # ═══════════════════════════════════════════════════════════
            # SECAO DE ENTRADA - IMEI
            # ═══════════════════════════════════════════════════════════
            self.imei_frame = ctk.CTkFrame(self, fg_color="#1a2332", corner_radius=10)
            self.imei_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=15)
            self.imei_frame.grid_columnconfigure(1, weight=1)

            self.imei_label = ctk.CTkLabel(
                self.imei_frame,
                text="📱 IMEI do Dispositivo:",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#FF6600"
            )
            self.imei_label.grid(row=0, column=0, sticky="w", padx=15, pady=(15, 5))

            self.imei_entry = ctk.CTkEntry(
                self.imei_frame,
                placeholder_text="Digite o IMEI (15+ dígitos) ou clique 'Detectar Automaticamente'",
                font=ctk.CTkFont(size=12),
                height=40
            )
            self.imei_entry.grid(row=1, column=0, columnspan=3, sticky="ew", padx=15, pady=5)

            self.btn_detect_imei = ctk.CTkButton(
                self.imei_frame,
                text="🔍 Detectar IMEI",
                fg_color="#1f3a5f",
                hover_color="#2f4a7f",
                text_color="#00AAFF",
                font=ctk.CTkFont(size=11, weight="bold"),
                height=40,
                command=self.detect_imei
            )
            self.btn_detect_imei.grid(row=0, column=3, rowspan=2, sticky="ew", padx=(5, 15), pady=5)

            self.imei_help = ctk.CTkLabel(
                self.imei_frame,
                text="💡 Dica: Digite #06# no celular para descobrir o IMEI, ou conecte e detecte automaticamente",
                font=ctk.CTkFont(size=10),
                text_color="#888888"
            )
            self.imei_help.grid(row=2, column=0, columnspan=4, sticky="w", padx=15, pady=(0, 15))

            # ═══════════════════════════════════════════════════════════
            # BOTOES PRINCIPAIS
            # ═══════════════════════════════════════════════════════════
            self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
            self.button_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=15)
            self.button_frame.grid_columnconfigure(0, weight=1)

            # Botão GRANDE - Bypass via IMEI (MÉTODO PRINCIPAL)
            self.btn_imei_bypass = ctk.CTkButton(
                self.button_frame, 
                text="▶ GERAR BYPASS FRP VIA IMEI (MÉTODO PRINCIPAL)", 
                fg_color="#FF6600",
                hover_color="#FF8800",
                text_color="#000000",
                font=ctk.CTkFont(size=15, weight="bold"),
                height=70,
                command=self.start_imei_bypass
            )
            self.btn_imei_bypass.grid(row=0, column=0, sticky="ew", pady=10)

            # Botões secundários - Métodos alternativos
            self.secondary_frame = ctk.CTkFrame(self.button_frame, fg_color="transparent")
            self.secondary_frame.grid(row=1, column=0, sticky="ew", pady=10)
            self.secondary_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="equal")

            self.btn_at_legacy = ctk.CTkButton(
                self.secondary_frame, 
                text="⚠️ Método Legado AT", 
                fg_color="#5f3f1f",
                hover_color="#7f5f3f",
                text_color="#FFAA00",
                font=ctk.CTkFont(size=11, weight="bold"),
                height=45,
                command=self.start_at_legacy
            )
            self.btn_at_legacy.grid(row=0, column=0, sticky="ew", padx=5)

            self.btn_force_recon = ctk.CTkButton(
                self.secondary_frame, 
                text="🔄 Forçar Reconexão", 
                fg_color="#1f3a5f",
                hover_color="#2f4a7f",
                text_color="#00AAFF",
                font=ctk.CTkFont(size=11, weight="bold"),
                height=45,
                command=self.start_force_recon
            )
            self.btn_force_recon.grid(row=0, column=1, sticky="ew", padx=5)

            self.btn_clear_log = ctk.CTkButton(
                self.secondary_frame, 
                text="🗑️ Limpar Log", 
                fg_color="#3f3f3f",
                hover_color="#5f5f5f",
                text_color="#CCCCCC",
                font=ctk.CTkFont(size=11, weight="bold"),
                height=45,
                command=self.clear_log
            )
            self.btn_clear_log.grid(row=0, column=2, sticky="ew", padx=5)

            # ═══════════════════════════════════════════════════════════
            # STATUS / PROGRESSO
            # ═══════════════════════════════════════════════════════════
            self.status_frame = ctk.CTkFrame(self, fg_color="#1a2332", corner_radius=10)
            self.status_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=10)
            self.status_frame.grid_columnconfigure(0, weight=1)

            self.status_label = ctk.CTkLabel(
                self.status_frame,
                text="Status: Aguardando entrada de IMEI...",
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
                text_color="#FF6600"
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
            with open("error_log.txt", "a") as f: 
                f.write(traceback.format_exc())

    def log(self, message):
        """Adiciona mensagem ao console"""
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"{message}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")
        self.update()

    def clear_log(self):
        """Limpa o console"""
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")

    def update_status(self, status_text, color="#FFAA00"):
        """Atualiza label de status"""
        self.status_label.configure(text=status_text, text_color=color)
        self.update()

    def detect_imei(self):
        """Detecta IMEI automaticamente via ADB"""
        self.btn_detect_imei.configure(state="disabled", text="⏳ Detectando...")
        self.update_status("Status: Detectando IMEI...", "#FFAA00")
        
        thread = threading.Thread(target=self._run_detect_imei)
        thread.daemon = True
        thread.start()

    def _run_detect_imei(self):
        """Thread para detectar IMEI"""
        self.log("Tentando conectar ao dispositivo via ADB...")
        imei = self.logic.get_device_imei(self.log)
        
        if imei:
            self.imei_entry.delete(0, "end")
            self.imei_entry.insert(0, imei)
            self.log(f"✓ IMEI detectado: {imei}")
            self.update_status("✓ IMEI detectado com sucesso!", "#00FF00")
        else:
            self.log("✗ Falha ao detectar IMEI. Digite manualmente.")
            self.log("  Dica: No celular, disque #06# para ver o IMEI")
            self.update_status("✗ Falha ao detectar - Digite o IMEI manualmente", "#FF6666")
        
        self.btn_detect_imei.configure(state="normal", text="🔍 Detectar IMEI")

    def start_imei_bypass(self):
        """Executa bypass via IMEI"""
        imei = self.imei_entry.get().strip()
        
        if not imei:
            self.log("✗ ERRO: Digite o IMEI ou clique em 'Detectar IMEI'")
            self.update_status("✗ IMEI não fornecido", "#FF6666")
            return
        
        if len(imei) < 15:
            self.log(f"✗ ERRO: IMEI inválido! Deve ter 15+ dígitos (informado: {len(imei)})")
            self.update_status("✗ IMEI inválido", "#FF6666")
            return
        
        self.btn_imei_bypass.configure(state="disabled", text="⏳ PROCESSANDO...")
        self.update_status("Status: Gerando bypass FRP via IMEI...", "#FFAA00")
        
        thread = threading.Thread(target=lambda: self._run_imei_bypass(imei))
        thread.daemon = True
        thread.start()

    def _run_imei_bypass(self, imei):
        """Executa o bypass via IMEI"""
        success = self.logic.imei_bypass_workflow(imei, self.log)
        
        self.btn_imei_bypass.configure(state="normal", text="▶ GERAR BYPASS FRP VIA IMEI (MÉTODO PRINCIPAL)")
        
        if success:
            self.update_status("✓ BYPASS FRP GERADO COM SUCESSO!", "#00FF00")
        else:
            self.update_status("✗ Falha ao gerar bypass - Verifique os logs", "#FF6666")

    def start_at_legacy(self):
        """Executa método legado AT"""
        self.btn_at_legacy.configure(state="disabled", text="⏳ Processando...")
        self.update_status("Status: Tentando método legado AT...", "#FFAA00")
        
        thread = threading.Thread(target=self._run_at_legacy)
        thread.daemon = True
        thread.start()

    def _run_at_legacy(self):
        """Executa AT legacy"""
        self.logic.enable_adb_via_at(self.log)
        self.btn_at_legacy.configure(state="normal", text="⚠️ Método Legado AT")

    def start_force_recon(self):
        """Executa forçar reconexão"""
        self.btn_force_recon.configure(state="disabled", text="⏳ Processando...")
        self.update_status("Status: Forçando reconexão...", "#FFAA00")
        
        thread = threading.Thread(target=self._run_force_recon)
        thread.daemon = True
        thread.start()

    def _run_force_recon(self):
        """Executa forçar reconexão"""
        self.logic.force_recognition(self.log)
        self.btn_force_recon.configure(state="normal", text="🔄 Forçar Reconexão")
        self.update_status("✓ Reconexão forçada", "#00FF00")

if __name__ == "__main__":
    app = App()
    app.mainloop()
