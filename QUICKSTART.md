# 🚀 INÍCIO RÁPIDO - Samsung ADB Master v2.0

## ⚡ 30 Segundos para Começar

### No seu PC (Windows)

```bash
# 1. Clonar repo
git clone https://github.com/wesleyabt/frpsam.git
cd frpsam

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Executar
python main.py
```

### No seu Samsung

1. Conecte via USB ao PC
2. Abra Discador → Digite: `*#0*#` → Pressione Chamar
3. Uma tela branca com botões deve aparecer ✓

### No Aplicativo

1. Clique: **"▶ EXECUTAR FLUXO COMPLETO"**
2. No celular: Autorize **"Permitir depuração USB"**
3. Pronto! Tudo automático 🎉

---

## 📦 Para Compilar Executável (.exe)

```bash
# Execute no diretório do projeto:
build.bat

# Resultado: dist/SamsungADBMaster.exe
```

O executável pode ser distribuído sem necessidade de Python!

---

## 📱 O que o Aplicativo Faz

| Etapa | Ação |
|-------|------|
| **1** | Habilita ADB via comandos AT no modo de teste |
| **2** | Força reconhecimento USB (reseta drivers) |
| **3** | Remove conta Google automaticamente |

---

## ⚙️ Requisitos

- Windows 10/11
- Samsung (2022-2026)
- Cabo USB
- Drivers Samsung USB
- Python 3.10+ (só se rodar do código)

---

## 🆘 Problemas Comuns

| Problema | Solução |
|----------|---------|
| Dispositivo não encontrado | Certifique-se que está em `*#0*#` |
| Drivers não instalados | Baixe em: samsung.com/android-usb-driver |
| ADB não autorizado | Procure prompt de USB Debug no celular |
| Python não encontrado | Instale em: python.org/downloads |

---

## 📚 Arquivos Importantes

- `main.py` - Interface gráfica
- `samsung_logic.py` - Lógica ADB
- `build.bat` - Compilador
- `README_v2.md` - Documentação completa

---

**Desenvolvido para Samsung | v2.0 | 2026**
