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
"""
TOTAL_DE_MEMBROS_ADICIONADO = 0


"""
CODDING: TelegramExtract <Class>
• Conectar no Telegram com Telethon
• Extrair/Adicionar Membros em Grupos do Telegram
"""
class TelegramExtract:
    def TelegramExtractJSON(salvar=None):
        """
        Função responsavel por retornar/atualizar configurações e contas do Telegram do arquivo TelegramExtract.json
        """
        if salvar:
            try:
                with open('TelegramExtract.json', 'w') as f:
                    # Salva os dados de volta no arquivo
                    json.dump(salvar, f)
                textExtract = open("TelegramExtract.json","r")
                textExtract = textExtract.read()
                return json.loads(textExtract)
            except Exception as erro:
                return False
        else:
            textExtract = open("TelegramExtract.json","r")
            textExtract = textExtract.read()
            return json.loads(textExtract)
    def telegramConnect(phone,api_id,api_hash):
        """
        Função responsavel por conectar na sua conta no Telegram
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
        TelegramExtractJSON = TelegramExtract.TelegramExtractJSON()
        for usuario in TelegramExtractJSON["Membros Filtrados"][:20]:
            usuario_entity = client.get_input_entity(usuario["username"])
            try:
                client(functions.channels.InviteToChannelRequest(grupo,[usuario_entity]))
                TOTAL_DE_MEMBROS_ADICIONADO += 1
                #$ COODDING: Remover Usuario da Lista de Membros Filtrados
                try:
                    TelegramExtractJSON["Membros Filtrados"].remove(usuario)
                    TelegramExtractJSON = TelegramExtract.TelegramExtractJSON(salvar=TelegramExtractJSON)
                except Exception as erro:
                    print(erro)
                print(f"{Fore.GREEN}{account.replace('.session','')}{Fore.RESET} adicionou",usuario["username"],"no grupo")
                time.sleep(random.randrange(60, 180))
            except errors.FloodWaitError as erro:
                numbers = ""
                for caracter in erro.args[0]:
                    if caracter.isdigit():
                        numbers += caracter
                print(f'{Fore.RED}[CONTA DO TELEGRAM {account.replace(".session","")}] FloodWaitError Detectado, aguardando {numbers} segundos para depois continuar')
                time.sleep(int(numbers))
            except errors.PeerFloodError as erro:
                print(erro)
                numbers = random.randrange(180,1000)
                print(f'{Fore.RED}[CONTA DO TELEGRAM {account.replace(".session","")}] PeerFloodError Detectado(Erro de Inundação do Telegram), aguardando {numbers} segundos para depois continuar')
                time.sleep(numbers)
            except errors.UserPrivacyRestrictedError as erro:
                #$ COODDING: Remover Usuario da Lista de Membros Filtrados
                try:
                    TelegramExtractJSON["Membros Filtrados"].remove(usuario)
                    TelegramExtractJSON = TelegramExtract.TelegramExtractJSON(salvar=TelegramExtractJSON)
                except Exception as erro:
                    print(erro)
                    
                print(f'{Fore.RED}[CONTA DO TELEGRAM {account.replace(".session","")}] UserPrivacyRestrictedError Detectado, As configurações de privacidade do usuário({usuario["username"]}) não permitem você adicionar ele(a) a grupos')
                time.sleep(random.randrange(60, 180))
            except Exception as erro:
                try:
                    TelegramExtractJSON["Membros Filtrados"].remove(usuario)
                    TelegramExtractJSON = TelegramExtract.TelegramExtractJSON(salvar=TelegramExtractJSON)
                except Exception as erro:
                    print(erro)
                print(f'{Fore.RED}[CONTA DO TELEGRAM {account.replace(".session","")}] {erro.args[0]}')
                time.sleep(random.randrange(60, 180))
           
            

    def exit():
        """Função responsavel por fechar programa"""
        input()
        sys.exit()


"""
CODDING: Variaveis de Mensagens do Sistema
"""
MENSAGEM_DE_ESCOLHER_GRUPO_PARA_EXTRAIR_MEMBROS = f'{Fore.GREEN}[CONTA DO TELEGRAM </PHONE>]{Fore.RESET} escolha um grupo pra extrair membros'




TelegramExtractJSON = TelegramExtract.TelegramExtractJSON() #$ Arquivo: TelegramExtract.json
if len(TelegramExtractJSON["Telegram Accounts"]) > 0: 
    try:
        for index,account in enumerate(TelegramExtractJSON["Telegram Accounts"]):
            
            phone = TelegramExtractJSON["Telegram Accounts"][account]["phone"]
            api_id = TelegramExtractJSON["Telegram Accounts"][account]["api_id"]
            api_hash = TelegramExtractJSON["Telegram Accounts"][account]["api_hash"]
            
            status,client = TelegramExtract.telegramConnect(phone,api_id, api_hash)
            if status:
                if len(TelegramExtractJSON["Membros Filtrados"]) == 0:
                    """
                    CODDING: Extrair Membros de Grupo do Telegram
                    """
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
                    TelegramExtract.TelegramExtractJSON(salvar=TelegramExtractJSON)
                else:
                    pass
                
                """
                CODDING: Adicionar Membros de Grupo do Telegram
                """
                
                Groups = []
                GroupsADM = []
                contagem_dos_grupos = 0
                
                TelegramExtractJSON = TelegramExtract.TelegramExtractJSON()
                
                print(f'{Fore.GREEN}[MEMBROS]{Fore.RESET} {len(TelegramExtractJSON["Membros Filtrados"])} Membros filtrados prontos para serem adicionados ao seu grupo')
                print('{}[CONTA DO TELEGRAM {}]{} escolha um grupo para adicionar membros'.format(Fore.GREEN,TelegramExtractJSON["Telegram Accounts"][account]['phone'], Fore.RESET))
                for dialog in client.get_dialogs():
                    Groups.append(dialog)
                    contagem_dos_grupos +=1
                    if dialog.is_group and dialog.is_channel:
                        if dialog.entity.admin_rights != None:
                            print('   {}. {} {}{}({} participantes, {}admin{})'.format(contagem_dos_grupos, dialog.name, dialog.id,Fore.LIGHTBLACK_EX ,dialog.entity.participants_count,Fore.GREEN,Fore.LIGHTBLACK_EX))
                        else:
                            print('   {}. {} {}{}({} participantes){}'.format(contagem_dos_grupos, dialog.name, dialog.id, Fore.LIGHTBLACK_EX ,dialog.entity.participants_count,Fore.RESET))
                            
                
                if len(Groups) > 0: 
                    index = int(input('   digite sua escolha: '))
                    grupo = Groups[index-1]
                    
                    TelegramExtractJSON["grupo.id"] = str(grupo.id)
                    TelegramExtractJSON = TelegramExtract.TelegramExtractJSON(salvar=TelegramExtractJSON)
                    print(f'   grupo escolhido: {Fore.GREEN}{grupo.name}')
                    
                    TelegramExtract.adicionar_membros(client, grupo,account)
                                
                else:
                    print(f"   {Fore.RED}[PERMISSÃO DE ADMINISTRADOR]{Fore.RESET} Nenhum grupo com permissão de administrador encontrado")
                
                
            
                
                
                
                
                
                
            else:
                pass
    except Exception as erro:
        print(f'd{Fore.RED}[*] Error: {erro}')
        TelegramExtract.exit()
else:
    print(f'{Fore.RED}[CONTAS DO TELEGRAM]{Fore.RED} Nenhuma conta do telegram encontrada')
    TelegramExtract.exit()

    
