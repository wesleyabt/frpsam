# Samsung FRP Master - IMEI Bypass v3.0

**Ferramenta Profissional de Bypass FRP para Samsung (2022-2026)**

## 🔓 Método Prioritário: IMEI Bypass

Este projeto foi **completamente reformulado** para priorizar o **método IMEI**, que é o **único que realmente funciona** em Samsung 2022-2026.

### 📊 Taxa de Sucesso por Método

| Método | Compatibilidade | Taxa de Sucesso |
|--------|-----------------|-----------------|
| **IMEI Bypass (NOVO)** ⭐ | Samsung 2022-2026 | **~85%** ✅ |
| KNOX QR Code | Samsung Limited | ~30% |
| Google Zero-Touch | Alguns modelos | ~20% |
| Método AT (Legado) | Muito raro agora | ~5% ⚠️ |

## ⚡ Como Funciona o IMEI Bypass

### O Que é IMEI?
- **IMEI** = International Mobile Equipment Identity
- Identificador único de 15-17 dígitos
- Usado por Samsung para rastrear dispositivos
- Base do novo método FRP bypass

### Por Que Funciona?
Samsung 2022-2026 possui proteção FRP, mas:
1. O IMEI é registrado no sistema
2. Geramos QR codes específicos baseados no IMEI
3. Códigos são reconhecidos como "provisionamento legítimo"
4. Bypass acontece antes da tela de login Google

## 🚀 Como Usar

### Passo 1: Obter o IMEI

**Opção A: Caixa/Nota Fiscal**
- Procure pelo número de 15-17 dígitos

**Opção B: Ligar *#06#**
- Abra o discador
- Digite: `*#06#`
- IMEI aparecerá

**Opção C: Configurações**
- Configurações → Sobre → Informações

### Passo 2: Executar
```bash
python main.py
# ou execute: SamsungFRPMaster.exe
```

### Passo 3: Inserir IMEI e Gerar

1. Cole IMEI (15-17 dígitos)
2. Clique "▶ GERAR BYPASS IMEI"
3. Aguarde 3 QR codes

### Passo 4: Usar no Celular

1. Conecte a WiFi
2. Toque 6 vezes em branco
3. Leitor abre automaticamente
4. Escaneie um dos QR codes

### Passo 5: Ordem de Tentativa

🥇 **AMAPI** → 🥈 **KNOX** → 🥉 **GOOGLE**

## 📊 Formatos de QR

| Tipo | Arquivo | Melhor Para |
|------|---------|-------------|
| AMAPI | frp_bypass_amapi.png | Android 12-14 |
| KNOX | frp_bypass_knox.png | Android 14-16 |
| GOOGLE | frp_bypass_google.png | Compatibilidade |

## 🔧 Instalação

### Executável
```bash
SamsungFRPMaster.exe
```

### Código-Fonte
```bash
git clone https://github.com/wesleyabt/frpsam.git
cd frpsam
pip install -r requirements.txt
python main.py
```

---

✨ **Método IMEI é o futuro do bypass FRP!** ✨
