import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.reactions = True
intents.message_content = True
intents.members = True  # Это нужно для работы с членами сервера

bot = commands.Bot(command_prefix='!', intents=intents)


TOKEN = ('Сюда токен')

# ID канала и сообщения, на которое будут реагировать пользователи
CHANNEL_ID = Укажите
MESSAGE_ID = Укажите

# Словарь с эмодзи и соответствующей ему ролью
ROLE_ASSIGNMENTS = {
    '👍': сюда,  # замените на ID вашей роли
}

# Укажите текущую роль, которую нужно удалить
CURRENT_ROLE_ID = вставь

# Роль, которую нужно выдать при входе на сервер
NEW_MEMBER_ROLE_ID = вставь  # замените на ID вашей роли

@bot.event
async def on_ready():
    print(f'Бот {bot.user} запущен!')
    await bot.change_presence(activity=discord.Game(name="Dev 2everyone"))

    # Добавление реакций на сообщение
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        try:
            message = await channel.fetch_message(MESSAGE_ID)
            for emoji in ROLE_ASSIGNMENTS.keys():
                await message.add_reaction(emoji)
        except discord.NotFound:
            print(f'Сообщение с ID {MESSAGE_ID} не найдено в канале {CHANNEL_ID}')
        except discord.Forbidden:
            print('Нет прав на добавление реакций в этот канал')

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == MESSAGE_ID:
        guild = bot.get_guild(payload.guild_id)
        role_id = ROLE_ASSIGNMENTS.get(str(payload.emoji))
        if role_id:
            role_to_add = guild.get_role(role_id)
            role_to_remove = guild.get_role(CURRENT_ROLE_ID)
            member = guild.get_member(payload.user_id)
            if role_to_add and role_to_remove and member:
                await member.remove_roles(role_to_remove)
                await member.add_roles(role_to_add)
                print(f"Removed {role_to_remove.name} and added {role_to_add.name} to {member.display_name}")

@bot.event
async def on_member_join(member):
    guild = member.guild
    role = guild.get_role(NEW_MEMBER_ROLE_ID)
    if role:
        await member.add_roles(role)
        print(f'Added {role.name} to {member.display_name} on join')

@bot.event
async def on_ready():
    try:
        print(f'Бот {bot.user} запущен!')
        await bot.change_presence(activity=discord.Game(name="Dev 2everyone"))
        await send_log(f'Бот {bot.user} запущен!')
    except Exception as e:
        print(f"Ошибка в on_ready: {e}")

bot.run(TOKEN)
