# Samsung ADB Master Tool v16.0

Ferramenta completa para habilitar ADB e remover conta Google em dispositivos Samsung (2022-2026).

## ✨ Funcionalidades

- ✅ **Habilitar ADB** via comandos AT no modo de teste (*#0*#)
- ✅ **Forçar Reconhecimento** do dispositivo no Windows
- ✅ **Remover Conta Google** automaticamente via ADB
- ✅ **Fluxo Automático Completo** - todas as 3 etapas em sequência
- ✅ **Etapas Individuais** - execute cada passo separadamente

## 🚀 Como Usar

### Requisitos
- Windows 10/11
- Drivers Samsung USB instalados
- Android SDK Platform Tools (ADB) - [Baixe aqui](https://developer.android.com/studio/releases/platform-tools)
- Cabo USB de boa qualidade

### Passos

1. **Conecte o celular ao PC via USB**

2. **No celular**, abra o Discador de Emergência e digite: `*#0*#`
   - Uma tela branca com botões aparecerá (Modo de Teste)

3. **Execute o aplicativo** `SamsungADBMaster.exe`

4. **Clique em "EXECUTAR FLUXO COMPLETO"** ou execute as etapas individualmente:
   - **1️⃣ Habilitar ADB** - Envia comandos AT para ativar ADB
   - **2️⃣ Forçar Reconhecimento** - Reinicia ADB server e reseta drivers USB
   - **3️⃣ Remover Google** - Remove a conta Google automaticamente

5. **Quando solicitado no celular**, autorize a depuração USB
   - Procure por: "Permitir depuração USB?"
   - Marque: "Sempre permitir neste computador"
   - Clique: "OK"

## ⚙️ Desenvolvimento

### Instalar Dependências
```bash
pip install -r requirements.txt
```

### Executar Aplicativo
```bash
python main.py
```

### Compilar para .EXE
```bash
build.bat
```

## 📁 Arquivos

- `main.py` - Interface gráfica (CustomTkinter)
- `samsung_logic.py` - Lógica principal (comandos AT, ADB, etc)
- `samsung_helper.ps1` - Scripts PowerShell para drivers
- `requirements.txt` - Dependências Python
- `build.bat` - Script de compilação

## ⚠️ Aviso Legal

Esta ferramenta é destinada para:
- Recuperação de dispositivos próprios
- Manutenção e suporte técnico
- Fins educacionais

O uso para contornar proteções em dispositivos de terceiros pode ser ilegal.

## 🔧 Troubleshooting

### "Dispositivo Samsung não encontrado"
- Certifique-se de que o celular está em modo de teste (*#0*#)
- Instale os drivers Samsung USB oficiais
- Tente outras portas USB

### "ADB não está no PATH"
- Baixe e instale Android SDK Platform Tools
- Adicione o caminho ao PATH do Windows

### "Dispositivo offline"
- Autorize a depuração USB no celular
- Desconecte e reconecte o cabo USB
- Reinicie o ADB server

## 📞 Suporte

Para mais informações sobre os comandos AT e Samsung:
- [Samsung Developers](https://developer.samsung.com)
- [Android Debug Bridge (ADB)](https://developer.android.com/studio/command-line/adb)

---

**Versão:** 16.0  
**Última atualização:** 2026-05-20  
**Compatibilidade:** Samsung 2022-2026 (Android 12-16)
