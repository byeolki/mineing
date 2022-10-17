import sqlite3, discord, datetime, pytz, func.jsonn as func, cooldowns, random, numpy as np
from korcen import korcen
from discord import Embed, ui
from discord.ext import commands
from itertools import cycle
from discord.commands import Option, option
from discord_slash import SlashContext
from cooldowns import CallableOnCooldown

intents = discord.Intents.all()
client = commands.Bot(intents = discord.Intents.all())
korcen = korcen.korcen()

rule = {"돌":40, "구리":20, "철":15, "금":10, "다이아몬드":9, "에메랄드":6, "가넷":8, }
bbobgi = ["돌", "돌", "돌", "돌", "돌", "돌", "돌", "돌", "구리", "구리", "구리", "구리", "철", "철", "철", "철", "금", "금", "다이아몬드", "다이아몬드", "에메랄드"]

@client.event
async def on_ready():
    status = cycle([f"{len(client.users)}명과 함께하는", f"{len(client.guilds)}개의 서버에 참여하는", f"노래 부르는"])
    print(f"{client.user.name}봇은 준비가 완료 되었습니다.")
    print(f"[!] 참가 중인 서버 : {len(client.guilds)}개의 서버에 참여 중")  
    print(f"[!] 이용자 수 : {len(client.users)}와 함께하는 중")
    guild_list = client.guilds
    for i in guild_list:
        print("서버 ID: {} / 서버 이름: {} / 멤버 수: {}".format(i.id, i.name, i.member_count))

def get_user(user_id):
    data = func.Jsonn()
    f = data.read()
    for i in f:
        if i['user_id'] == user_id:
            return i
    return None

