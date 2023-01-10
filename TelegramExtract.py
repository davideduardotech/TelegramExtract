"""
CODDING: Bot(Python) de automação para Extrair/Adicionar membros em grupos do Telegram de forma 100% automática
• DESENVOLVEDOR(GITHUB): https://github.com/davideduardotech
"""

from telethon.sync import TelegramClient
from telethon import functions, types,errors
from telethon.errors import FloodWaitError
from datetime import datetime
import re, sys, time, os
import json
import random
from colorama import Fore, init
init(autoreset=True, convert=True)



"""
CODDING: Variaveis
• Variaveis Responsaveis por Controlar/Gerenciar Sistema
"""
TOTAL_DE_MEMBROS_ADICIONADO = 0



"""
CODDING: TelegramExtract <Class>
• Conectar no Telegram com Telethon
• Extrair/Adicionar Membros em Grupos do Telegram
"""
class TelegramExtract:
    def configuracoes(newConfiguracoes=None):
        """
        Função responsavel por retornar/atualizar configurações e contas do Telegram do arquivo TelegramExtract.json
        """
        
        #$ CODDING: VARIAVEIS DE MENSAGEM
        MENSAGEM_DE_ARQUIVO_DE_CONFIGURACAO_NAO_ENCONTRADO = f'{Fore.RED}[ARQUIVO NÃO ENCONTRADO]{Fore.RESET} Arquivo dependente "TelegramExtract.json" não encontrado, impossivel iniciar realize o download novamente em https://github.com/davideduardotech/TelegramExtract'
        
        if newConfiguracoes:
            try:
                with open('TelegramExtract.json', 'w') as f:
                    #$ Atualizar --> TelegramExtract.json
                    json.dump(newConfiguracoes, f)
                textExtract = open("TelegramExtract.json","r")
                textExtract = textExtract.read()
                return json.loads(textExtract) #$ Return: {"grupo.id":...,"Membros Filtrados":...,"Telegram Accounts":...} </dicionario>
            except Exception as erro:
                return False
        else:
            try:
                textExtract = open("TelegramExtract.json","r")
                textExtract = textExtract.read()
                return json.loads(textExtract) #$ Return: {"grupo.id":...,"Membros Filtrados":...,"Telegram Accounts":...} </dicionario>
            except Exception as erro:
                print(MENSAGEM_DE_ARQUIVO_DE_CONFIGURACAO_NAO_ENCONTRADO)
                TelegramExtract.exit()
    
    def conectar_em_conta_do_telegram(phone,api_id,api_hash):
        """
        Função responsavel por conectar na sua conta no Telegram usando as seguintes informações PHONE, API_ID e API_HASH
        """
        
        #$ CODDING: VARIAVEIS DE MENSAGENS
        MENSAGEM_DE_CONTA_CONECTADA = f'{Fore.GREEN}[CONTA DO TELEGRAM]{Fore.RESET} Telegram({phone}) Conectado'
        MENSAGEM_SENDCODE = f'{Fore.GREEN}[CONTA DO TELEGRAM]{Fore.RESET} Digite seu codigo de confirmação({phone}):'
        MENSAGEM_FLOODERROR = f'{Fore.GREEN}[CONTA DO TELEGRAM]{Fore.RESET} FloadError detectado na conta({phone}) para aguardar </NUMBERS> segundos, impossivel conectar na conta...'
        MENSAGEM_ACCOUNT_BANNED = f'{Fore.RED}[CONTA DO TELEGRAM]{Fore.RESET} Conta do Telegram({phone}) Banida'
        MENSAGEM_ERROR = f'{Fore.RED}[CONTA DO TELEGRAM]{Fore.RESET} Não foi possivel conectar na conta do Telegram({phone})'
        
        
        try:
            client = TelegramClient(phone, api_id,api_hash)
            client.connect()
            
            
            if not client.is_user_authorized():
                try:
                    client.send_code_request(phone)
                    print(MENSAGEM_SENDCODE,end=" ")
                    client.sign_in(phone, input())
                
                except errors.FloodError as erro:
                    numbers = ""
                    for caracter in erro.args[0]:
                        if caracter.isdigit():
                            numbers += caracter
                    print(MENSAGEM_FLOODERROR.replace("</NUMBERS>",numbers),end='')
                    return (False , None)
                except errors.PhoneNumberBannedError as erro:
                    print(MENSAGEM_ACCOUNT_BANNED)
                    return (False, None)
                except Exception as erro:
                    return (False, None)
            if client.is_connected():
                print(MENSAGEM_DE_CONTA_CONECTADA)
                return (True, client)
            else:
                print(MENSAGEM_ERROR)
                return (False, None)   
        except errors.FloodError as erro:
            numbers = ""
            for caracter in erro.args[0]:
                if caracter.isdigit():
                    numbers += caracter
            print(MENSAGEM_FLOODERROR.replace("</NUMBERS>",numbers),end='')
            return (False, None)
        except Exception as erro:
            print(MENSAGEM_ERROR)
            return (False,None)
    def adicionar_membros(client,grupo,account):
        global TOTAL_DE_MEMBROS_ADICIONADO
        TelegramExtractJSON = TelegramExtract.configuracoes()
        for usuario in TelegramExtractJSON["Membros Filtrados"][:TelegramExtractJSON["Sistema Anti-Spam"]["limide de adicao de membros por conta"]]:
            usuario_entity = client.get_input_entity(usuario["username"])
            try:
                client(functions.channels.InviteToChannelRequest(grupo,[usuario_entity]))
                TOTAL_DE_MEMBROS_ADICIONADO += 1
                #$ COODDING: Remover Usuario da Lista de Membros Filtrados
                try:
                    TelegramExtractJSON["Membros Filtrados"].remove(usuario)
                    TelegramExtractJSON = TelegramExtract.configuracoes(newConfiguracoes=TelegramExtractJSON)
                except Exception as erro:
                    print(erro)
                print(f"{Fore.GREEN}{account.replace('.session','')}{Fore.RESET} adicionou","{}".format(Fore.GREEN,usuario["username"],Fore.RESET),"no grupo | {}No total, {}".format(Fore.LIGHTBLACK_EX,'Apenas 1 Membro foi Adicionado' if TOTAL_DE_MEMBROS_ADICIONADO == 1 else '{} Membros foram adicionados'.format(TOTAL_DE_MEMBROS_ADICIONADO)))
                time.sleep(random.randrange(TelegramExtractJSON["Sistema Anti-Spam"]["aguardar(segundos) a cada adicao de membro"][0], TelegramExtractJSON["Sistema Anti-Spam"]["aguardar(segundos) a cada adicao de membro"][1]))
            except errors.FloodWaitError as erro:
                numbers = ""
                for caracter in erro.args[0]:
                    if caracter.isdigit():
                        numbers += caracter
                print(f'{Fore.RED}[CONTA DO TELEGRAM {account.replace(".session","")}] FloodWaitError Detectado, aguardando {numbers} segundos para depois continuar')
                time.sleep(int(numbers))
            except errors.PeerFloodError as erro:
                numbers = random.randrange(TelegramExtractJSON["Sistema Anti-Spam"]["aguardar(segundos) por peerflooderror"][0],TelegramExtractJSON["Sistema Anti-Spam"]["aguardar(segundos) por peerflooderror"][1])
                print(f'{Fore.RED}[CONTA DO TELEGRAM {account.replace(".session","")}] PeerFloodError Detectado(Erro de Inundação do Telegram), aguardando {numbers} segundos para depois continuar')
                time.sleep(numbers)
            except errors.UserPrivacyRestrictedError as erro:
                #$ COODDING: Remover Usuario da Lista de Membros Filtrados
                try:
                    TelegramExtractJSON["Membros Filtrados"].remove(usuario)
                    TelegramExtractJSON = TelegramExtract.configuracoes(newConfiguracoes=TelegramExtractJSON)
                except Exception as erro:
                    print(erro)
                    
                print(f'{Fore.RED}[CONTA DO TELEGRAM {account.replace(".session","")}] UserPrivacyRestrictedError Detectado, As configurações de privacidade do usuário({usuario["username"]}) não permitem você adicionar ele(a) a grupos')
                time.sleep(random.randrange(TelegramExtractJSON["Sistema Anti-Spam"]["aguardar(segundos) a cada adicao de membro"][0], TelegramExtractJSON["Sistema Anti-Spam"]["aguardar(segundos) a cada adicao de membro"][1]))
            except Exception as erro:
                try:
                    TelegramExtractJSON["Membros Filtrados"].remove(usuario)
                    TelegramExtractJSON = TelegramExtract.configuracoes(newConfiguracoes=TelegramExtractJSON)
                except Exception as erro:
                    print(erro)
                print(f'{Fore.RED}[CONTA DO TELEGRAM {account.replace(".session","")}] {erro.args[0]}')
                time.sleep(random.randrange(TelegramExtractJSON["Sistema Anti-Spam"]["aguardar(segundos) a cada adicao de membro"][0], TelegramExtractJSON["Sistema Anti-Spam"]["aguardar(segundos) a cada adicao de membro"][1]))
           
            

    def exit():
        """Função responsavel por fechar programa"""
        input()
        sys.exit()


