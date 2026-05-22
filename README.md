# 🔓 Samsung FRP Bypass Master v3.0

**Ferramenta completa para desbloquear Samsung com proteção FRP (2022-2026)**

## ✨ Funcionalidades Principais

- ✅ **IMEI Bypass** (Método Principal - Taxa ~85%)
- ✅ **QR Code Multi-Formato** (AMAPI, KNOX, GOOGLE)
- ✅ **Auto-detecção de IMEI** via ADB
- ✅ **Métodos Alternativos** (AT legado + reconexão)
- ✅ **Interface Intuitiva** com status em tempo real
- ✅ **Console de Logs** detalhado

---

## 🚀 Instalação Rápida

### Requisitos
- **Windows 10/11**
- **Drivers Samsung USB** instalados
- **Cabo USB** de boa qualidade
- **Python 3.10+** (se rodar pelo código)

### Passo 1: Clonar o Repositório
```bash
git clone https://github.com/wesleyabt/frpsam.git
cd frpsam
```

### Passo 2: Instalar Dependências
```bash
pip install -r requirements.txt
```

### Passo 3: Executar
```bash
python main.py
```

---

## 📱 Como Usar (Passo a Passo)

### 1️⃣ Preparar o Celular
- Conecte o Samsung ao PC via **USB**
- Celular deve estar **na tela de boas-vindas** ou **formatado recentemente**

### 2️⃣ Obter o IMEI
**Opção A (Automática - RECOMENDADA)**
```
[No App] → Clique "🔍 Detectar IMEI"
```

**Opção B (Manual)**
```
[No Celular] → Telefone → Disque #06# → Copie o IMEI
[No App] → Cole no campo de entrada
```

### 3️⃣ Gerar Bypass FRP
```
[No App] → Clique "▶ GERAR BYPASS FRP VIA IMEI"
```
- O app gerará **3 QR codes** em formatos diferentes
- QR codes salvos em: `frp_bypass_amapi.png`, `frp_bypass_knox.png`, `frp_bypass_google.png`

### 4️⃣ Escanear QR Code
```
[No Celular] → Na tela de boas-vindas, toque 6 vezes em qualquer espaço vazio
→ Abre o leitor de QR Code
→ Aponte a câmera para um dos QR codes gerados
```

### 5️⃣ Completar Setup
- O celular processar o QR Code
- Se aceito: **Bypass FRP ativado** ✅
- Se der erro de formato: **Tente outro QR code**

---

## 📦 Compilar Executável (.exe)

Para distribuir sem necessidade de Python:

```bash
# No diretório do projeto:
build.bat

# Resultado: dist/SamsungFRPBypass.exe
```

Então você pode compartilhar apenas o arquivo `.exe`

---

## 🔧 Métodos Disponíveis

### 1️⃣ IMEI Bypass (PRINCIPAL)
- **Taxa de Sucesso**: ~85% ✅
- **Compatibilidade**: 2022-2026
- **Tempo**: ~2 minutos

### 2️⃣ Método Legado AT
- **Taxa de Sucesso**: ~10%
- **Compatibilidade**: 2022-2023 (principalmente)
- **Quando usar**: Se IMEI não funcionar

### 3️⃣ Forçar Reconexão
- **Função**: Reset de drivers USB
- **Quando usar**: Como complemento dos outros métodos

---

## 📊 Formato dos QR Codes

| Formato | Compatibilidade | Descrição |
|---------|-----------------|-----------|
| **AMAPI** | Android 14+ | Android Management API (padrão) |
| **KNOX** | Samsung 2024+ | KNOX Mobile Enrollment (oficial Samsung) |
| **GOOGLE** | Android 13+ | Google Provisioning (compatibilidade máxima) |

**Dica**: Tente **AMAPI** primeiro. Se der erro, tente **KNOX** ou **GOOGLE**.

---

## ⚙️ Desenvolvimento

### Estrutura do Projeto

```
frpsam/
├── main.py                 # Interface gráfica (CustomTkinter)
├── samsung_logic.py        # Lógica de bypass (IMEI, QR, etc)
├── build.bat              # Script para compilar .exe
├── requirements.txt       # Dependências Python
├── QUICKSTART.md          # Guia rápido
└── README.md              # Este arquivo
```

### Dependências

```
customtkinter>=5.0
pyserial>=3.5
pyinstaller>=6.0
qrcode[pil]>=7.4
pillow>=10.0
```

### Executar em Desenvolvimento

```bash
python main.py
```

---

## 🐛 Troubleshooting

### ❌ "IMEI não detecta"
**Solução**:
1. Verifique se o celular está conectado ao PC
2. Instale/atualize drivers Samsung USB
3. Execute `adb devices` no PowerShell para confirmar conexão
4. Tente digitar manualmente (disque `#06#` no celular)

### ❌ "QR Code - Formato Inválido"
**Solução**:
1. Tente outro formato (KNOX → GOOGLE → AMAPI)
2. Certifique-se que o celular tem bateria suficiente
3. Verifique se está na tela correta (boas-vindas)

### ❌ "Bypass não funciona"
**Solução**:
1. Tente o **Método Legado AT** como alternativa
2. Use **Forçar Reconexão** para reset de drivers
3. Desconecte/reconecte o cabo e tente novamente

---

## 📝 Licença

Este projeto é para **fins educacionais e de manutenção**.

---

## 🎯 Próximas Versões

- 🔜 Suporte a Samsung tablets
- 🔜 Integração com mais métodos de bypass
- 🔜 Interface em português/inglês/espanhol

---

**Desenvolvido por Wesley Santos**  
📧 [GitHub: wesleyabt](https://github.com/wesleyabt)  
⭐ Se foi útil, deixe uma estrela! ⭐
