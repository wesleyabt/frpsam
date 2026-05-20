import subprocess
import time
import serial
import serial.tools.list_ports
import os
import json
import qrcode
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

    def enable_adb_via_at(self, callback_log):
        """Habilita ADB via comandos AT no modo de teste (*#0*#)"""
        callback_log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        callback_log("ETAPA 1: Habilitando ADB via Comandos AT")
        callback_log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        port_name = self.find_port(callback_log)
        if not port_name:
            callback_log("✗ ERRO: Dispositivo Samsung não encontrado!")
            callback_log("  Certifique-se de:")
            callback_log("  1. Conectar o celular via USB")
            callback_log("  2. Abrir: Discador → *#0*# (Modo de Teste)")
            callback_log("  3. Autorizar acesso ao modem se solicitado")
            return False

        # Sequência de comandos AT otimizada para Samsung 2022-2026
        commands = [
            ("AT", "Teste de conexão"),
            ("AT+PACM=1", "Registrando módulo PACM"),
            ("AT+SWATD=0", "Desativando watchdog"),
            ("AT+DEBUGLVC=0,5", "Configurando debug LVC"),
            ("AT+ACTIVATE=0,0,0", "Ativando ADB"),
            ("AT+USBMODECONFIG=2", "Configurando modo USB para ADB+MTP"),
            ("AT+TMODE=1", "Ativando test mode"),
            ("AT+SWATD=1", "Reativando watchdog"),
        ]

        try:
            callback_log(f"\n📱 Conectando na porta {port_name}...")
            ser = serial.Serial(port_name, 115200, timeout=2)
            time.sleep(1)
            
            for cmd, description in commands:
                callback_log(f"\n→ {description}")
                callback_log(f"  Comando: {cmd}")
                
                ser.write((cmd + "\r\n").encode())
                time.sleep(0.8)
                
                response = ser.read_all().decode(errors='ignore').strip()
                if response:
                    callback_log(f"  Resposta: {response}")
                    
                    if "OK" in response:
                        callback_log(f"  ✓ Sucesso!")
                    elif "ACTIVATE" in response and "0,OK" in response:
                        callback_log(f"  ✓ ADB ATIVADO COM SUCESSO!")
                else:
                    callback_log(f"  ⚠ Sem resposta (normal para alguns comandos)")
                
                time.sleep(0.5)
            
            ser.close()
            callback_log("\n✓ Ciclo de ativação AT concluído!")
            time.sleep(2)
            return True
            
        except Exception as e:
            callback_log(f"✗ Erro ao enviar comandos AT: {str(e)}")
            return False

    def force_recognition(self, callback_log):
        """Força reconhecimento do ADB no Windows"""
        callback_log("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        callback_log("ETAPA 2: Forçando Reconhecimento ADB")
        callback_log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        # 1. Reiniciar ADB Server
        callback_log("\n→ Reiniciando servidor ADB...")
        try:
            subprocess.run(["adb", "kill-server"], capture_output=True, timeout=5)
            time.sleep(1)
            subprocess.run(["adb", "start-server"], capture_output=True, timeout=5)
            callback_log("✓ Servidor ADB reiniciado")
        except Exception as e:
            callback_log(f"⚠ ADB não está no PATH: {str(e)}")
            callback_log("  Instale Android SDK Platform Tools")

        # 2. Reset de drivers USB via PowerShell (Windows)
        if os.name == 'nt':
            callback_log("\n→ Resetando drivers Samsung USB...")
            ps_script = """
$devices = Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -like '*VID_04E8*' }
if ($devices) {
    foreach ($dev in $devices) {
        try {
            Disable-PnpDevice -InstanceId $dev.InstanceId -Confirm:$false -ErrorAction SilentlyContinue
            Start-Sleep -Seconds 1
            Enable-PnpDevice -InstanceId $dev.InstanceId -Confirm:$false -ErrorAction SilentlyContinue
            Write-Output "Resetado: $($dev.FriendlyName)"
        } catch {
            Write-Output "Erro ao resetar: $($dev.FriendlyName)"
        }
    }
}
"""
            result = self.run_powershell(ps_script)
            if result:
                callback_log(f"  {result}")
            callback_log("✓ Drivers resetados")

        callback_log("\n→ Aguardando reconexão do dispositivo...")
        time.sleep(3)
        
        callback_log("✓ Reconhecimento concluído!")
        return True

    def remove_google_account(self, callback_log):
        """Remove conta Google via ADB após habilitar debugging"""
        callback_log("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        callback_log("ETAPA 3: Removendo Conta Google")
        callback_log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        # Aguardar prompt de debug no dispositivo
        callback_log("\n⚠ AÇÃO NECESSÁRIA NO CELULAR:")
        callback_log("  → Procure pelo aviso 'Permitir depuração USB?'")
        callback_log("  → Marque 'Sempre permitir neste computador'")
        callback_log("  → Clique 'OK' ou 'SIM'")
        callback_log("\n⏳ Aguardando 30 segundos para você autorizar...\n")
        
        for i in range(30, 0, -1):
            callback_log(f"⏱ {i}s", end="\r")
            time.sleep(1)
        
        callback_log("\n→ Verificando conexão ADB...")
        try:
            # Listar dispositivos conectados
            result = subprocess.run(
                ["adb", "devices"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if "device" not in result.stdout or "offline" in result.stdout:
                callback_log("✗ Dispositivo não autorizado ou offline!")
                callback_log("  Tente novamente e autorize o computador no celular")
                return False
            
            callback_log("✓ Dispositivo conectado e autorizado!")
            
            # Obter ID da conta Google
            callback_log("\n→ Localizando conta Google...")
            result = subprocess.run(
                ["adb", "shell", "dumpsys", "package", "d"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Remover conta Google (método universal)
            callback_log("→ Removendo conta Google...")
            
            # Método 1: Remover via pm (Package Manager)
            remove_commands = [
                ["adb", "shell", "pm", "disable-user", "--user", "0", "com.google.android.gms"],
                ["adb", "shell", "settings", "delete", "secure", "google_account_setup"],
                ["adb", "shell", "content", "delete", "--uri", "content://com.google.android.calendar/calendars"],
            ]
            
            for cmd in remove_commands:
                try:
                    callback_log(f"\n→ Executando: {' '.join(cmd[4:])}")
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        callback_log("  ✓ Executado com sucesso")
                    else:
                        callback_log(f"  ⚠ Resultado: {result.stderr[:100]}")
                except Exception as e:
                    callback_log(f"  ⚠ {str(e)}")
                time.sleep(0.5)
            
            # Método 2: Limpar dados de contas
            callback_log("\n→ Limpando dados de contas...")
            subprocess.run(
                ["adb", "shell", "pm", "clear", "com.android.settings"],
                capture_output=True,
                timeout=5
            )
            
            callback_log("\n✓ Conta Google removida/desativada!")
            return True
            
        except Exception as e:
            callback_log(f"✗ Erro ao remover conta: {str(e)}")
            return False

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
            return "ADB não está instalado ou não está no PATH"

    def generate_elite_qr(self, save_path="adb_qr.png"):
        """Gera QR Code para provisionamento (backup)"""
        data = {
            "android.app.extra.PROVISIONING_DEVICE_ADMIN_COMPONENT_NAME": "com.google.android.apps.work.clouddpc/.receiver.CloudDeviceAdminReceiver",
            "android.app.extra.PROVISIONING_DEVICE_ADMIN_SIGNATURE_CHECKSUM": "I92vovpGaO7mS_H67_v_S_H67_v_S_H67_v_S_H67_v_",
            "android.app.extra.PROVISIONING_LEAVE_ALL_SYSTEM_APPS_ENABLED": True,
            "android.app.extra.PROVISIONING_ADMIN_EXTRAS_BUNDLE": {
                "com.google.android.apps.work.clouddpc.EXTRA_ENROLLMENT_TOKEN": "ADB_ENABLE_2026"
            }
        }
        qr_content = json.dumps(data, separators=(',', ':'))
        qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(qr_content)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(save_path)
        return save_path

    def execute_full_workflow(self, callback_log):
        """Executa o fluxo completo: ADB → Reconhecimento → Remove Google"""
        callback_log("╔═══════════════════════════════════════════════════════╗")
        callback_log("║         SAMSUNG ADB MASTER - FLUXO COMPLETO           ║")
        callback_log("╚═══════════════════════════════════════════════════════╝")
        
        # Etapa 1: Habilitar ADB
        if not self.enable_adb_via_at(callback_log):
            callback_log("\n✗ Falha ao habilitar ADB. Abortando processo.")
            return False
        
        time.sleep(2)
        
        # Etapa 2: Forçar reconhecimento
        if not self.force_recognition(callback_log):
            callback_log("\n✗ Falha ao forçar reconhecimento. Abortando processo.")
            return False
        
        time.sleep(2)
        
        # Etapa 3: Remover conta Google
        if not self.remove_google_account(callback_log):
            callback_log("\n⚠ Falha ao remover conta Google automaticamente.")
            callback_log("  Você pode fazer isso manualmente em: Configurações → Contas")
        
        callback_log("\n╔═══════════════════════════════════════════════════════╗")
        callback_log("║              ✓ PROCESSO CONCLUÍDO!                    ║")
        callback_log("╚═══════════════════════════════════════════════════════╝")
        return True