"""
CODDING: Variaveis de Mensagens do Sistema
"""
MENSAGEM_NENHUM_GRUPO_ESCOLHIDO = f'{Fore.RED}[CONTAS DO TELEGRAM]{Fore.RESET} Nenhuma conta do telegram encontrada, impossivel iniciar...'
MENSAGEM_DE_ESCOLHER_GRUPO_PARA_EXTRAIR_MEMBROS = f'{Fore.GREEN}[CONTA DO TELEGRAM </PHONE>]{Fore.RESET} escolha um grupo pra extrair membros'
MENSAGEM_DE_ESCOLHA_DE_GRUPO_INVALIDA = f'{Fore.RED}[GRUPO INVÁLIDO]{Fore.RESET} Escolha inválida, não foi possivel selecionar nenhum grupo, tente novamente...'



TelegramExtractJSON = TelegramExtract.configuracoes()
if len(TelegramExtractJSON["Telegram Accounts"]) > 0:
    try:
        while True:
            for index,account in enumerate(TelegramExtractJSON["Telegram Accounts"]):
                
                phone = TelegramExtractJSON["Telegram Accounts"][account]["phone"]
                api_id = TelegramExtractJSON["Telegram Accounts"][account]["api_id"]
                api_hash = TelegramExtractJSON["Telegram Accounts"][account]["api_hash"]
                
                status,client = TelegramExtract.conectar_em_conta_do_telegram(phone,api_id, api_hash)
                if status:
                    if len(TelegramExtractJSON["Membros Filtrados"]) == 0:
                        while True:
                            """
                            CODDING: Extrair Membros de Grupo do Telegram
                            """
                            try:
                                Groups = []
                                contagem_dos_grupos = 0

                                print(MENSAGEM_DE_ESCOLHER_GRUPO_PARA_EXTRAIR_MEMBROS.replace("</PHONE>", phone))
                                for dialog in client.get_dialogs():
                                    if dialog.is_group and dialog.is_channel:
                                        contagem_dos_grupos +=1
                                        Groups.append(dialog)
                                        if dialog.entity.admin_rights != None:
                                            print('   {}. {} {}{}({} participantes, {}admin{})'.format(contagem_dos_grupos, dialog.name, dialog.id,Fore.LIGHTBLACK_EX ,dialog.entity.participants_count,Fore.GREEN,Fore.LIGHTBLACK_EX))
                                        else:
                                            print('   {}. {} {}{}({} participantes){}'.format(contagem_dos_grupos, dialog.name, dialog.id, Fore.LIGHTBLACK_EX ,dialog.entity.participants_count,Fore.RESET))
                                    
                                        
                                index = int(input('   digite sua escolha: '))
                                grupo = Groups[index-1]
                                break
                            except Exception as erro:
                                print(MENSAGEM_DE_ESCOLHA_DE_GRUPO_INVALIDA)
                                





                        """
                        CODDING: Extraindo membros
                        """
                        print('\n\n   Grupo escolhido: {}{}'.format(Fore.GREEN, grupo.name))
                        alfabeto = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
                        MembrosFiltrados = []
                        NumerosFiltrados = []

                        for key in alfabeto:
                            offset = 0
                            limit = 100
                            while True:
                                participantes = client(functions.channels.GetParticipantsRequest(
                                    grupo,
                                    types.ChannelParticipantsSearch(key),
                                    offset,
                                    limit,
                                    hash=0))
                                

                                if not participantes.users:
                                    print('      Usuarios filtrados por Search({}): {}'.format(key,offset))
                                    break
                                
                                for user in participantes.users:
                                    try:
                                        if re.findall(r"\b[a-zA-Z]", user.first_name)[0].lower() == key:
                                            if user.username != None:
                                                MembrosFiltrados.append({'username':user.username,'id':user.id,'access_hash':user.access_hash})
                                                if user.phone != None:
                                                    NumerosFiltrados.append(user.phone)
                                    except:
                                        pass
                                    

                                offset += len(participantes.users)
                            

                        """
                        CODDING: criando arquivos com numeros filtrados
                        """
                        print('         {}{} membros filtrados do grupo'.format(Fore.GREEN,len(MembrosFiltrados),grupo.name))
                        
                        TelegramExtractJSON["Membros Filtrados"] = MembrosFiltrados
                        TelegramExtractJSON = TelegramExtract.configuracoes(newConfiguracoes=TelegramExtractJSON)
                        
                    else:
                        pass
                    
                    """
                    CODDING: Adicionar Membros de Grupo do Telegram
                    """
                    
                    Groups = []
                    GroupsADM = []
                    contagem_dos_grupos = 0
                    
                    TelegramExtractJSON = TelegramExtract.configuracoes()
                    
                    print(f'{Fore.GREEN}[MEMBROS]{Fore.RESET} {len(TelegramExtractJSON["Membros Filtrados"])} Membros filtrados prontos para serem adicionados ao seu grupo')
                    
                    while True:
                        try:
                            print('{}[CONTA DO TELEGRAM {}]{} escolha um grupo para adicionar membros'.format(Fore.GREEN,TelegramExtractJSON["Telegram Accounts"][account]['phone'], Fore.RESET))
                            for dialog in client.get_dialogs():
                                Groups.append(dialog)
                                contagem_dos_grupos +=1
                                if dialog.is_group and dialog.is_channel:
                                    if dialog.entity.admin_rights != None:
                                        print('   {}. {} {}{}({} participantes, {}admin{})'.format(contagem_dos_grupos, dialog.name, dialog.id,Fore.LIGHTBLACK_EX ,dialog.entity.participants_count,Fore.GREEN,Fore.LIGHTBLACK_EX))
                                    else:
                                        print('   {}. {} {}{}({} participantes){}'.format(contagem_dos_grupos, dialog.name, dialog.id, Fore.LIGHTBLACK_EX ,dialog.entity.participants_count,Fore.RESET))
                                        
                            
                            
                            index = int(input('   digite sua escolha: '))
                            grupo = Groups[index-1]
                            break
                        except Exception as erro:
                            print(MENSAGEM_DE_ESCOLHA_DE_GRUPO_INVALIDA)
                    
                    TelegramExtractJSON["grupo.id"] = str(grupo.id)
                    TelegramExtractJSON = TelegramExtract.configuracoes(newConfiguracoes=TelegramExtractJSON)
                    print(f'   grupo escolhido: {Fore.GREEN}{grupo.name}')
                    
                    TelegramExtract.adicionar_membros(client, grupo,account)
                                
                    
                         
                else:
                    pass
            
            print(f'{Fore.GREEN}[SISTEMA ANTI-SPAM]{Fore.RESET} Limite de adicição de Membros Atingido, '+'aguardando {} segundos para adicionar {} membros por conta novamente'.format(TelegramExtractJSON["Sistema Anti-Spam"]["periodo de horas(em segundos) que contas ira hibernar após atingir limites de adicao de membros"],TelegramExtractJSON["Sistema Anti-Spam"]["limide de adicao de membros por conta"]))
            time.sleep(TelegramExtractJSON["Sistema Anti-Spam"]["periodo de horas(em segundos) que contas ira hibernar após atingir limites de adicao de membros"])
    except Exception as erro:
        print(f'd{Fore.RED}[*] Error: {erro}')
        TelegramExtract.exit()
else:
    print(MENSAGEM_NENHUM_GRUPO_ESCOLHIDO)
    TelegramExtract.exit()

    
