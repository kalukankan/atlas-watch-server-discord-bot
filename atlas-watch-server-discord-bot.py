# -*- coding: utf-8 -*-
import os
import discord
from discord import ChannelType, Client, Message
from awsdb import commands, consts
from awsdb.utils import ASWDConfig, Utils
import traceback


# global var
client: Client = discord.Client()
config: ASWDConfig = ASWDConfig(client)
cmd_manager: commands.CommandManager = commands.CommandManager(config)


@client.event
async def on_ready():
    """
    Discordクライアント初期化イベント
    :return: None
    :rtype: None
    """
    print('起動開始...')
    print('ユーザ名:', client.user.name)
    print('ユーザID:', client.user.id)
    print('------')

    try:
        print("ログ出力フォルダ作成.")
        os.makedirs(consts.LOG_FOLDER, exist_ok=True)

        servers = Utils.get_none_cmd_channel_servers(client)
        if servers:
            print("Bot用コマンドチャンネル追加...")
            for server in servers:
                await client.create_channel(server, consts.CMD_CHANNEL_NAME, type=ChannelType.text)
            print("Bot用コマンドチャンネル追加完了.")

        msg = "起動.\nこのチャンネルでコマンドを実行します.\n/? を入力すると使い方を表示します."
        channels = Utils.get_cmd_channels(client)
        for channel in channels:
            await client.send_message(channel, msg)
    except Exception as e:
        print("【エラー】on_ready. 処理終了.")
        with open(consts.LOG_FILE, 'a') as f:
            traceback.print_exc(file=f)
        exit(1)


@client.event
async def on_message(message):
    """
    メッセージ書き込みイベント
    :param message: 書き込まれたメッセージ
    :type message: Message
    :return: None
    :rtype: None
    """
    try:
        if message.channel.name.upper() == consts.CMD_CHANNEL_NAME and not message.author.bot:
            await cmd_manager.execute(message)
    except Exception as e:
        print("【エラー】on_message. 処理継続.")
        with open(consts.LOG_FILE, 'a') as f:
            traceback.print_exc(file=f)
        client.send_message(message.channel, "【エラー】複数回発生したら再起動か管理者に報告よろ.")


if __name__ == "__main__":
    client.run(config.token)
