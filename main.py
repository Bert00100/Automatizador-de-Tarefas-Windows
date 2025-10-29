import subprocess
import os
import platform
import wmi
import psutil
import socket
import ctypes
import sys
from colorama import Fore, Style, init

init(autoreset=True)

def header(title):
    print(Fore.CYAN + f"\n=== {title} ===" + Style.RESET_ALL)

def txt_info(label, value):
    print(Fore.YELLOW + f"{label:<30}: " + Style.RESET_ALL + f"{value}")

def debug_step(step_number, description):
    print(Fore.MAGENTA + f"\n[PASSO {step_number}] " + Fore.WHITE + description + Style.RESET_ALL)

def debug_success(message):
    print(Fore.GREEN + f"  ✓ {message}" + Style.RESET_ALL)

def debug_error(message):
    print(Fore.RED + f"  ✗ {message}" + Style.RESET_ALL)

def debug_warning(message):
    print(Fore.YELLOW + f"  ⚠ {message}" + Style.RESET_ALL)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    debug_warning("Solicitando privilégios de administrador...")
    try:
        script = os.path.abspath(sys.argv[0])
        params = ' '.join([script] + sys.argv[1:])
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
        sys.exit(0)
    except Exception as e:
        debug_error(f"Falha ao solicitar privilégios: {e}")
        return False

def perguntar_continuar():
    while True:
        print("\n" + "="*50)
        print(Fore.CYAN + "1 - Voltar ao Menu Principal" + Style.RESET_ALL)
        print(Fore.CYAN + "0 - Sair" + Style.RESET_ALL)
        opcao = input(Fore.YELLOW + "\nEscolha uma opção: " + Style.RESET_ALL)

        if opcao == "0":
            print(Fore.CYAN + "Encerrando..." + Style.RESET_ALL)
            sys.exit(0)
        elif opcao == "1":
            return
        else:
            print(Fore.RED + "Opção inválida! Tente novamente." + Style.RESET_ALL)

def clearDisk():
    header("As acoes a seguir podem levar algum tempo")
    
    debug_step(1, "Otimizando SSD com ReTrim...")
    improvesSSD = subprocess.run(
        ["powershell", "-Command", "Get-Command Optimize-Volume; Import-Module Storage; Optimize-Volume -DriveLetter C -ReTrim -Verbose"],
        capture_output=True,
        text=True
    )
    print(improvesSSD.stdout)
    if improvesSSD.returncode == 0:
        debug_success("SSD otimizado com sucesso")
    else:
        debug_warning("Aviso ao otimizar SSD")

    debug_step(2, "Executando limpeza de arquivos (sagerun:1)...")
    clearFiles01 = subprocess.run(
        ["powershell", "-Command", "cleanmgr /sagerun:1"],
        capture_output=True,
        text=True
    )
    print(clearFiles01.stdout)
    if clearFiles01.returncode == 0:
        debug_success("Limpeza 01 concluída")
    else:
        debug_warning("Aviso na limpeza 01")

    debug_step(3, "Executando limpeza de arquivos (sagerun:2)...")
    clearFiles02 = subprocess.run(
        ["powershell", "-Command", "cleanmgr /sagerun:2"],
        capture_output=True,
        text=True
    )
    print(clearFiles02.stdout)
    if clearFiles02.returncode == 0:
        debug_success("Limpeza 02 concluída")
    else:
        debug_warning("Aviso na limpeza 02")

    debug_step(4, "Desfragmentando disco C:...")
    clearDefrag = subprocess.run(
        ["powershell", "-Command", "defrag C: /U /V"],
        capture_output=True,
        text=True
    )
    print(clearDefrag.stdout)
    if clearDefrag.returncode == 0:
        debug_success("Desfragmentação concluída")
    else:
        debug_warning("Aviso na desfragmentação")

    erros = []
    if improvesSSD.stderr.strip():
        erros.append("Melhora de SSD")
    if clearFiles01.stderr.strip():
        erros.append("Limpeza de arquivos 01")
    if clearFiles02.stderr.strip():
        erros.append("Limpeza de arquivos 02")
    if clearDefrag.stderr.strip():
        erros.append("Desfragmentar o disco")

    if erros:
        print(f"Ocorreu um erro(s) ao limpar: {', '.join(erros)}")
    else:
        txt_info("Disco Limpo e Melhorado com Sucesso", "")

