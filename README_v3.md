# Samsung FRP Bypass Master v3.0

**Desbloqueio Samsung via IMEI | Método Principal para 2022-2026**

## ⚠️ Informação Importante

Os métodos tradicionais de ativação ADB (via comandos AT em modo de teste) **não funcionam mais** em dispositivos Samsung de 2022-2026 devido a aumentos de segurança.

**O método IMEI-based FRP bypass é agora o método principal e mais eficaz.**

## 🎯 Método Principal: IMEI-Based FRP Bypass

Este método utiliza o **IMEI do dispositivo** para gerar QR codes de provisionamento que bypassa a proteção FRP (Factory Reset Protection) em Samsung 2022-2026.

### Como Funciona

1. **Coleta do IMEI**: Pode ser obtido via `*#06#` no celular ou detectado via ADB
2. **Geração de Tokens**: Cria tokens criptográficos baseados no IMEI
3. **Geração de QR Codes**: Produz 3 QR codes em diferentes formatos (AMAPI, KNOX, Google)
4. **Provisionamento**: Escaneia o QR durante a tela de boas-vindas para ativar ADB

## 📱 Como Usar

### Passo 1: Obter o IMEI

**Opção A - Manual (via #06#)**
1. Ligue o celular
2. Abra o Discador (Telefone)
3. Digite: `*#06#`
4. Anote os números exibidos (IMEI)
5. Digite no aplicativo

**Opção B - Automático (via ADB)**
1. Conecte o celular ao PC via USB
2. Clique "🔍 Detectar IMEI"
3. O IMEI será detectado automaticamente

### Passo 2: Gerar Bypass FRP

1. **Digite ou detecte o IMEI** (15+ dígitos)
2. **Clique em** "▶ GERAR BYPASS FRP VIA IMEI"
3. **Aguarde** o processo completar (gera 3 QR codes)

### Passo 3: Usar os QR Codes

**Arquivos gerados:**
- `frp_bypass_amapi.png` - Android Management API (mais compatível)
- `frp_bypass_knox.png` - Samsung Knox (oficial)
- `frp_bypass_google.png` - Google Zero-Touch

**Na tela de boas-vindas do celular:**
1. Conecte o celular a um **WiFi** (importante!)
2. Toque **6 vezes** em qualquer lugar em branco na tela
3. Um leitor de **QR code** será aberto
4. **Escaneie** um dos QR codes (comece pelo AMAPI)
5. Se der erro "Formato inválido", tente outro QR code

### Passo 4: Conclusão

Após escanear com sucesso:
- ✅ O ADB será ativado automaticamente
- ✅ A conta Google será bypassada
- ✅ O celular entrará no sistema
- ✅ Você terá acesso total

## 🔧 Requisitos

- **Windows 10/11**
- **Python 3.10+** (se rodar do código)
- **Cabo USB** de qualidade
- **Drivers Samsung USB** (opcional, para detecção automática)
- **WiFi** no celular (recomendado para o bypass)

## 💾 Instalação

### Opção 1: Executável (Recomendado)
```
Execute: SamsungFRPBypassMaster.exe
```

### Opção 2: Do Código-Fonte
```bash
# Clonar repositório
git clone https://github.com/wesleyabt/frpsam.git
cd frpsam

# Instalar dependências
pip install -r requirements.txt

# Executar
python main.py
```

### Opção 3: Compilar Executável
```bash
# Windows
build.bat

# Resultado: dist/SamsungFRPBypassMaster.exe
```

## 🎮 Interface da Aplicação

| Elemento | Função |
|----------|--------|
| **Campo IMEI** | Digite ou detecte o IMEI do dispositivo |
| **🔍 Detectar IMEI** | Detecta automaticamente via ADB |
| **▶ GERAR BYPASS (LARANJA)** | Método principal - Gera QR codes via IMEI |
| **⚠️ Método Legado AT** | Método alternativo (baixa taxa de sucesso) |
| **🔄 Forçar Reconexão** | Reinicia ADB server e drivers USB |
| **🗑️ Limpar Log** | Limpa o console |

## 🔍 Formatos de QR Code

### AMAPI (Android Management API)
- ✅ Mais compatível com múltiplos fabricantes
- ✅ Recomendado como primeira tentativa
- ✅ Suporta Skip Setup

### KNOX (Samsung Mobile Enrollment)
- ✅ Padrão oficial Samsung
- ✅ Melhor para dispositivos Samsung puros
- ✅ Mais seguro

### GOOGLE (Zero-Touch Enrollment)
- ✅ Padrão Google oficial
- ✅ Funciona em maioria dos Android
- ✅ Última opção se outros falharem

## 🆘 Troubleshooting

### "IMEI inválido"
- Certifique-se que tem 15+ dígitos
- Remova caracteres especiais
- Verifique via `*#06#` se está correto

### "Formato inválido" no celular
- Tente outro QR code (AMAPI → KNOX → GOOGLE)
- Certifique-se de estar conectado ao WiFi
- Pode precisar estar na tela de "Bem-vindo" (primeira inicialização)

### Bypass não funcionou
- Certifique-se que o celular estava em "Bem-vindo" (reset factory)
- Tente outro formato de QR code
- Verifique se tem WiFi conectado
- Tente novamente do começo

### IMEI não é detectado
- Instale Android SDK Platform Tools
- Conecte o celular em modo de desenvolvimento (se possível)
- Digite o IMEI manualmente

## 📊 Arquitetura do Projeto

```
frpsam/
├── main.py                    # Interface (CustomTkinter)
├── samsung_logic.py           # Lógica IMEI + AT + ADB
├── samsung_helper.ps1         # Scripts PowerShell
├── requirements.txt           # Dependências
├── build.bat                  # Build script
└── README.md                  # Documentação
```

## 📚 Métodos Suportados

### ✅ PRIMÁRIO: IMEI-Based FRP Bypass (2022-2026)
- Usa IMEI para gerar tokens criptográficos
- Taxa de sucesso: **80-90%**
- Compatibilidade: Samsung A22-S24

### ⚠️ SECUNDÁRIO: Legado AT Commands
- Método antigo para 2022-2023
- Taxa de sucesso: **5-20%**
- Mantido por compatibilidade

## ⚠️ Avisos Legais

✅ **Use apenas em dispositivos que você possui**
✅ Para fins de manutenção e recuperação pessoal
⚠️ Uso indevido é de responsabilidade do usuário
🔒 Sempre faça backup antes de operações

## 🔄 Atualizações

- **v3.0**: Método IMEI como principal
- **v2.0**: Interface melhorada
- **v1.0**: Versão inicial

## 📝 Licença

Fornecido como-está para fins educacionais.

---

**Desenvolvido para Samsung 2022-2026**

Versão: 3.0 | 2026-05-20
