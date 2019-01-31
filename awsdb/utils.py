# -*- coding: utf-8 -*-
import configparser

from discord import ChannelType, Client, Server

from awsdb import consts


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


class Utils:
    @classmethod
    async def send_message(cls, client, channel, msg):
        """
        Discordにメッセージを送信する.
        :param client: Discordクライアントインスタンス
        :type client: Client
        :param channel: メッセージを送信するチャンネルインスタンス
        :type channel: Channel
        :param msg: 送信するメッセージ
        :type msg: str
        :return: None
        :rtype: None
        """
        await client.send_message(channel, msg)

    @classmethod
    def get_channels(cls, client):
        """
        メッセージを送信するチャンネルのリストを取得
        :return: Discordサーバのチャンネル毎のリスト
        :rtype: list of Channel
        """
        print('get_channels call...')
        ret = []
        for server in client.servers:
            for channel in server.channels:
                if ChannelType.text != channel.type:
                    continue
                if not cls.exists_server_name(channel.name.upper()):
                    continue
                ret.append(channel)
        return ret

    @classmethod
    def get_none_cmd_channel_servers(cls, client):
        """
        Botコマンド用チャンネルのないサーバのリストを取得する.
        :param client: Disordのクライアントオブジェクト
        :type client: Client
        :return: サーバのリスト
        :rtype: list os Server
        """
        print('get_none_cmd_channel_servers call...')
        ret = []
        for server in client.servers:
            has_cmd_channel = False
            for channel in server.channels:
                if ChannelType.text != channel.type:
                    continue
                if channel.name.upper() not in consts.CMD_CHANNEL_NAME:
                    continue
                has_cmd_channel = True
                break
            if not has_cmd_channel:
                ret.append(server)
        return ret

    @classmethod
    def get_cmd_channels(cls, client):
        """
        Botコマンド用チャンネルのリストを取得する.
        :return: チャンネルのリスト
        :rtype: list of Channel
        """
        print('get_cmd_channels call...')
        ret = []
        for server in client.servers:
            for channel in server.channels:
                if ChannelType.text != channel.type:
                    continue
                if channel.name.upper() != consts.CMD_CHANNEL_NAME:
                    continue
                ret.append(channel)
                break
        return ret

    @classmethod
    def get_watch_server_names(cls, client):
        """
        監視サーバ名のチャンネル名のリストを取得する.
        :param client: Discordのクライアント.
        :return: Discordのチャンネル名のリスト.
        :rtype: list of str
        """
        print('get_watch_server_names call.')
        ret = []
        if not client:
            return ret
        for server in client.servers:
            if not server:
                continue
            for channel in server.channels:
                if not channel:
                    continue
                if ChannelType.text != channel.type:
                    continue
                if not cls.exists_server_name(channel.name.upper()):
                    continue
                ret.append(channel.name.upper())
        return list(set(ret))

    @classmethod
    def find_channel(cls, server, channel_name):
        """
        サーバ内より指定された名前のチャンネルを取得する.
        :param server: Discordのサーバインスタンス
        :type server: Server
        :param channel_name: Discordのチャンネル名
        :type channel_name: str
        :return: チャンネルインスタンス. 見つからない場合は None.
        :rtype: Channel
        """
        for channel in server.channels:
            if (channel.name.upper() == channel_name):
                return channel
        return None

    @classmethod
    def exists_channel(cls, server, channel_name):
        """
        指定したサーバ内に指定したチャンネルが存在するか.
        :param server: Discordのサーバインスタンス
        :type server: Server
        :param channel_name: Discordのチャンネル名
        :type channel_name: str
        :return: 処理結果
        :rtype: bool
        """
        for channel in server.channels:
            if channel.name.upper() == channel_name.upper():
                return True
        return False

    @classmethod
    def get_object(cls, key_name, key, items):
        """
        配列内の辞書より指定キーと一致するオブジェクトを取得する.
        :param key_name: キー名
        :type key_name: str
        :param key: 検索するキー
        :param items: 対象のリスト
        :type items: list
        :return: 検索結果.値が取得できない場合Noneを返却.
        """
        for x in items:
            if not x or key_name not in x:
                continue
            if x[key_name] == key:
                return x
        return None

    @classmethod
    def get_value(cls, key_name, key, value_name, items):
        """
        配列内の辞書より指定キーと一致する指定値を取得する.
        :param key_name: キー名
        :type key_name: str
        :param key: 検索するキー
        :param value_name: 取得したい値の名前
        :type value_name: str
        :param items: 対象のリスト
        :type items: list
        :return: 検索結果.値が取得できない場合Noneを返却.
        """
        for x in items:
            if not x or key_name not in x or value_name not in x:
                continue
            if x[key_name] == key:
                return x[value_name]
        return None

    @classmethod
    def exists_value(cls, key_name, value, items):
        """
        配列内の辞書に指定キーと一致する値が存在するか.
        :param key_name: キー名
        :type key_name: str
        :param value: 検索する値
        :param items: 対象のリスト
        :type items: list
        :return: 判定結果.
        :rtype: bool
        """
        for x in items:
            if not x or key_name not in x:
                continue
            if x[key_name] == value:
                return True
        return False

    @classmethod
    def get_server_id(cls, cluster_id, server_name):
        """
        クラスターIDとサーバ名(A1-O15)からサーバIDを取得する.
        :param cluster_id: クラスターID
        :type cluster_id: int
        :param server_name: サーバ名(A1-O15)
        :type server_name: str
        :return: サーバID
        :rtype: int
        """
        if (cluster_id < 1 or 4 < cluster_id):
            raise ValueError("クラスターIDが1-4の値を渡してください. cluster_id:{}".format(cluster_id))
        server = cls.get_object("name", server_name, consts.SERVER_NAMES)
        if not server:
            raise ValueError("サーバ名はA1-O15の値を渡してください. server_name:{}".format(server_name))
        return (cluster_id - 1) * 225 + server["id"]

    @classmethod
    def exists_server_name(cls, server_name):
        """
        サーバ名(A1-O15)が存在するか.
        :param server_name: サーバ名
        :type server_name: str
        :return: 判定結果.
        :rtype: bool
        """
        for x in consts.SERVER_NAMES:
            if not x or "name" not in x:
                continue
            if x["name"] == server_name:
                return True
        return False
