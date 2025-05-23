import discord
import random
import os
import requests
from discord import app_commands
from discord.ext import commands
from discord import Game,Activity,ActivityType
from googletrans import Translator
import yt_dlp
import asyncio
from collections import deque 
from discord import File,Embed
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém o token do arquivo .env
TOKEN = os.getenv('BOT_TOKEN')
if not TOKEN:
    raise ValueError("Token não encontrado no arquivo .env")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!',intents=intents)

SONG_QUEUES = {}
ultimo_escolhido = None

async def search_ytdl_async(query, ydl_opts):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: _extract(query, ydl_opts))


def _extract(query,ydl_opts):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(query, download=False)

def get_random_frase():
    url = 'https://zenquotes.io/api/random'
    response = requests.get(url)
    data = response.json()
    frase_original = data[0]['q'] + " — " + data[0]['a']

    translator = Translator()
    traducao = translator.translate(frase_original, dest='pt') 

    return traducao.text

def get_random_frase_dv():
    frases = [
                "Não existem sonhos impossíveis para aqueles que realmente acreditam que o poder realizador reside no interior de cada ser humano.",
                "Amor a gente espera, como o pescador espera o seu peixe ou o devoto espera o seu milagre: em silêncio, sem se perder a paciência com a demora.",
                "Calma, calabreso",
                "Não pergunte o que seu país pode fazer por você, pergunte o que você pode fazer pelo seu país.",
                "A educação é a arma mais poderosa que você pode usar para mudar o mundo.",
                "O homem é a medida de todas as coisas.",
                "O homem é condenado a ser livre.",
                "A vida é essencialmente apropriação, agressão, superação do que é estranho e mais fraco.",
                "O homem, em seu orgulho, criou Deus à sua imagem e semelhança.",
                "A visão do homem agora cansa - o que é hoje o niilismo, se não isto?... Estamos cansados do homem...",
                "O maior erro que um homem pode cometer é sacrificar a sua saúde a qualquer outra vantagem",
                "A glória é tanto mais tardia quanto mais duradoura há de ser, porque todo fruto delicioso amadurece lentamente",
                "A vida é um processo constante de morte",
                "O talento atinge um alvo que ninguém mais pode atingir. A genialidade atinge um alvo que ninguém mais pode ver"
              
              ]
    
    return random.choice(frases)

def carregar_imagens(diretorio:str):
    extensoes_validas = {'.jpeg','.jpg','.png','.gif','.webp', '.mp4', '.mov', '.webm'}
    return [
        os.path.join(diretorio, arquivo)
        for arquivo in os.listdir(diretorio)
        if os.path.splitext(arquivo)[1].lower() in extensoes_validas
    ]

imagens_aleat = carregar_imagens('imagens_aleat')
imagens_dvbrito = carregar_imagens('imgs_davibrito')
imagens_ratinho  = carregar_imagens('img_segredo') 


@bot.event
async def on_ready():
    await bot.change_presence(
        activity=Activity(type=ActivityType.watching, name="🎲 tudo e todos, palmeia dog"),
        status=discord.Status.online
     
    )
    print(f'Bot{bot.user} está operando!')

    try:
        synced = await bot.tree.sync()
        print(f"Comandos sincronizados: {len(synced)}")
    except Exception as e:
        print(f"Erro ao sincronizar comandos: {e}")


@bot.tree.command(name='imgrandom', description="Envia mensagens e frases aleatórias")
async def random_interaction(interaction: discord.Interaction):
    image_path = random.choice(imagens_aleat)
    frase = get_random_frase()
    
    with open(image_path, 'rb') as file:
        discord_file = discord.File(file, filename=os.path.basename(image_path))

    
    embed = Embed(
        title="✨ Pensamento",
        description=f"**\"{frase}\"**",
        color=discord.Color.purple()
    )
    embed.set_footer(text="🌟Jotinha trabalhou muito nessa.")
    
    
    embed.set_image(url=f"attachment://{os.path.basename(image_path)}")

    
    await interaction.response.send_message(embed=embed, file=discord_file)


