import discord
from datetime import datetime
from config import CHANNEL_ID, MENTION_ROLE
from database import get_today_items, clear_today, add_subscriber, get_subscribers


class SubscribeButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=86400)

    @discord.ui.button(label="✅ S'inscrire aux infos quotidiennes", style=discord.ButtonStyle.green)
    async def subscribe(self, interaction: discord.Interaction, button: discord.ui.Button):
        subscribers = await get_subscribers()
        if interaction.user.id in subscribers:
            await interaction.response.send_message("Tu es déjà inscrit ! 📬", ephemeral=True)
            return
        await add_subscriber(interaction.user.id)
        await interaction.response.send_message("Tu es inscrit ! Tu recevras les infos chaque jour en MP 📬", ephemeral=True)
        button.disabled = True
        await interaction.message.edit(view=self)


async def send_daily_report(bot, channel_override=None, show_subscribe=False):
    items = await get_today_items()
    channel = channel_override or await bot.fetch_channel(CHANNEL_ID)
    if not items:
        await channel.send(f"{MENTION_ROLE} 📭 Rien à signaler pour aujourd'hui !")
        if show_subscribe:
            subscribers = await get_subscribers()
            if channel_override and hasattr(channel_override, 'recipient'):
                user_id = channel_override.recipient.id
                if user_id not in subscribers:
                    await channel.send("📬 Veux-tu recevoir ces infos automatiquement chaque jour ?", view=SubscribeButton())
            else:
                await channel.send("📬 Veux-tu recevoir ces infos automatiquement chaque jour ?", view=SubscribeButton())

    promo_embeds = []
    game_embeds = []
    code_embeds = []

    for item in items:
        data = {
            'title': item[1],
            'type': item[2],
            'code': item[3],
            'url': item[4],
            'platform': item[5] if len(item) > 5 else 'Inconnu',
            'source': item[6]
        }

        if item[2] == 'promo':
            promo_embeds.append(data)
        elif item[2] == 'game':
            game_embeds.append(data)
        elif item[2] == 'code':
            code_embeds.append(data)

    date_str = datetime.now().strftime("%d/%m/%Y")

    if promo_embeds:
        embed = discord.Embed(title=f"🏷️ Codes Promo du {date_str}", color=0xFF6B35)
        for p in promo_embeds:
            value = f"Code: {p['code']}\nSource: {p['source']}\n[pour en savoir plus]({p['url']})"
            embed.add_field(name=p['title'][:256], value=value[:1024], inline=False)
        await channel.send(content=MENTION_ROLE, embed=embed)

    if game_embeds:
        embed = discord.Embed(title=f"🎮 Jeux Gratuits du {date_str}", color=0x00B4D8)
        for g in game_embeds:
            value = f"Plateforme: {g['platform']}\nSource: {g['source']}\n[Pour en savoir plus]({g['url']})"
            embed.add_field(name=g['title'][:256], value=value[:1024], inline=False)
        await channel.send(embed=embed)

    if code_embeds:
        embed = discord.Embed(title=f"🔑 Codes d'échange du {date_str}", color=0x9B5DE5)
        for c in code_embeds:
            value = f"Récompense: {c['reward']}\nSource: {c['source']}\n[Pour en savoir plus]({c['url']})"
            embed.add_field(name=c['title'][:256], value=value[:1024], inline=False)
        await channel.send(embed=embed)

    if show_subscribe:
            subscribers = await get_subscribers()
            if channel_override and hasattr(channel_override, 'recipient'):
                user_id = channel_override.recipient.id
                if user_id not in subscribers:
                    await channel.send("📬 Veux-tu recevoir ces infos automatiquement chaque jour ?", view=SubscribeButton())
            else:
                await channel.send("📬 Veux-tu recevoir ces infos automatiquement chaque jour ?", view=SubscribeButton())