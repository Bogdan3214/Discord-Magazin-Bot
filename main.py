import discord
import os

client = discord.Client(intents=discord.Intents.all())

duty_channel_id = 1078415029805776966
presence_channel_id = 1078414693766549625
token = os.environ['TOKEN']
duty_timers = {}

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

async def update_presence(client, duty_timers):
    presence_channel_object = client.get_channel(presence_channel_id)
    has_duty = bool(duty_timers)
    await presence_channel_object.edit(name=f'{"🟩" if has_duty else "🟥"}┊prezenta-magazin')

@client.event
async def on_message(msg):
    if msg.channel.id == duty_channel_id:
        if msg.content == 'start':
            if msg.author.id not in duty_timers:
                await msg.reply('Tura ta la magazin a inceput.')
                await msg.reply('Te rugam sa eviti situatia in care stai mai putin de o ora la magazin iar daca ai nevoie de a pleca, sa revii in maximum 5 minute. In caz contrar, risti posibilitatea de a ti se aplica o sanctiune proportionala cu nivelul fraudarii pontajului.')
                duty_timers[msg.author.id] = discord.utils.utcnow()
                await update_presence(client, duty_timers)
            else:
                await msg.reply('Nu poti incepe o tura deja inceputa. Pentru a incepe tura te rugam ca mai intai sa opresti pontajul folosind comanda stop.')
                await msg.reply('Pentru a incepe tura te rugam ca mai intai sa opresti pontajul folosind comanda stop.')
        elif msg.content == 'stop':
            if msg.author.id in duty_timers:
                duration = discord.utils.utcnow() - duty_timers[msg.author.id]
                hours, remainder = divmod(duration.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                time_string = f'{hours} ore si {minutes} minute'
                await msg.reply(f'Pontaj Oprit.')
                await msg.reply(f'Ai inregistrat {time_string} in aceasta tura.')
                del duty_timers[msg.author.id]
                await update_presence(client, duty_timers)
            else:
                await msg.reply('Nu poti opri o tura neinceputa.')
                await msg.reply('Daca vrei sa incepi o tura, introdu comanda start.')
    elif msg.content == 'status':
        duty_times = {}
        for user_id, start_time in duty_timers.items():
            duration = discord.utils.utcnow() - start_time
            hours, remainder = divmod(duration.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_string = f'{hours} ore si {minutes} minute'
            user = client.get_user(user_id)
            duty_times[user.name] = time_string
        reply_message = '\n'.join([f'{username}: {time}' for username, time in duty_times.items()])
        await msg.channel.reply(f'Timpul petrecut in tura ta actuala:\n{reply_message}')

<<<<<<< HEAD
client.run(token)
=======
client.run(token)
>>>>>>> 6251bebb3757bcd1e5d3f4e3c8445a27f4f03e7b
