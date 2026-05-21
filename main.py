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

            self.title("Samsung FRP Master - IMEI Bypass v3.0")
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
            self.header = ctk.CTkFrame(self, corner_radius=0, fg_color="#0a0e27")
            self.header.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
            self.header.grid_columnconfigure(0, weight=1)
            
            self.title_label = ctk.CTkLabel(
                self.header, 
                text="🔓 SAMSUNG FRP MASTER - IMEI BYPASS v3.0", 
                font=ctk.CTkFont(size=26, weight="bold"),
                text_color="#FF4444"
            )
            self.title_label.pack(side="left", padx=30, pady=15)
            
            self.subtitle_label = ctk.CTkLabel(
                self.header, 
                text="Método Prioritário para Samsung 2022-2026 | Bypass via IMEI", 
                font=ctk.CTkFont(size=11),
                text_color="#888888"
            )
            self.subtitle_label.pack(side="left", padx=30)

            # ═══════════════════════════════════════════════════════════
            # INSTRUCOES
            # ═══════════════════════════════════════════════════════════
            self.instructions_frame = ctk.CTkFrame(self, fg_color="#1a2a3a", corner_radius=10)
            self.instructions_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=15)
            self.instructions_frame.grid_columnconfigure(0, weight=1)
            
            instruction_text = """⚡ MÉTODO IMEI (RECOMENDADO - Taxa de Sucesso ~85%)
1️⃣  Obtenha o IMEI do celular:
    • Opção A: Procure na caixa/nota fiscal
    • Opção B: Disque *#06# (se conseguir)
    • Opção C: Verifique em "Sobre o telefone"
    • Opção D: Cole abaixo e clique "GERAR BYPASS IMEI"

2️⃣  Digite o IMEI no campo abaixo (15-17 dígitos)
3️⃣  Clique "▶ GERAR BYPASS IMEI" para gerar QR codes
4️⃣  Na tela de Bem-vindo do celular: Toque 6 vezes em qualquer lugar
5️⃣  Escaneie um dos QR codes gerados (tente AMAPI → KNOX → GOOGLE)"""

            self.instructions_label = ctk.CTkLabel(
                self.instructions_frame,
                text=instruction_text,
                font=ctk.CTkFont(size=10),
                text_color="#CCCCCC",
                justify="left"
            )
            self.instructions_label.pack(padx=20, pady=15)

            # ═══════════════════════════════════════════════════════════
            # ENTRADA IMEI
            # ═══════════════════════════════════════════════════════════
            self.imei_frame = ctk.CTkFrame(self, fg_color="#1a1f3a", corner_radius=10)
            self.imei_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
            self.imei_frame.grid_columnconfigure(1, weight=1)

            imei_label = ctk.CTkLabel(
                self.imei_frame,
                text="📱 IMEI (15-17 dígitos):",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#00FF00"
            )
            imei_label.grid(row=0, column=0, padx=15, pady=10, sticky="w")

            self.imei_entry = ctk.CTkEntry(
                self.imei_frame,
                placeholder_text="Exemplo: 354676110001234",
                font=ctk.CTkFont(size=12),
                height=40,
                text_color="#FFFFFF",
                fg_color="#2a2a3a"
            )
            self.imei_entry.grid(row=0, column=1, padx=15, pady=10, sticky="ew")

            # ═══════════════════════════════════════════════════════════
            # BOTOES PRINCIPAIS
            # ═══════════════════════════════════════════════════════════
            self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
            self.button_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=15)
            self.button_frame.grid_columnconfigure(0, weight=1)

            # Botão GRANDE - Fluxo IMEI (Prioritário)
            self.btn_imei_bypass = ctk.CTkButton(
                self.button_frame, 
                text="▶ GERAR BYPASS IMEI (RECOMENDADO)", 
                fg_color="#FF4444",
                hover_color="#FF6666",
                text_color="#FFFFFF",
                font=ctk.CTkFont(size=15, weight="bold"),
                height=60,
                command=self.start_imei_bypass
            )
            self.btn_imei_bypass.grid(row=0, column=0, sticky="ew", pady=10)

            # Botões secundários em linha
            self.secondary_frame = ctk.CTkFrame(self.button_frame, fg_color="transparent")
            self.secondary_frame.grid(row=1, column=0, sticky="ew", pady=10)
            self.secondary_frame.grid_columnconfigure((0, 1), weight=1, uniform="equal")

            self.btn_legacy_at = ctk.CTkButton(
                self.secondary_frame, 
                text="⚙️ Método Legado (AT)", 
                fg_color="#1a1a3f",
                hover_color="#2a2a5f",
                text_color="#FFAA00",
                font=ctk.CTkFont(size=11, weight="bold"),
                height=40,
                command=self.start_legacy_at
            )
            self.btn_legacy_at.grid(row=0, column=0, sticky="ew", padx=5)

            self.btn_force_recon = ctk.CTkButton(
                self.secondary_frame, 
                text="🔄 Forçar Reconexão", 
                fg_color="#1a1a3f",
                hover_color="#2a2a5f",
                text_color="#FFAA00",
                font=ctk.CTkFont(size=11, weight="bold"),
                height=40,
                command=self.start_force_recognition
            )
            self.btn_force_recon.grid(row=0, column=1, sticky="ew", padx=5)

            # ═══════════════════════════════════════════════════════════
            # STATUS / PROGRESSO
            # ═══════════════════════════════════════════════════════════
            self.status_frame = ctk.CTkFrame(self, fg_color="#1a1f3a", corner_radius=10)
            self.status_frame.grid(row=4, column=0, sticky="ew", padx=20, pady=10)
            self.status_frame.grid_columnconfigure(0, weight=1)

            self.status_label = ctk.CTkLabel(
                self.status_frame,
                text="Status: Aguardando IMEI...",
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
            self.console_label.grid(row=5, column=0, sticky="w", padx=20, pady=(15, 5))

            self.console_frame = ctk.CTkFrame(self, fg_color="#000000", corner_radius=5)
            self.console_frame.grid(row=6, column=0, sticky="nsew", padx=20, pady=(0, 20))
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
            self.grid_rowconfigure(6, weight=1)
            
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

    def start_imei_bypass(self):
        """Inicia o bypass via IMEI (método prioritário)"""
        imei = self.imei_entry.get().strip()
        
        if not imei:
            self.update_status("✗ Digite o IMEI primeiro!", "#FF6666")
            self.log("✗ ERRO: Campo IMEI está vazio!")
            return
        
        # Limpar espaços e caracteres especiais
        imei = ''.join(filter(str.isdigit, imei))
        
        if len(imei) < 15:
            self.update_status(f"✗ IMEI inválido! ({len(imei)} dígitos)", "#FF6666")
            self.log(f"✗ ERRO: IMEI precisa ter 15+ dígitos, você digitou {len(imei)}")
            return
        
        self.btn_imei_bypass.configure(state="disabled", text="⏳ PROCESSANDO...")
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")
        
        self.update_status("Status: Gerando bypass IMEI...", "#FFAA00")
        
        thread = threading.Thread(target=lambda: self._run_imei_bypass(imei))
        thread.daemon = True
        thread.start()

    def _run_imei_bypass(self, imei):
        """Executa o bypass IMEI em thread"""
        success = self.logic.imei_bypass_workflow(imei, self.log)
        
        self.btn_imei_bypass.configure(state="normal", text="▶ GERAR BYPASS IMEI (RECOMENDADO)")
        
        if success:
            self.update_status("✓ BYPASS IMEI GERADO COM SUCESSO!", "#00FF00")
            self.log("\n✓ Verifique os arquivos QR code gerados!")
        else:
            self.update_status("✗ Falha ao gerar bypass", "#FF6666")

    def start_legacy_at(self):
        """Executa método legado AT (compatibilidade)"""
        self.btn_legacy_at.configure(state="disabled")
        self.update_status("Status: Tentando método legado AT...", "#FFAA00")
        
        thread = threading.Thread(target=lambda: self._run_legacy_at())
        thread.daemon = True
        thread.start()

    def _run_legacy_at(self):
        """Executa método legado"""
        self.logic.enable_adb_via_at(self.log)
        self.btn_legacy_at.configure(state="normal")
        self.update_status("⚠️ Método AT concluído (baixa taxa de sucesso)", "#FFAA00")

    def start_force_recognition(self):
        """Força reconhecimento USB"""
        self.btn_force_recon.configure(state="disabled")
        self.update_status("Status: Forçando reconexão...", "#FFAA00")
        
        thread = threading.Thread(target=lambda: self._run_force_recon())
        thread.daemon = True
        thread.start()

    def _run_force_recon(self):
        """Executa forçar reconexão"""
        self.logic.force_recognition(self.log)
        self.btn_force_recon.configure(state="normal")
        self.update_status("✓ Reconexão concluída", "#00FF00")

if __name__ == "__main__":
    app = App()
    app.mainloop()
