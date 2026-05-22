import customtkinter as ctk
from tkinter import messagebox, scrolledtext
import threading
import subprocess
import sys
from samsung_logic import SamsungLogic

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("FRP Samsung - v3.0 IMEI Focused")
        self.geometry("900x700")
        self.resizable(True, True)
        
        self.logic = SamsungLogic()
        self.detected_imei = None
        self.monitoring = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="FRP Samsung Bypass Tool v3.0",
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=10)
        
        # Status frame
        status_frame = ctk.CTkFrame(main_frame)
        status_frame.pack(fill="x", pady=10)
        
        status_label = ctk.CTkLabel(status_frame, text="Status:", font=("Arial", 12, "bold"))
        status_label.pack(side="left", padx=5)
        
        self.status_var = ctk.StringVar(value="Ready")
        self.status_display = ctk.CTkLabel(
            status_frame,
            textvariable=self.status_var,
            font=("Arial", 12),
            text_color="green"
        )
        self.status_display.pack(side="left", padx=5)
        
        # IMEI Detection Section
        imei_frame = ctk.CTkFrame(main_frame, border_width=2, border_color="blue")
        imei_frame.pack(fill="x", pady=10)
        
        imei_label = ctk.CTkLabel(
            imei_frame,
            text="STEP 1: Detect Device IMEI",
            font=("Arial", 14, "bold"),
            text_color="blue"
        )
        imei_label.pack(pady=5)
        
        detect_imei_btn = ctk.CTkButton(
            imei_frame,
            text="Auto-Detect IMEI via ADB",
            command=self.start_imei_detection,
            fg_color="blue",
            hover_color="darkblue",
            height=50,
            font=("Arial", 12, "bold")
        )
        detect_imei_btn.pack(pady=5, padx=10, fill="x")
        
        self.imei_status = ctk.CTkLabel(
            imei_frame,
            text="IMEI: Not detected",
            font=("Arial", 11),
            text_color="gray"
        )
        self.imei_status.pack(pady=5)
        
        # IMEI Bypass Section (MAIN)
        bypass_frame = ctk.CTkFrame(main_frame, border_width=3, border_color="green")
        bypass_frame.pack(fill="x", pady=10)
        
        bypass_label = ctk.CTkLabel(
            bypass_frame,
            text="STEP 2: Generate & Apply FRP Bypass Code",
            font=("Arial", 14, "bold"),
            text_color="green"
        )
        bypass_label.pack(pady=5)
        
        self.bypass_btn = ctk.CTkButton(
            bypass_frame,
            text="Generate FRP Bypass Code (IMEI Method)",
            command=self.start_imei_bypass,
            fg_color="green",
            hover_color="darkgreen",
            height=60,
            font=("Arial", 13, "bold"),
            state="disabled"
        )
        self.bypass_btn.pack(pady=10, padx=10, fill="x")
        
        self.bypass_status = ctk.CTkLabel(
            bypass_frame,
            text="Waiting for IMEI detection...",
            font=("Arial", 11),
            text_color="orange"
        )
        self.bypass_status.pack(pady=5)
        
        # Generated Code Display
        code_display_label = ctk.CTkLabel(
            bypass_frame,
            text="Generated Code:",
            font=("Arial", 10, "bold")
        )
        code_display_label.pack(pady=(10, 0))
        
        self.code_display = ctk.CTkTextbox(bypass_frame, height=80, width=400)
        self.code_display.pack(pady=5, padx=10, fill="both")
        
        # Legacy AT Method (Fallback)
        at_frame = ctk.CTkFrame(main_frame, border_width=2, border_color="orange")
        at_frame.pack(fill="x", pady=10)
        
        at_label = ctk.CTkLabel(
            at_frame,
            text="FALLBACK: Legacy AT Command Method",
            font=("Arial", 12, "bold"),
            text_color="orange"
        )
        at_label.pack(pady=5)
        
        at_btn = ctk.CTkButton(
            at_frame,
            text="Run AT Command Bypass (Legacy)",
            command=self.start_force_recognition,
            fg_color="orange",
            hover_color="darkorange",
            height=40,
            font=("Arial", 11)
        )
        at_btn.pack(pady=5, padx=10, fill="x")
        
        # Utilities Section
        util_frame = ctk.CTkFrame(main_frame)
        util_frame.pack(fill="x", pady=10)
        
        util_label = ctk.CTkLabel(
            util_frame,
            text="Utilities",
            font=("Arial", 12, "bold")
        )
        util_label.pack(pady=5)
        
        util_btn_frame = ctk.CTkFrame(util_frame)
        util_btn_frame.pack(fill="x", padx=10, pady=5)
        
        clean_btn = ctk.CTkButton(
            util_btn_frame,
            text="Clean Activate",
            command=self.start_clean_activate,
            width=150
        )
        clean_btn.pack(side="left", padx=5)
        
        mtp_btn = ctk.CTkButton(
            util_btn_frame,
            text="MTP Browser",
            command=self.start_mtp_browser,
            width=150
        )
        mtp_btn.pack(side="left", padx=5)
        
        monitor_btn = ctk.CTkButton(
            util_btn_frame,
            text="Toggle Device Monitor",
            command=self.toggle_monitoring,
            width=150
        )
        monitor_btn.pack(side="left", padx=5)
        
        # Console Output
        console_label = ctk.CTkLabel(
            main_frame,
            text="Console Output",
            font=("Arial", 11, "bold")
        )
        console_label.pack(pady=(10, 0))
        
        self.console = scrolledtext.ScrolledText(
            main_frame,
            height=10,
            width=100,
            bg="#1e1e1e",
            fg="#00ff00",
            font=("Courier New", 9)
        )
        self.console.pack(fill="both", expand=True, pady=5)
        
    def log(self, message):
        """Log message to console"""
        self.console.insert("end", message + "\n")
        self.console.see("end")
        self.console.update()
        
    def update_status(self, message, color="green"):
        """Update status display"""
        self.status_var.set(message)
        self.status_display.configure(text_color=color)
        
    def start_imei_detection(self):
        """Start IMEI detection in separate thread"""
        thread = threading.Thread(target=self._run_detect_imei, daemon=True)
        thread.start()
        
    def _run_detect_imei(self):
        """Detect IMEI via ADB"""
        try:
            self.update_status("Detecting IMEI...", "orange")
            self.log("[*] Starting IMEI detection via ADB...")
            
            result = self.logic.detect_imei()
            
            if result:
                self.detected_imei = result
                self.imei_status.configure(text=f"IMEI: {result}", text_color="green")
                self.bypass_btn.configure(state="normal")
                self.bypass_status.configure(text="Ready to generate bypass code", text_color="green")
                self.update_status("IMEI Detected Successfully", "green")
                self.log(f"[+] IMEI Detected: {result}")
            else:
                self.imei_status.configure(text="IMEI: Detection failed", text_color="red")
                self.bypass_status.configure(text="IMEI detection failed. Please try again.", text_color="red")
                self.update_status("IMEI Detection Failed", "red")
                self.log("[!] Failed to detect IMEI")
                
        except Exception as e:
            self.update_status(f"Error: {str(e)}", "red")
            self.log(f"[!] Error during IMEI detection: {str(e)}")
            
    def start_imei_bypass(self):
        """Start IMEI bypass code generation"""
        if not self.detected_imei:
            messagebox.showerror("Error", "Please detect IMEI first")
            return
            
        thread = threading.Thread(target=self._run_imei_bypass, daemon=True)
        thread.start()
        
    def _run_imei_bypass(self):
        """Generate FRP bypass code using IMEI"""
        try:
            self.update_status("Generating bypass code...", "orange")
            self.bypass_btn.configure(state="disabled")
            self.log(f"[*] Generating FRP bypass code for IMEI: {self.detected_imei}")
            
            code = self.logic.generate_frp_bypass_code(self.detected_imei)
            
            if code:
                self.code_display.delete("1.0", "end")
                self.code_display.insert("1.0", code)
                self.bypass_status.configure(text="Code generated successfully!", text_color="green")
                self.update_status("Bypass Code Generated", "green")
                self.log(f"[+] Bypass code generated:\n{code}")
                
                # Ask if user wants to apply
                apply = messagebox.askyesno(
                    "Apply Code",
                    "Bypass code generated. Do you want to apply it now?"
                )
                if apply:
                    self._apply_bypass_code(code)
            else:
                self.bypass_status.configure(text="Code generation failed", text_color="red")
                self.update_status("Bypass Code Generation Failed", "red")
                self.log("[!] Failed to generate bypass code")
                
        except Exception as e:
            self.update_status(f"Error: {str(e)}", "red")
            self.log(f"[!] Error during bypass generation: {str(e)}")
        finally:
            self.bypass_btn.configure(state="normal")
            
    def _apply_bypass_code(self, code):
        """Apply the generated bypass code"""
        try:
            self.log("[*] Applying bypass code to device...")
            result = self.logic.apply_frp_bypass(code, self.detected_imei)
            
            if result:
                self.update_status("Bypass Applied Successfully", "green")
                self.log("[+] Bypass code applied successfully!")
                messagebox.showinfo("Success", "FRP bypass applied successfully!")
            else:
                self.update_status("Failed to Apply Bypass", "red")
                self.log("[!] Failed to apply bypass code")
                messagebox.showerror("Error", "Failed to apply bypass code")
                
        except Exception as e:
            self.update_status(f"Error: {str(e)}", "red")
            self.log(f"[!] Error applying bypass: {str(e)}")
            
    def start_clean_activate(self):
        """Start clean activation process"""
        thread = threading.Thread(target=self._run_clean_activate, daemon=True)
        thread.start()
        
    def _run_clean_activate(self):
        """Run clean activation"""
        try:
            self.update_status("Running clean activation...", "orange")
            self.log("[*] Starting clean activation process...")
            
            result = self.logic.clean_activate()
            
            if result:
                self.update_status("Clean Activation Complete", "green")
                self.log("[+] Clean activation completed successfully")
            else:
                self.update_status("Clean Activation Failed", "red")
                self.log("[!] Clean activation failed")
                
        except Exception as e:
            self.update_status(f"Error: {str(e)}", "red")
            self.log(f"[!] Error during clean activation: {str(e)}")
            
    def start_force_recognition(self):
        """Start force recognition (AT method)"""
        thread = threading.Thread(target=self._run_force_recognition, daemon=True)
        thread.start()
        
    def _run_force_recognition(self):
        """Run force recognition"""
        try:
            self.update_status("Running force recognition...", "orange")
            self.log("[*] Starting force recognition (AT method)...")
            
            result = self.logic.force_recognition()
            
            if result:
                self.update_status("Force Recognition Complete", "green")
                self.log("[+] Force recognition completed")
            else:
                self.update_status("Force Recognition Failed", "red")
                self.log("[!] Force recognition failed")
                
        except Exception as e:
            self.update_status(f"Error: {str(e)}", "red")
            self.log(f"[!] Error during force recognition: {str(e)}")
            
    def start_mtp_browser(self):
        """Start MTP browser"""
        try:
            self.log("[*] Launching MTP browser...")
            self.logic.open_mtp_browser()
        except Exception as e:
            self.log(f"[!] Error opening MTP browser: {str(e)}")
            
    def toggle_monitoring(self):
        """Toggle device monitoring"""
        self.monitoring = not self.monitoring
        
        if self.monitoring:
            self.update_status("Device monitoring ON", "green")
            self.log("[*] Device monitoring started")
            thread = threading.Thread(target=self.monitor_adb, daemon=True)
            thread.start()
        else:
            self.update_status("Device monitoring OFF", "gray")
            self.log("[*] Device monitoring stopped")
            
    def monitor_adb(self):
        """Monitor ADB connection"""
        while self.monitoring:
            try:
                result = subprocess.run(
                    ["adb", "devices"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if "device" in result.stdout.lower():
                    self.log("[+] Device connected")
                else:
                    self.log("[-] No device detected")
                    
                threading.Event().wait(2)
                
            except Exception as e:
                self.log(f"[!] Monitor error: {str(e)}")
                break

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