@bot.tree.command(name='davibrito', description="Davi Brito")
async def random_interaction(interaction: discord.Interaction):
    image_path = random.choice(imagens_dvbrito)
    frase = get_random_frase_dv()
    
    with open(image_path, 'rb') as file:
        discord_file = discord.File(file, filename=os.path.basename(image_path))


    embed = Embed(
        title="📜 Citação de Davi Brito",
        description=f"**\"{frase}\"**",
        color=discord.Color.gold()  
    )
    embed.set_footer(text="🌟 Inspirado por Calabreso")
    
    
    embed.set_image(url=f"attachment://{os.path.basename(image_path)}")

    
    await interaction.response.send_message(embed=embed, file=discord_file)

@bot.tree.command(name='segredo', description="Segredinho")
async def random_interaction(interaction: discord.Interaction):
    image_path = random.choice(imagens_ratinho)


    with open(image_path, 'rb') as file:
        discord_file = discord.File(file, filename=os.path.basename(image_path))


    embed = Embed(
        title="🐭 Tenho que lhe trazer isso",
        color=discord.Color.dark_blue()  
    )
    embed.set_footer(text="🌟 Rapaz..")
    
    
    embed.set_image(url=f"attachment://{os.path.basename(image_path)}")

    
    await interaction.response.send_message(embed=embed, file=discord_file)

ultimo_escolhido = None
@bot.tree.command(name='resposta', description='Mostra umas verdades aí')
async def ascii(interaction: discord.Interaction):
    global ultimo_escolhido
    pasta = 'texts'

    try:
        arquivos = [f for f in os.listdir(pasta) if f.endswith('.txt')]

        if not arquivos:
            await interaction.response.send_message('❌ Nenhuma arte ASCII encontrada!', ephemeral=True)
            return

        random.shuffle(arquivos)
        arquivo_escolhido = random.choice(arquivos)
        
        # Evita repetir o mesmo arquivo duas vezes seguidas
        while arquivo_escolhido == ultimo_escolhido:
            arquivo_escolhido = random.choice(arquivos)
        ultimo_escolhido = arquivo_escolhido

        cam_arq = os.path.join(pasta, arquivo_escolhido)

        with open(cam_arq, 'r', encoding='utf-8') as file:
            ascii_art = file.read()

        # Criar um embed para deixar a mensagem bonita
        embed = discord.Embed(
            title="💬 Verdades Reveladas",
            description=f"Veja o que descobrimos sobre você, **{interaction.user.name}**:",
            color=discord.Color.blurple()
        )
        
        # Limitar o tamanho da arte ASCII para caber no embed
        if len(ascii_art) > 1500:
            ascii_art = ascii_art[:1500] + "\n... [ASCII muito longo, cortado]"

        embed.add_field(
            name="🎨 ASCII Art",
            value=f"```\n{ascii_art}\n```",
            inline=False
        )
        
        embed.set_footer(text="Incrível, não é? 🌟")
        
        await interaction.response.send_message(embed=embed)

    except Exception as e:
        await interaction.response.send_message(f"❌ Erro ao carregar ASCII: {e}", ephemeral=True)


