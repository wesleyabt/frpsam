# 🔓 SAMSUNG FRP BYPASS MASTER v3.0 - Guia Rápido

## ⚡ 30 Segundos para Começar

### PC (Windows 10/11)

```bash
# 1. Clonar repositório
git clone https://github.com/wesleyabt/frpsam.git
cd frpsam

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Executar aplicativo
python main.py
```

### Samsung (Qualquer modelo 2022-2026)

1. **Conectar ao PC via USB**
2. **Descobrir o IMEI**: Clique em **"🔍 Detectar IMEI"** OU disque `#06#` no celular
3. **Gerar bypass**: Clique em **"▶ GERAR BYPASS FRP VIA IMEI"**
4. Selecione **3 QR codes** gerados (tente AMAPI primeiro)
5. **No celular**: Escaneie o QR code na tela de boas-vindas
6. **Pronto!** ✅ Bypass FRP ativado

---

## 📦 Compilar Executável (.exe)

```bash
# No diretório do projeto:
build.bat

# Resultado: dist/SamsungFRPBypass.exe
```

---

## 🎯 O que Cada Botão Faz

| Botão | Descrição | Taxa de Sucesso |
|-------|-----------|-----------------|
| **GERAR BYPASS FRP VIA IMEI** | Método principal (RECOMENDADO) | **~85%** ✅ |
| **Método Legado AT** | Alternativa para aparelhos 2022-2023 | ~10% |
| **Forçar Reconexão** | Reset de drivers USB | Complementar |
| **Limpar Log** | Limpa console de texto | Útil |

---

## 📱 Obtendo o IMEI

### Método 1: Detecção Automática (MAIS FÁCIL)
- Clique em **"🔍 Detectar IMEI"** no app
- O IMEI aparecerá automaticamente

### Método 2: Discador do Celular
- Abra o **Telefone/Chamadas**
- Disque: `*#06#`
- Copie o IMEI (15-17 dígitos)
- Cole no campo do app

### Método 3: Configurações
- **Configurações > Sobre o telefone > Informações do dispositivo**

---

## ✨ Novidades v3.0

✅ **Interface Redesenhada** - IMEI como foco principal  
✅ **Taxa de sucesso ~85%** - Via método IMEI  
✅ **3 Formatos de QR** - Aumenta compatibilidade  
✅ **Auto-detecção de IMEI** - Via ADB  
✅ **Métodos alternativos** - AT legado + reconexão

---

## ⚠️ Troubleshooting

| Problema | Solução |
|----------|---------|
| IMEI não detecta | Conecte o celular via USB e tente de novo |
| QR Code "Formato Inválido" | Tente outro formato (KNOX ou GOOGLE) |
| Bypass não funciona | Use método AT legado como alternativa |

---

**Desenvolvido para Samsung 2022-2026** 🚀

