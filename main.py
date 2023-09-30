import discord
from discord.ext import commands
import json
import random
import time

with open('config.json', 'r') as file:
    config = json.load(file)


token = config['token']
prefix = config['prefix']
delay = config['delay']
phrases_file = config['phrases_file']

bot = commands.Bot(command_prefix=prefix, self_bot=True)

trolllist = []

phrases_open = open(phrases_file, 'r', encoding='utf-8')
phrases = phrases_open.read().splitlines()
phrases = list(filter(None, phrases))
random.shuffle(phrases)

@bot.command()
async def troll(ctx, victim):
    await ctx.message.delete()
    if victim in trolllist:
        await ctx.send("Невозможно добавить " + victim + " в траль-лист: цель уже находится в траль-листе")
    else:
        trolllist.append(victim)
        await ctx.send("Добавил " + victim + " в траль-лист")
        

@bot.command()
async def untroll(ctx, victim):
    await ctx.message.delete()
    if victim in trolllist:
        trolllist.remove(victim)
        await ctx.send("Удалил " + victim + " из траль-листа")
    else:
        await ctx.send("Невозможно удалить " + victim + " из траль-листа: цель отсутствует в траль-листе")
    

@bot.command()
async def setDelay(ctx, delay):
    await ctx.message.delete()
    delay = delay
    await ctx.send("Установлена задержка: " + delay + "ms")

@bot.command()
async def listTrolls(ctx):
    await ctx.message.delete()
    message = "Траль-лист:\n"
    for troll in trolllist:
        message += troll + "\n"
    await ctx.send(message)

@bot.command()
async def clearTrolls(ctx):
    await ctx.message.delete()
    trolllist.clear()
    await ctx.send("Траль-лист успешно очищен")

@bot.command()
async def enable(ctx):
    await ctx.message.delete()
    await ctx.send("Тралинг включен")
    while trolllist:
        phrase = random.choice(trolllist) + " " + random.choice(phrases)
        await ctx.send(phrase)
        time.sleep(int(delay)/1000)
    if not trolllist:
        await ctx.send("Траль-лист пустой, выключаем тралинг")

@bot.command()
async def disable(ctx):
    await ctx.message.delete()
    trolllist.clear()
    await ctx.send("Траль-лист очищен, тралинг выключен")

@bot.command()
async def help(ctx):
    await ctx.message.delete()
    helpMessage = "Помощь:\n"
    helpMessage += "troll <упоминание> - добавляет цель в траль лист\n"
    helpMessage += "untroll <упоминание> - удаляет цель из траль листа\n"
    helpMessage += "setDelay <время> - устанавливает задержку между сообщениями\n"
    helpMessage += "listTrolls - показывает траль-лист\n"
    helpMessage += "clearTrolls - очищает траль-лист\n"
    helpMessage += "enable - запускает тралинг\n"
    helpMessage += "disable - очищает траль-лист и выключает тралинг\n"
    await ctx.send(helpMessage)



bot.run(token)