def infoMachine():
    debug_step(1, "Coletando informações do sistema...")
    
    header("Informações do Sistema")
    txt_info("Nome da Máquina", platform.node())
    txt_info("Nome do Usuário", os.getlogin())
    txt_info("Versão do Sistema Operacional", platform.platform())
    debug_success("Informações do sistema coletadas")

    debug_step(2, "Coletando informações da BIOS...")
    header("Informações da BIOS")
    try:
        c = wmi.WMI()
        for bios in c.Win32_BIOS():
            txt_info("Serial Number", bios.SerialNumber if bios.SerialNumber else "N/A")
        debug_success("Informações da BIOS coletadas")
    except Exception as e:
        debug_error(f"Erro ao coletar BIOS: {e}")

    debug_step(3, "Coletando informações de rede...")
    header("Informações da Placa de Rede")
    try:
        ip_interfaces = psutil.net_if_addrs()
        for interface_name, addresses in ip_interfaces.items():
            for address in addresses:
                if address.family == socket.AF_INET:
                    txt_info(f"Interface: {interface_name}", address.address)
        debug_success("Informações de rede coletadas")
    except Exception as e:
        debug_error(f"Erro ao coletar rede: {e}")

def scanWin():
    header("Scan e Reparo do Windows (DISM)")

    debug_step(1, "Verificando privilégios de administrador...")
    if not is_admin():
        debug_error("Este script precisa ser executado como ADMINISTRADOR!")
        debug_warning("A limpeza de RAM requer privilégios elevados.")
        
        resposta = input(Fore.YELLOW + "\nDeseja reiniciar como administrador? (s/n): " + Style.RESET_ALL)
        if resposta.lower() == 's':
            run_as_admin()
            return "Reiniciando como administrador..."
        else:
            debug_warning("Continuando sem limpeza de RAM...")
    else:
        debug_success("Privilégios de administrador confirmados")
    
    debug_step(1, "Iniciando DISM /RestoreHealth...")
    debug_warning("Este processo pode levar vários minutos")
    
    with subprocess.Popen(
        ["powershell", "-Command", "DISM /Online /Cleanup-Image /RestoreHealth"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    ) as proc:
        for line in proc.stdout:
            print(line, end="")
    
    retcode = proc.wait()
    if retcode != 0:
        debug_error(f"Comando retornou código {retcode}")
        return f"Error: comando retornou código {retcode}"
    else:
        debug_success("DISM concluído com sucesso")
        return "OK"


def clearNet():
    header("LIMPEZA DE REDE")
    
    debug_step(1, "Verificando privilégios de administrador...")
    if not is_admin():
        debug_error("Este script precisa ser executado como ADMINISTRADOR!")
        debug_warning("A limpeza de rede requer privilégios elevados.")
        
        resposta = input(Fore.YELLOW + "\nDeseja reiniciar como administrador? (s/n): " + Style.RESET_ALL)
        if resposta.lower() == 's':
            run_as_admin()
            return "Reiniciando como administrador..."
        else:
            debug_warning("Continuando sem privilégios...")
    else:
        debug_success("Privilégios de administrador confirmados")

    erros = []

    debug_step(2, "Limpando DNS da máquina...")
    flushDNS = subprocess.run(
        ["powershell", "-Command", "ipconfig /flushdns"],
        capture_output=True,
        text=True
    )

    if flushDNS.stderr.strip():
        erros.append("Flush DNS")
        debug_error("Erro ao limpar o DNS da máquina")
    else:
        debug_success("Limpeza do DNS realizada com sucesso!")
    
    debug_step(3, "Re-register do DNS...")
    reRegistDNS = subprocess.run(
        ["powershell", "-Command", "ipconfig /registerdns"],
        capture_output=True,
        text=True
    )

    if reRegistDNS.stderr.strip():
        erros.append("Re-Register do DNS")
        debug_error("Erro ao fazer o re-register da máquina")
    else:
        debug_success("Re-register da máquina feito com sucesso!")

    debug_step(4, "Fazendo release do IP...")
    renIP_rel = subprocess.run(
        ["powershell", "-Command", "ipconfig /release"],
        capture_output=True,
        text=True
    )

    if renIP_rel.stderr.strip():
        erros.append("Release IP")
        debug_error("Aviso ao executar release do IP")
    else:
        debug_success("Release do IP executado!")

    debug_step(5, "Renew do IP...")
    renIP_ren = subprocess.run(
        ["powershell", "-Command", "ipconfig /renew"],
        capture_output=True,
        text=True
    )

    if renIP_ren.stderr.strip():
        erros.append("Renew do IP")
        debug_error("Aviso ao executar o renew do IP")
    else:
        debug_success("Renew do IP feito!")
    
    debug_step(6, "Reset de IP...")
    restTcpIP = subprocess.run(
        ["powershell", "-Command", "netsh int ip reset"],
        capture_output=True,
        text=True
    )

    if restTcpIP.stderr.strip():
        erros.append("Reset de IP")
        debug_error("Aviso ao resetar IP")
    else:
        debug_success("Reset do IP feito!")
    
    debug_step(7, "Reset do Winsock...")
    resetWiSock = subprocess.run(
        ["powershell", "-Command", "netsh winsock reset"],
        capture_output=True,
        text=True
    )

    if resetWiSock.stderr.strip():
        erros.append("Reset do WinSock")
        debug_error("Aviso ao resetar o WinSock")
    else:
        debug_success("Reset do Winsock feito com sucesso!")

    if erros:
        return f"Ocorreu um erro ao executar: {', '.join(erros)}"
    else:
        debug_success("Limpeza de rede concluída!")
        return "Limpeza da Rede WiFi/Ethernet concluída"

def testPing():
    header("Teste de Ping")

    erros = []
        
    debug_step(1, "Ping do DNS Google..")
    pingGoogle = subprocess.run(
    ["powershell", "-Command", "ping 8.8.8.8"],
       capture_output=True,
       text=True
    )

    if pingGoogle.stderr.strip():
        erros.append("Erro ao pingar DNS Google")
    else:
        print(pingGoogle.stdout)
        debug_success("Ping bem sucedido")

def mapNet():
    header("Mapa de conexão")

    debug_step(1, "Verificando privilégios de administrador...")
    if not is_admin():
        debug_error("Este script precisa ser executado como ADMINISTRADOR!")
        debug_warning("A limpeza de RAM requer privilégios elevados.")
        
        resposta = input(Fore.YELLOW + "\nDeseja reiniciar como administrador? (s/n): " + Style.RESET_ALL)
        if resposta.lower() == 's':
            run_as_admin()
            return "Reiniciando como administrador..."
        else:
            debug_warning("Continuando sem limpeza de RAM...")
    else:
        debug_success("Privilégios de administrador confirmados")
    
    erros = []

    debug_step(2, "Localizar Servidor")
    net = input("Digite o Servidor que deseja Mapear: ")

    debug_step(3, "Mapeando a rede...")
    print("ATENÇÃO ISSO PODE LEVAR UM TEMPO")
    trackNet = subprocess.run(
        ["powershell", "-Command", f"tracert {net}"],
        capture_output=True,
        text=True
    )

    if trackNet.stderr.strip():
        erros.append("Servidor não encontrado")
        debug_error("Erro ao mapear o Servidor")
    else:
        print(trackNet.stdout)
        debug_success("Servidor Mapeado com sucesso")

def restartPoint():
    header("Criando Ponto de Restauração")

    erros = []

    debug_step(1, "Executando ferramente de ponto de Restauração")
    point = subprocess.run(
        ["SystemPropertiesProtection.exe"],
        shell=True, 
        capture_output= True, 
        text= True
    )

    if point.stderr.strip():
        erros.append("Execução de Ponto de Restauração")
        debug_error("Erro ao executar ponto de restauração")
    else:
        debug_success("Ponto de Restauração Criado.")



def mostrarmenu():
    opcoes = [
        "[ 1 ] Informação da Máquina",
        "[ 2 ] Limpar SSD/HD",
        "[ 3 ] Scanner do Windows",
        "[ 4 ] Limpar Caches de Wifi/Ethernet",
        "[ 5 ] Teste de Ping",
        "[ 6 ] Mapa de Conexão",
        "[ 7 ] Criar Ponto de Restauração",
        "[ 0 ] Sair"
    ]

    print("Selecione a opção que você quer realizar:\n")
    for opcao in opcoes:
        print(opcao)

while True:
    mostrarmenu()
    op = input(Fore.YELLOW + "\nQual opção você deseja executar: " + Style.RESET_ALL)

    if op == "1":
        infoMachine()
        perguntar_continuar()
    elif op == "2":
        clearDisk()
        perguntar_continuar()
    elif op == "3":
        resultado = scanWin()
        print(Fore.GREEN + f"\n{resultado}" + Style.RESET_ALL)
        perguntar_continuar()
    elif op == "4":
        resultado = clearNet()
        print(Fore.GREEN + f"\n{resultado}" + Style.RESET_ALL)
        perguntar_continuar()
    elif op == "5":
        resultado = testPing()
        print(Fore.GREEN + f"\n{resultado}" + Style.RESET_ALL)
        perguntar_continuar()
    elif op == "6":
        resultado = mapNet()
        print(Fore.GREEN + f"\n{resultado}" + Style.RESET_ALL)
        perguntar_continuar()
    elif op == "7": 
        resultado = restartPoint()
        print(Fore.GREEN + f"\n{resultado}" + Style.RESET_ALL)
        perguntar_continuar()
    elif op == "0":
        print(Fore.CYAN + "Encerrando..." + Style.RESET_ALL)
        sys.exit(0)
    else:
        print(Fore.RED + "Opção inválida!" + Style.RESET_ALL)
        perguntar_continuar()