# Samsung ADB Master v2.0

**Enable ADB | Force Recognition | Remove Google Account**

Uma ferramenta completa para habilitar ADB em dispositivos Samsung (2022-2026), forçar reconhecimento no Windows e remover contas Google automaticamente.

## 🚀 Recursos

- ✅ **Habilitar ADB via Comandos AT** - Funciona em modo de teste (*#0*#)
- ✅ **Forçar Reconhecimento** - Reset de drivers USB e ADB Server
- ✅ **Remover Conta Google** - Desativa Google Play Services e limpa dados
- ✅ **Fluxo Automático Completo** - Executa as 3 etapas em sequência
- ✅ **Interface Moderna** - CustomTkinter com logs em tempo real
- ✅ **Suporte Windows** - Otimizado para Windows 10/11

## 📋 Requisitos

- **Sistema Operacional**: Windows 10 ou Windows 11
- **Smartphone**: Samsung (2022-2026)
- **Conexão**: Cabo USB de qualidade
- **Drivers**: Samsung USB Drivers instalados

### Para Desenvolvedores
- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)

## 🔧 Instalação

### Opção 1: Usar o Executável (Recomendado)
1. Baixe `SamsungADBMaster.exe` em Releases
2. Execute o arquivo
3. Siga as instruções na interface

### Opção 2: Compilar do Código-Fonte

```bash
# 1. Clonar repositório
git clone https://github.com/wesleyabt/frpsam.git
cd frpsam

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Executar aplicação
python main.py
```

### Opção 3: Compilar para Executável

```bash
# Windows: Execute o script de build
build.bat

# Ou manualmente:
pip install -r requirements.txt
pyinstaller --noconfirm --onefile --windowed ^
    --name "SamsungADBMaster" ^
    --add-data "samsung_helper.ps1;." ^
    main.py
```

## 📱 Como Usar

### Passo 1: Preparar o Celular
1. Conecte o Samsung ao computador via USB
2. Abra o aplicativo de Discador (telefone)
3. Digite: `*#0*#` e pressione chamar
4. Uma tela branca com botões deve aparecer (Modo de Teste)

### Passo 2: Executar a Ferramenta
1. Abra `SamsungADBMaster.exe`
2. Leia as instruções no topo
3. Clique em **"▶ EXECUTAR FLUXO COMPLETO"** ou escolha etapas individuais

### Passo 3: Autorizar no Celular
1. Quando solicitado, procure por: **"Permitir depuração USB?"**
2. Marque **"Sempre permitir neste computador"**
3. Clique **"OK"** ou **"SIM"**

### Passo 4: Aguardar Conclusão
- O aplicativo executará automaticamente:
  - ✓ Habilita ADB via AT
  - ✓ Força reconhecimento USB
  - ✓ Remove conta Google
- Verifique o console para logs detalhados

## 🎮 Botões da Interface

| Botão | Função |
|-------|--------|
| **▶ EXECUTAR FLUXO COMPLETO** | Executa as 3 etapas automaticamente (recomendado) |
| **1. Habilitar ADB** | Apenas ativa ADB via comandos AT |
| **2. Forçar Reconexão** | Reset de drivers e servidor ADB |
| **3. Remover Google** | Remove conta Google (requer ADB autorizado) |

## 🔍 Solução de Problemas

### "Dispositivo Samsung não encontrado"
- Certifique-se de que o celular está em modo de teste (*#0*#)
- Reconecte o cabo USB
- Tente uma porta USB diferente
- Reinstale drivers Samsung USB

### "Dispositivo não autorizado"
- Procure pela mensagem "Permitir depuração USB?" no celular
- Marque "Sempre permitir neste computador"
- Clique "OK"
- Se ainda não aparecer, reinstale o ADB

### "Conta Google não foi removida"
- Verifique se o ADB está realmente ativado
- Tente executar manualmente: `Configurações → Contas → Google`
- Remova a conta manualmente se necessário

## 📊 Arquitetura

```
frpsam/
├── main.py                 # Interface gráfica (CustomTkinter)
├── samsung_logic.py        # Lógica de ADB e AT commands
├── samsung_helper.ps1      # Scripts PowerShell (detecção de drivers)
├── build.bat              # Script de compilação Windows
├── requirements.txt       # Dependências Python
└── README.md             # Este arquivo
```

## 🛠️ Dependências

- **customtkinter** - Interface gráfica moderna
- **pyserial** - Comunicação serial (AT commands)
- **pyinstaller** - Compilação para .exe
- **qrcode** - Geração de QR codes (backup)
- **pillow** - Processamento de imagens

## ⚠️ Avisos Legais

- ✅ Use apenas em dispositivos que você possui
- ✅ Esta ferramenta é para fins de manutenção e desenvolvimento
- ⚠️ O uso indevido para contornar proteções em dispositivos alheios é ilegal
- 🔒 Certifique-se de ter backups antes de executar

## 📞 Suporte

- 🐛 Reportar bugs: [Issues no GitHub](https://github.com/wesleyabt/frpsam/issues)
- 💬 Sugestões: Abra uma discussion no repositório
- 📖 Documentação: Veja a wiki do projeto

## 📝 Licença

Este projeto é fornecido como-está para fins educacionais e de manutenção.

## 👨‍💻 Contribuindo

Contribuições são bem-vindas! Por favor:
1. Fork o repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

---

**Desenvolvido com ❤️ para Samsung**

Versão: 2.0 | Última atualização: 2026-05-20