class SignUp(ui.Modal):
    def __init__(self):
        super().__init__(title=f"유빈이 서비스 가입!")
        self.id = discord.ui.InputText(label = "닉네임" , placeholder = "게임에 이용할 닉네임을 적어주세요!", min_length=3, max_length=12)
        self.add_item(self.id)

    async def callback(self, inter : discord.Interaction):
        user = inter.user
        data = func.Jsonn(user=user)
        if data.name_check(self.id.value) == "돌아가":
            return await inter.response.send_message('닉네이 중복이에요!',ephemeral=True)
        if korcen.check(self.id.value):
            return await inter.response.send_message('닉네임에 욕설이 포함되어 있어요!',ephemeral=True)
        data.signup(self.id.value)
        embed = Embed(description=f"가입 성공!",color = 0xd561ff,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.set_author(name="Yubin | Search", icon_url=inter.user.avatar.url)
        embed.add_field(name="닉네임", value=f"`{self.id.value}`", inline=True)
        embed.add_field(name="돈", value=f"`100000`", inline=True)
        embed.add_field(name="레벨", value=f"`레벨 : 1, exp : 0`", inline=True)
        embed.set_footer(icon_url="https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMTEwMDRfNDIg%2FMDAxNjMzMzA3OTIyMjYw.1eGG1vtf5IK0VS2DXY-3mDEsOdfQml9Np8mtchrOLocg.-2Sj_PnOxzHb4ZiaZvge8OTpSG7fak9yYYZR9_vKlZcg.JPEG.yeeun4333%2Foutput_3864043908.jpg&type=a340")
        return await inter.response.send_message(embed=embed)

@client.slash_command(name="가입",description="서비스에 가입하실 수 있습니다!")
async def signup(ctx:discord.ApplicationContext) -> None: 
    user = ctx.author
    data = func.Jsonn(user=user)
    try: y = data.user_read()
    except: await ctx.send_modal(SignUp())

@client.slash_command(name="광질",description="광질을 할 수 있습니다!")
@commands.cooldown(1, 2, commands.BucketType.user)
async def kang(ctx:discord.ApplicationContext) -> None:
    rulee = {"돌":0, "구리":0, "철":0, "금":0, "다이아몬드":0, "에메랄드":0}
    user = ctx.author
    data = func.Jsonn(user=user)
    try: data.all_read()[str(user.id)]
    except: return await ctx.respond("**/가입**통해 가입 후 이용해주세요!")
    pickaxe = data.choose_pickaxe()
    if pickaxe == "곡괭이 없음": return await ctx.respond("현재 소유중인 곡괭이가 없어요!")
    block = bbobgi; random.shuffle(block); n = random.randint(43, 100)*(int(pickaxe.split('.')[-1])**2)
    for i in range(n):
        y = np.random.choice(bbobgi, replace=False); rulee[y] = 1+rulee[y]
    mine = data.mining(n, rulee); exp = data.plus_exp(n)
    embed = Embed(description=f"광질중..",color = 0xd561ff,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
    embed.set_author(name="Yubin | Search", icon_url=user.avatar.url)
    embed.add_field(name="진행도", value=f"▯▯▯▯▯▯▯▯▯▯", inline=True)
    embed.set_footer(icon_url="https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMTEwMDRfNDIg%2FMDAxNjMzMzA3OTIyMjYw.1eGG1vtf5IK0VS2DXY-3mDEsOdfQml9Np8mtchrOLocg.-2Sj_PnOxzHb4ZiaZvge8OTpSG7fak9yYYZR9_vKlZcg.JPEG.yeeun4333%2Foutput_3864043908.jpg&type=a340")
    msg = await ctx.respond(embed=embed)
    z = 1
    while z <= 10: 
        embed = Embed(description=f"광질중..",color = 0xd561ff,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.set_author(name="Yubin | Search", icon_url=user.avatar.url)
        embed.add_field(name="진행도", value=f"{z*'▮'}{(10-z)*'▯'}", inline=True)
        embed.set_footer(icon_url="https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMTEwMDRfNDIg%2FMDAxNjMzMzA3OTIyMjYw.1eGG1vtf5IK0VS2DXY-3mDEsOdfQml9Np8mtchrOLocg.-2Sj_PnOxzHb4ZiaZvge8OTpSG7fak9yYYZR9_vKlZcg.JPEG.yeeun4333%2Foutput_3864043908.jpg&type=a340")
        await msg.edit_original_message(embed=embed)
        z += 1
    embed = Embed(description=f"광질 완료!",color = 0xd561ff,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
    embed.set_author(name="Yubin | Mining", icon_url=user.avatar.url)
    embed.add_field(name="캔 블럭 수", value=f"**{n}**개", inline=True)
    if type(mine) is list:embed.add_field(name="곡괭이", value=f"사용한 곡 : **{pickaxe} 곡괭이**, 내구도 : **{mine[0]}**", inline=True)
    else: embed.add_field(name="곡괭이", value=f"사용한 곡 : **{pickaxe} 곡괭이**, 내구도 : **{mine}**", inline=True)
    embed.add_field(name="레벨", value=f"레벨 : **{exp['level']}**, 경험치 : **{exp['exp']}**", inline=True)
    embed.add_field(name="돌", value=f"**{rulee['돌']}**개", inline=True); embed.add_field(name="구리", value=f"**{rulee['구리']}**개", inline=True)
    embed.add_field(name="철", value=f"**{rulee['철']}**개", inline=True); embed.add_field(name="금", value=f"**{rulee['금']}**개", inline=True)
    embed.add_field(name="다이아몬드", value=f"**{rulee['다이아몬드']}**개", inline=True); embed.add_field(name="에메랄드", value=f"**{rulee['에메랄드']}**개", inline=True)
    embed.set_footer(icon_url="https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMTEwMDRfNDIg%2FMDAxNjMzMzA3OTIyMjYw.1eGG1vtf5IK0VS2DXY-3mDEsOdfQml9Np8mtchrOLocg.-2Sj_PnOxzHb4ZiaZvge8OTpSG7fak9yYYZR9_vKlZcg.JPEG.yeeun4333%2Foutput_3864043908.jpg&type=a340")
    await msg.edit_original_message(embed=embed)

@client.slash_command(name="제작",description="곡괭이를 제작 할 수 있습니다!")
async def make(ctx:discord.ApplicationContext, 레벨: Option(str, description="곡괭이의 레벨을 선택해주세요!", choices=["lv.1 곡괭이", "lv.2 곡괭이", "lv.3 곡괭이", "lv.4 곡괭이", "lv.5 곡괭이"])) -> None: 
    user = ctx.author
    data = func.Jsonn(user=user)
    nagoo = data.plus_pickaxe(int(레벨[3]))
    if nagoo == "놉":
        return await ctx.respond("돈이 모자라요!")
    embed = Embed(description=f"{레벨} 를 제작하였어요!",color = 0xd561ff,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
    embed.set_author(name="Yubin | Make", icon_url=user.avatar.url)
    embed.add_field(name="내구도", value=f"**{nagoo}**", inline=True)
    embed.add_field(name="채굴당 캘 수 있는 블록 수", value=f"**{(int(레벨[3])**2)*50}**~**{(int(레벨[3])**2)*100}**개", inline=True)
    await ctx.respond(embed=embed)

async def get_pickaxe(ctx: discord.AutocompleteContext):
    data = func.Jsonn(ctx.interaction.user)
    return data.get_axe()

@client.slash_command(name="수리",description="곡괭이의 내구도를 풀로 올립니다")
@option("곡괭이", description="수리할 곡괭이를 골라주세요!", autocomplete=get_pickaxe)
async def fix(ctx:discord.ApplicationContext, 곡괭이:str) -> None: 
    user = ctx.author
    data = func.Jsonn(user=user)
    lv = 곡괭이.split(' : ')[0].split(' ')[0]
    nagoo = int(곡괭이.split(' : ')[2])
    y = data.fix_pickaxe(lv=lv, nagoo=nagoo)
    if y == 'nope':
        await ctx.respond("도구를 수리할 재료가 부족합니다!")
    else:
        embed = Embed(description=f"{lv} 곡괭이를 성공적으로 수리 하였어요!",color = 0xd561ff,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.set_author(name="Yubin | Mining", icon_url=user.avatar.url)
        embed.add_field(name="내구도", value=f"**{nagoo}** -> **{(y)}**", inline=True)
        await ctx.respond(embed=embed)

async def get_block(ctx: discord.AutocompleteContext):
    data = func.Jsonn(ctx.interaction.user)
    return data.get_block()

@client.slash_command(name="판매",description="광물을 판매 합니다!")
@option("광물", description="판매할 광물을 골라주세요!", autocomplete=get_block)
async def fix(ctx:discord.ApplicationContext, 광물:str) -> None: 
    user = ctx.author
    data = func.Jsonn(user=user)
    if 광물 == "전체":
        y = data.sell_block(category="전체")
        category= "**광물** 을 모두"
        block = "보유중인 광물"; block_count = y[-1]
    else:
        block = 광물.split(' : ')[0]; block_count = 광물.split(" : ")[1];y=data.sell_block(category=block)
        category=f"**{block}** 을/를 모두"
    embed = Embed(description=f"{category} 판매 하였어요!",color = 0xd561ff,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
    embed.set_author(name="Yubin | Make", icon_url=user.avatar.url)
    embed.add_field(name="블록", value=f"**{block} {block_count}** 개를 판매")
    embed.add_field(name="수익", value=f"번 돈 : **{y[0]}**, 현재 돈 : **{y[1]}**", inline=True)
    await ctx.respond(embed=embed)

@client.slash_command(description = "테스트 커맨드")
async def 테스트(inter):
    for emoji in inter.guild.emojis:
        print(emoji.name+" = "+f"'<a:{emoji.name}:{emoji.id}>'") 

client.run('MTAwNTMwMjQ1Nzg5MjYyMjM2Ng.G5DCYe.99519GSRClMR3YtkjjiZSF-9vDESf-yoLGKslY')