@bot.tree.command(name="pause", description="Pausa a música que tá tocando.")
async def pause(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client

    
    if voice_client is None:
        return await interaction.response.send_message("Não estou em nenhum canal de voz!.")

    
    if not voice_client.is_playing():
        return await interaction.response.send_message("Não tô tocando nada como que vou pausar algo?.")
    
    
    voice_client.pause()
    await interaction.response.send_message("Música parada!")

@bot.tree.command(name="resume", description="Retoma a música que foi pausada.")
async def resume(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client

    
    if voice_client is None:
        return await interaction.response.send_message("Não estou em nenhum canal de voz!.")

    if not voice_client.is_paused():
        return await interaction.response.send_message("Tem nenhuma música pausada não, dog")
    
  
    voice_client.resume()
    await interaction.response.send_message("Tá pausado, dog.")



@bot.tree.command(name="skip", description="Pula o som atual")
async def skip(interaction: discord.Interaction):
    if interaction.guild.voice_client and (interaction.guild.voice_client.is_playing() or interaction.guild.voice_client.is_paused()):
        interaction.guild.voice_client.stop()
        await interaction.response.send_message("Pulei o som que tava tocando.")
    else:
        await interaction.response.send_message("Não tô tocando nada como que vou pular algo?.")        

@bot.tree.command(name="stop", description="Para de tocar e limpa a playlist.")
async def stop(interaction: discord.Interaction):
    await interaction.response.defer()

    voice_client = interaction.guild.voice_client

    if not voice_client or not voice_client.is_connected():
        await interaction.response.send_message("Não estou em nenhum canal de voz!")
        return  
    
    guild_id_str = str(interaction.guild_id)
    if guild_id_str in SONG_QUEUES:
        SONG_QUEUES[guild_id_str].clear()

    if voice_client.is_playing() or voice_client.is_paused():
        voice_client.stop()

    # Caminho da imagem local
    img_path = "stop_img/stop_img.jpeg"

    # Criar embed
    embed = discord.Embed(
        title="🎶 Música finalizada!",
        description="Deitei sem sono, dog👋",
        color=discord.Color.red()
    )

    # Abrir a imagem e enviá-la como anexo
    file = discord.File(img_path, filename="stop_img.jpeg")
    embed.set_image(url=f"attachment://stop_img.jpeg")

    await interaction.followup.send(embed=embed, file=file)

    # Desconectar depois de enviar a mensagem
    asyncio.create_task(voice_client.disconnect())


@bot.tree.command(name="play",description="Toca umas músicas ai ou adiciona na fila")
@app_commands.describe(song_query="Procurando")
async def play(interaction:discord.Interaction, song_query:str):
    await interaction.response.defer()

    voice_channel = interaction.user.voice.channel
    if voice_channel is None:
        await interaction.followup.send("Entra num canal de voz aí, meu amigão.")
        return
    
    voice_client = interaction.guild.voice_client

    if voice_client is None:
        voice_client = await voice_channel.connect()

    elif voice_channel != voice_client.channel:
        await voice_client.move_to(voice_channel)    

    ydl_options = {
        'format':'bestaudio[abr<=96]/bestaudio',
        'noplaylist': True,
        'youtube_include_dash_manifest': False,
        'youtube_include_hls_manifest': False
    }

    query = 'ytsearch1:' + song_query
    results = await search_ytdl_async(query, ydl_options)
    tracks = results.get("entries", [])

    if tracks is None:
        await interaction.followup.send("Achei nada, meu querido.")
        return

    first_track = tracks[0]
    audio_url = first_track["url"]
    title = first_track.get("title", "Untitled")

    guild_id = str(interaction.guild_id)
    if SONG_QUEUES.get(guild_id) is None:
        SONG_QUEUES[guild_id] = deque()

    SONG_QUEUES[guild_id].append((audio_url, title))

    if voice_client.is_playing() or voice_client.is_paused():
        await interaction.followup.send(f"Coloquei na fila: **{title}**")
    else:
        await interaction.followup.send(f"Now playing: **{title}**",ephemeral=True)
        await play_next_song(voice_client, guild_id, interaction.channel)

async def play_next_song(voice_client, guild_id, channel):
    if SONG_QUEUES[guild_id]:
        audio_url, title = SONG_QUEUES[guild_id].popleft()

        ffmpeg_options = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            "options": "-vn -c:a libopus -b:a 96k",
            # Remove executable if FFmpeg is in PATH
        }

        source = discord.FFmpegOpusAudio(audio_url, **ffmpeg_options, executable="bin\\ffmpeg\\ffmpeg.exe")

        def after_play(error):
            if error:
                print(f"Deu um erro pra tocar {title}: {error}")
            asyncio.run_coroutine_threadsafe(play_next_song(voice_client, guild_id, channel), bot.loop)

        voice_client.play(source, after=after_play)
        asyncio.create_task(channel.send(f"Now playing: **{title}**"))
    else:
        await voice_client.disconnect()
        SONG_QUEUES[guild_id] = deque()  




bot.run(TOKEN)    