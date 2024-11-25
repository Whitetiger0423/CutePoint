import pickle
import random
import os
import discord
import dotenv
import time
import asyncio

bot = discord.Bot()
dotenv.load_dotenv()

path = "./"
file_list = os.listdir(path)
file_list_pkl = [file for file in file_list if file.endswith(".pkl")]

async def check():
    while True:
        for i in file_list_pkl:
            with open(f"{i}", "rb") as f:
                UserData = pickle.load(f)
                UserData += 1
            with open(f"{i}", "wb") as f:
                pickle.dump(UserData, f)
        await asyncio.sleep(20)

@bot.event
async def on_ready():
    print(f"Log In as {bot.user.name}({bot.user.id})")
    await check()

@bot.slash_command(description="유저 정보를 등록합니다.")
async def 등록(ctx):
    if os.path.isfile(f"{ctx.user.id}.pkl") == False:
        embed = discord.Embed(
            title="등록", description="봇의 서비스에 등록합니다. 동의하지 않을 경우 서비스 이용에 제한이 있을 수 있습니다."
        )
        embed.add_field(name="수집하는 정보", value="유저의 디스코드 id", inline=False)

        class Button(discord.ui.View):
            @discord.ui.button(label="⭕ 동의", style=discord.ButtonStyle.primary)
            async def primary(
                self, button: discord.ui.Button, interaction: discord.Interaction
            ):
                UserData = 1
                if interaction.user.id == ctx.user.id:
                    with open(f"{interaction.user.id}.pkl", "wb") as f:
                        pickle.dump(UserData, f)
                    new_embed = discord.Embed(
                        title="등록 완료", description=""
                    )
                    new_embed.add_field(
                        name="", value=f"<@!{interaction.user.id}>님, 등록을 완료하였습니다. 아이디는 {interaction.user.id}입니다."
                    )
                    self.disable_all_items()
                    await interaction.response.edit_message(view=self, embed=new_embed)

            @discord.ui.button(label="❌ 취소", style=discord.ButtonStyle.danger)
            async def danger(
                self, button: discord.ui.Button, interaction: discord.Interaction
            ):
                if interaction.user.id == ctx.user.id:
                    new_embed = discord.Embed(
                        title="등록 취소", description=""
                    )
                    new_embed.add_field(
                        name="", value=f"등록이 취소되었습니다."
                    )
                    self.disable_all_items()
                    await interaction.response.edit_message(view=self, embed=new_embed)
        await ctx.respond(embed=embed, view=Button())

    else:
        embed = discord.Embed(title="등록된 유저", description="")
        embed.add_field(
            name="", value="이미 등록되었습니다. `/탈퇴` 명령어를 통해 탈퇴할 수 있습니다.", inline=False
        )
        await ctx.respond(embed=embed)


@bot.slash_command(description="봇 서비스를 탈퇴합니다.")
async def 탈퇴(ctx):
    if os.path.isfile(f"{ctx.user.id}.pkl"):
        embed = discord.Embed(
            title="탈퇴", description="봇의 서비스를 탈퇴합니다. 탈퇴할 경우 모든 데이터가 파기되며, 복구하기 어렵습니다."
        )
        embed.add_field(
            name="파기하는 정보", value="유저의 디스코드 id, 서비스 이용 중 가챠 기록", inline=False
        )

        class Button(discord.ui.View):
            @discord.ui.button(label="⭕ 동의", style=discord.ButtonStyle.primary)
            async def primary(
                self, button: discord.ui.Button, interaction: discord.Interaction
            ):
                if interaction.user.id == ctx.user.id:
                    os.remove(f"{interaction.user.id}.pkl")
                    new_embed = discord.Embed(
                        title="탈퇴 완료", description=""
                    )
                    new_embed.add_field(
                        name="", value=f"<@!{interaction.user.id}>님, 탈퇴를 완료하였습니다."
                    )
                    self.disable_all_items()
                    await interaction.response.edit_message(view=self, embed=new_embed)

            @discord.ui.button(label="❌ 취소", style=discord.ButtonStyle.danger)
            async def danger(
                self, button: discord.ui.Button, interaction: discord.Interaction
            ):
                if interaction.user.id == ctx.user.id:
                    new_embed = discord.Embed(
                        title="탈퇴 취소", description=""
                    )
                    new_embed.add_field(
                        name="", value=f"탈퇴가 취소되었습니다."
                    )
                    self.disable_all_items()
                    await interaction.response.edit_message(view=self, embed=new_embed)

        await ctx.respond(embed=embed, view=Button())

    else:
        embed = discord.Embed(title="등록하지 않은 유저", description="")
        embed.add_field(name="", value="`/등록`을 통해 가입해주세요.", inline=False)
        await ctx.respond(embed=embed)


@bot.slash_command(description="본인의 정보를 확인합니다.")
async def 정보(ctx):
    if os.path.isfile(f"{ctx.user.id}.pkl"):
        with open(f"{ctx.user.id}.pkl", "rb") as f:
            UserData = pickle.load(f)
        embed = discord.Embed(title="유저 정보", description="")
        embed.add_field(name="ID", value=f"`{ctx.user.id}`", inline=True)
        embed.add_field(
            name="포인트",
            value=f"{UserData}",
            inline=False,
        )
    else:
        embed = discord.Embed(title="등록되지 않은 유저", description="")
        embed.add_field(name="", value="`/등록`을 통해 가입한 후 다시 사용해주세요.", inline=False)
    await ctx.respond(embed=embed)

bot.run(os.getenv("BOT_TOKEN"))
