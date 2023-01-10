## Extrair/Adicionar Membros no Telegram com Python
Este projeto visa automatiza o processo de Extrair/Adicionar membros em grupos do Telegram de forma 100% automática. Usando o módulo [Telethon](https://github.com/LonamiWebs/Telethon) do [Python](https://www.python.org/), é possível realizar essa tarefa de forma totalmente automatizada.


FUNCIONALIDADES:
<br>• Conecta em várias contas do Telegram(Tratando errors de FloodError, FloodWaitError, PhoneNumberBannedError)
<br>• Extrai Membros de grupo do Telegra por completo e em ordem alfabetica de A...Z(consegue extrair de 70% a 98% dos membros)
<br>• Adiciona Membros de forma 100% automática no seu grupo do Telegram(Tratando errors de FloodError, FloodWaitError, PeerFloodError, UserPrivacyRestrictedError...)
<br>• Sistema Anti-Spam, Bot aguarda de 60/180s para adicionar cada membro, e adiciona apenas 20 membros por vez e troca de conta, depois de adicionar 20 membros com cada conta, ele aguarda algumas horas e repete todo o processo...(OBS: Você pode moficiar as configurações do Sistema Anti-Spam)



### 1. Instalando Dependência(Telethon & Colorama)
Para usar este projeto, é necessário ter o [Python 3.6](https://www.python.org/downloads/release/python-360/) ou superior instalado em sua máquina. Além disso, você precisará instalar as seguintes dependências:
```bash
pip install telethon
pip install colorama
```

### 2. Clonando Repositório
```bash
git clone https://github.com/davideduardotech/TelegramExtract.git
cd pyTelegram
```

### 3. Configurando
Antes de usar este projeto, você precisará obter as chaves de API's das suas contas do Telegram(<code>API_ID</code>,<code>API_HASH</code>) Para fazer isso, siga as instruções em https://core.telegram.org/api/obtaining_api_id.

Em seguida, Adicione suas contas editando o arquivo TelegramExtract.json, adicionando suas contas dentro da chave "Telegram Account" com as suas informações de <code>PHONE.session</code>, <code>PHONE</code>, <code>API_ID</code> e <code>API_HASH</code>

EXEMPLO:
```bash
{
  "Telegram Accounts":{
    "+5581993762632.session:{
      "phone":+5581993762632,
      "api_id":767623,
      "api_hash": "d93449f3e5b4bc1fb096a29c2fe7cb71b"
    },
    ...
  }
}
```

nas configurações do <code>"Sitema Anti-Spam"</code> você pode alterar e personalizar o tempo estre os requests como você quiser quiser para evitar bloqueios:
<br>• <code>"aguardar(segundos) a cada adicao de membro"</code>
<br>• <code>"aguardar(segundos) por peerflooderror"</code> 
<br>• <code>"limide de adicao de membros por conta"</code> 
<br>• <code>"periodo de horas(em segundos) que contas ira hibernar após atingir limites de adicao de membros"</code> 

EXEMPLO PADRÃO DO ANTI-SPAM:
```bash
{
  ...
  "Sistema Anti-Spam": {
        "aguardar(segundos) a cada adicao de membro": [60, 180], 
        "aguardar(segundos) por peerflooderror": [100, 1000], 
        "limide de adicao de membros por conta": 20, 
        "periodo de horas(em segundos) que contas ira hibernar após atingir limites de adicao de membros": 28800
   },
   ...
}
```

### 4. Pronto, agora basta utilizar
Para usar este projeto, basta executar o script TelegramExtract.py, Por exemplo:
```bash
python TelegramExtract.py
```

### 👨‍💻 Contribuição
Se você deseja contribuir para este projeto, basta criar um pull request com suas alterações. Todas as contribuições serão analisadas e, se aceitas, serão mescladas com o branch principal.




