# 🛠️ Windows System Optimizer

Script Python completo para otimização, manutenção e diagnóstico de sistemas Windows. Oferece ferramentas essenciais para melhorar o desempenho e resolver problemas comuns de rede e armazenamento.

## ✨ Funcionalidades

### 1. 📊 Informações da Máquina
- Coleta dados completos do sistema operacional
- Informações da BIOS (Serial Number)
- Detalhes de interfaces de rede e endereços IP
- Nome da máquina e usuário atual

### 2. 🗑️ Limpeza de SSD/HD
- Otimização de SSD com ReTrim
- Limpeza automática de arquivos temporários (2 passes)
- Desfragmentação de disco
- Liberação de espaço em disco

### 3. 🔍 Scanner do Windows
- Executa DISM (Deployment Image Servicing and Management)
- Reparo automático de corrupção do sistema
- Restauração de integridade do Windows
- Exibe progresso em tempo real

### 4. 🌐 Limpeza de Cache de Rede
- Flush de cache DNS
- Re-registro de DNS
- Release e renovação de IP
- Reset de TCP/IP
- Reset do Winsock
- Solução para problemas de conectividade

### 5. 📡 Teste de Ping
- Teste de conectividade com DNS do Google (8.8.8.8)
- Diagnóstico rápido de conexão à internet
- Exibição de latência e perda de pacotes

### 6. 🗺️ Mapa de Conexão
- Rastreamento de rota até servidor específico (tracert)
- Identificação de pontos de falha na rede
- Análise de saltos de conexão

### 7. 💾 Ponto de Restauração
- Acesso rápido à ferramenta de criação de pontos de restauração
- Interface nativa do Windows para backup do sistema

## 🔧 Requisitos

### Dependências Python
```bash
pip install wmi psutil colorama
```

### Bibliotecas necessárias:
- `subprocess` (built-in)
- `os` (built-in)
- `platform` (built-in)
- `wmi` - Acesso a informações WMI do Windows
- `psutil` - Informações de sistema e rede
- `socket` (built-in)
- `ctypes` (built-in)
- `sys` (built-in)
- `colorama` - Interface colorida no terminal

### Sistema Operacional
- **Windows 10/11** (recomendado)
- **Privilégios de Administrador** necessários para maioria das funções

## 🚀 Como Usar

### Instalação

1. Clone o repositório ou baixe o script:
```bash
git clone https://github.com/seu-usuario/windows-optimizer.git
cd windows-optimizer
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

### Execução

**Execute como Administrador** (recomendado):
```bash
# Clique com botão direito no terminal e selecione "Executar como Administrador"
python optimizer.py
```

O script solicitará automaticamente privilégios de administrador quando necessário para operações específicas.

## 📋 Menu Principal

```
Selecione a opção que você quer realizar:

[ 1 ] Informação da Máquina
[ 2 ] Limpar SSD/HD
[ 3 ] Scanner do Windows
[ 4 ] Limpar Caches de Wifi/Ethernet
[ 5 ] Teste de Ping
[ 6 ] Mapa de Conexão
[ 7 ] Criar Ponto de Restauração
[ 0 ] Sair
```

## ⚠️ Avisos Importantes

- ⚡ **Privilégios de Administrador**: Várias funções requerem execução como administrador
- ⏱️ **Tempo de Execução**: Algumas operações (limpeza de disco, DISM, desfragmentação) podem levar vários minutos
- 💾 **Ponto de Restauração**: Recomenda-se criar um ponto de restauração antes de executar operações de limpeza
- 🌐 **Conexão de Rede**: A limpeza de cache de rede pode interromper temporariamente a conectividade

## 🎨 Interface

O script utiliza código de cores para melhor visualização:

- 🔵 **Ciano**: Títulos e menus
- 🟡 **Amarelo**: Informações e prompts
- 🟢 **Verde**: Operações bem-sucedidas
- 🔴 **Vermelho**: Erros
- 🟣 **Magenta**: Passos de execução

## 🐛 Solução de Problemas

### "Este script precisa ser executado como ADMINISTRADOR"
- Feche o terminal
- Abra o CMD ou PowerShell como Administrador
- Execute novamente o script

### Erro de módulo não encontrado
```bash
pip install wmi psutil colorama
```

### Operação demora muito tempo
- Operações como DISM e desfragmentação podem levar 10-30 minutos
- Aguarde a conclusão ou cancele com Ctrl+C

## 📝 Licença

Este projeto é de código aberto. Sinta-se livre para usar, modificar e distribuir.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests

## 📧 Contato

Para dúvidas ou sugestões, abra uma issue no repositório.

---

**⭐ Se este projeto foi útil, considere dar uma estrela no GitHub!**