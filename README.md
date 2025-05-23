# Bot Discord

Este é um bot Discord desenvolvido em Python para um servidor pessoal.

## Configuração
Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:
```
BOT_TOKEN=seu_token_aqui
```

4. Configure as pastas necessárias:
- Crie uma pasta `imagens_aleat` para imagens aleatórias
- Crie uma pasta `img_segredo` para imagens secretas
- Crie uma pasta `stop_img` para imagens de stop
- Crie uma pasta `imgs_davibrito` para imagens específicas

## Executando o Bot

Para iniciar o bot, execute:
```bash
python bot.py
```

## Estrutura do Projeto

- `bot.py`: Arquivo principal do bot
- `texts/`: Diretório com arquivos de texto
- `imagens_aleat/`: Diretório com imagens aleatórias (não versionado)
- `img_segredo/`: Diretório com imagens secretas (não versionado)
- `stop_img/`: Diretório com imagens de stop (não versionado)
- `imgs_davibrito/`: Diretório com imagens específicas (não versionado)

## Funcionamento

- Devido ser um bot para uso pessoal optei por usar recursos gratuitos, então o função random_interaction une a API gratuita zenquotes retornando citações famosas em inglês e por uma questão de preferência as citações são traduzidas pela biblioteca *googletrans*
- O bot também conta com a funcionalidade musical permitindo possibilitando as ações básicas de um music player sendo pesquisar uma música, pausar/despausar, pular e encerrar além de funções como criar uma playlist, a biblioteca usada foi *yt_dlp* pela sua conexão com Youtube onde um grande leque de músicas

## Segurança

- O token do bot está protegido no arquivo `.env`
- Diretórios com imagens sensíveis não são versionados
- Arquivos de cache e temporários são ignorados pelo git 