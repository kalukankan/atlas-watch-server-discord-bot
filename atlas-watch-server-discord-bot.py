# -*- coding: utf-8 -*-
import os

import discord
import configparser
from discord import ChannelType
import consts
import utils
import command
import traceback


class ASWDConfig:
    """
    atlas-server-watch-discord-bot コンフィグ管理クラス.
    """

    def __init__(self, client_val):
        self.__config = configparser.ConfigParser()
        self.__config.read(consts.CONFIG_FILE_NAME)
        self.__token = self.config.get(consts.SECTION_NAME, consts.KEY_TOKEN)
        self.__watch_world = int(self.config.get(consts.SECTION_NAME, consts.KEY_WATCH_WORLD))
        self.__watch_interval = int(self.config.get(consts.SECTION_NAME, consts.KEY_WATCH_INTERVAL))
        self.__player_sbn_count = int(self.config.get(consts.SECTION_NAME, consts.KEY_PLAYER_SBN_COUNT))
        self.__blacklist = self.config.get(consts.SECTION_NAME, consts.KEY_BLACKLIST).split(",")
        self.__is_watch_started = False
        self.__last_servers_info = {}
        self.__blacklist_notice_server_names = []
        self.__client = client_val

    @property
    def config(self):
        return self.__config

    @property
    def token(self):
        return self.__token

    @property
    def watch_world(self):
        return self.__watch_world

    @watch_world.setter
    def watch_world(self, watch_world):
        self.__watch_world = watch_world
        self.write()

    @property
    def watch_interval(self):
        return self.__watch_interval

    @watch_interval.setter
    def watch_interval(self, watch_interval):
        self.__watch_interval = watch_interval
        self.write()

    @property
    def player_sbn_count(self):
        return self.__player_sbn_count

    @player_sbn_count.setter
    def player_sbn_count(self, player_sbn_count):
        self.__player_sbn_count = player_sbn_count if player_sbn_count >= 3 else 3
        self.write()

    @property
    def blacklist(self):
        return self.__blacklist

    def add_blacklist(self, player):
        """
        ブラックリストにプレイヤーを追加する.
        :param player: プレイヤー名
        :type player: str
        :return: 処理結果(True: 追加成功, False: 既に存在するプレイヤー名がある等で追加失敗)
        :rtype: bool
        """
        if player in self.blacklist:
            return False
        self.blacklist.append(player)
        self.write()
        return True

    def del_blacklist(self, player):
        """
        ブラックリストからプレイヤーを削除する.
        :param player: プレイヤー名
        :type player: str
        :return: 処理結果(True: 削除成功, False: 存在しないプレイヤー名等で削除失敗)
        :rtype: bool
        """
        if player not in self.blacklist:
            return False
        self.blacklist.remove(player)
        self.write()
        return True

    @property
    def is_watch_started(self):
        return self.__is_watch_started

    @is_watch_started.setter
    def is_watch_started(self, val):
        self.__is_watch_started = val

    @property
    def last_servers_info(self):
        return self.__last_servers_info

    @last_servers_info.setter
    def last_servers_info(self, val):
        self.__last_servers_info = val

    @property
    def blacklist_notice_server_names(self):
        return self.__blacklist_notice_server_names
    
    @property
    def client(self):
        return self.__client

    def write(self):
        """
        コンフィグを書き込む.
        :return: None
        :rtype: None
        """
        configw = configparser.ConfigParser()
        configw.add_section(consts.SECTION_NAME)
        configw.set(consts.SECTION_NAME, consts.KEY_TOKEN, self.token)
        configw.set(consts.SECTION_NAME, consts.KEY_WATCH_WORLD, str(self.watch_world))
        configw.set(consts.SECTION_NAME, consts.KEY_WATCH_INTERVAL, str(self.watch_interval))
        configw.set(consts.SECTION_NAME, consts.KEY_PLAYER_SBN_COUNT, str(self.player_sbn_count))
        configw.set(consts.SECTION_NAME, consts.KEY_BLACKLIST, ",".join(self.blacklist))
        with open(consts.CONFIG_FILE_NAME, 'w') as configfile:
            configw.write(configfile)


# global var
client = discord.Client()
config = ASWDConfig(client)
cmd_manager = command.CommandManager(config)


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

        servers = utils.get_none_cmd_channel_servers(client)
        if servers:
            print("Bot用コマンドチャンネル追加...")
            for server in servers:
                await client.create_channel(server, consts.CMD_CHANNEL_NAME, type=ChannelType.text)
            print("Bot用コマンドチャンネル追加完了.")

        msg = "起動.\nこのチャンネルでコマンドを実行します.\n/? を入力すると使い方を表示します."
        channels = utils.get_cmd_channels(client)
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
