# -*- coding: utf-8 -*-
import asyncio
import jsons
import requests
from discord import ChannelType
from datetime import datetime

import consts
import utils


class Command:
    """
    Botのコマンドクラス.
    """

    @property
    def config(self):
        return self.__config

    def __init__(self, config):
        """
        コンストラクタ.
        :param config: コンフィグ管理インスタンス.
        :type config: ASWDConfig
        """
        self.__config = config

    def usage(self):
        """
        使い方を返却する.
        :param message: Discordメッセージインスタンス
        :type message: Message
        :return: コマンドの使い方
        :rtype: str
        """
        pass

    def is_call(self, msg):
        """
        コマンドが呼び出されたか.
        :param msg: 書き込まれたメッセージ
        :type msg: str
        :return: 処理結果
        :rtype: bool
        """
        pass

    def is_cmd_help(self, msg, start_index):
        """
        コマンドのヘルプが呼び出されたか.
        :param msg: 書き込まれたメッセージ
        :type msg: str
        :param start_index: コマンド部の文字数
        :type start_index: int
        :return: 処理結果
        :rtype: bool
        """
        return start_index < len(msg) and msg[start_index:].startswith("/?")

    async def execute(self, message):
        """
        コマンドを実行する.
        :param message: Discordメッセージインスタンス
        :type message: Message
        :return: 処理結果
        :rtype: bool
        """
        pass

    async def send_message(self, channel, msg):
        """
        メッセージを送信する.
        :param channel: メッセージ送信先Channelインスタンス
        :type channel: ChannelType
        :param msg: 送信するメッセージ
        :type msg: str
        :return: 処理結果
        :rtype: bool
        """
        await utils.send_message(self.config.client, channel, msg)


class AllCommand(Command):
    """
    全コマンドを扱うコマンドクラス
    """

    @property
    def cmd_list(self):
        return self.__cmd_list

    def __init__(self, config, cmd_list):
        super().__init__(config)
        self.__cmd_list = cmd_list


class CommandManager:
    """
    コマンド管理クラス.
    コマンド実行はこのクラスの execute() にメッセージを食わせる.
    """

    def __init__(self, config):
        """
        コンストラクタ.
        コマンドクラス追加時は __cmd_list にコマンドインスタンスを追加すること.
        :param config: コンフィグ管理インスタンス
        :type config: ASWDConfig
        """

        self.__config = config
        self.__cmd_list = [
            StartCommand(config),
            StopCommand(config),
            AddBlackListCommand(config),
            DelBlackListCommand(config),
            ListBlackListCommand(config),
            AddServerCommand(config),
            DelServerCommand(config),
            StatusCommand(config),
            SetWatchWorldCommand(config),
            SetWatchIntervalCommand(config),
            SetPlayerSbnCountCommand(config),
            FuckYeahCommand(config)
        ]
        self.__help_cmd = HelpCommand(config, self.__cmd_list)
        self.__cmd_list.append(self.__help_cmd)

    async def execute(self, message):
        """
        コマンド実行.
        :param message: Discordのメッセージインスタンス
        :type message: Message
        :return: 処理結果
        :rtype: bool
        """

        # コマンド呼び出し判定
        if not message.content.startswith("/"):
            return False

        # コマンド判定
        call_cmd = None
        for cmd in self.__cmd_list:
            if cmd.is_call(message.content):
                call_cmd = cmd
                break
        if not call_cmd:
            # コマンドが存在しない場合ヘルプ表示
            msg = "コマンドが正しくありません.\n" + self.__help_cmd.usage()
            await utils.send_message(self.__config.client, message.channel, msg)
            return False

        return await call_cmd.execute(message)


class HelpCommand(AllCommand):
    """
    ヘルプを表示する.
    """

    def __init__(self, config, cmd_list):
        ret = []
        for cmd in cmd_list:
            if type(cmd) == HelpCommand:
                continue
            ret.append(cmd)
        super().__init__(config, ret)

    def usage(self):
        msg = "/? : ヘルプを表示します. /start /? のように入力するとコマンドのヘルプを表示します."
        return msg

    def is_call(self, msg):
        return msg == "/?"

    async def execute(self, message):
        ret = []
        ret.append(self.usage())
        for cmd in self.cmd_list:
            ret.append(cmd.usage())
        msg = "\n".join(ret)
        await self.send_message(message.channel, msg)
        return True


class StartCommand(Command):
    """
    サーバ監視開始コマンド.
    """

    def __init__(self, config):
        super().__init__(config)

    def usage(self):
        msg = "/start : 監視を開始します."
        return msg

    def is_call(self, msg):
        return msg.startswith("/start")

    async def execute(self, message):
        print('/start call...')

        # コマンドヘルプ判定
        if len(message.content) >= 7:
            if self.is_cmd_help(message.content, 7):
                msg = self.usage()
                await self.send_message(message.channel, msg)
                return False
            else:
                msg = "コマンドに誤りがあります.\n" + self.usage()
                await self.send_message(message.channel, msg)
                return False

        # 起動確認
        if self.config.is_watch_started:
            msg = "監視継続します."
            return False

        msg = "監視開始."
        await self.send_message(message.channel, msg)

        self.config.is_watch_started = True
        while self.config.is_watch_started:
            print('WebServiceよりjson取得開始.')
            atlas_grids_json = requests.get(self.config.url).text
            if not atlas_grids_json:
                print('取得失敗. 処理終了.')
                return False
            print('取得成功.')
            grids_dict = jsons.loads(atlas_grids_json)

            # サーバ情報収集
            servers_info = {}
            for grid in grids_dict["grids"]:
                server_name = grid["grid"]
                player_count = len(grid["players"])
                player_sbn_count = 0
                last_server_info = None
                if len(self.config.last_servers_info) != 0 and server_name in self.config.last_servers_info:
                    last_server_info = self.config.last_servers_info[server_name]
                if last_server_info is not None:
                    last_player_count = last_server_info["player_count"]
                    if last_player_count is not None:
                        player_sbn_count = player_count - last_player_count
                players = grid["players"]
                blacklist_players = []
                for bl_player in blacklist_players:
                    for player in players:
                        player_name = player["name"]
                        if player_name.lower().find(bl_player.lower()) == -1:
                            continue
                        blacklist_players.append(player)

                servers_info[server_name] = {
                    "server_name": server_name,
                    'player_count': player_count,
                    "player_sbn_count": player_sbn_count,
                    "blacklist_players": blacklist_players
                }

            # サーバ情報を元に通知
            timestr = datetime.now().strftime("%m/%d %H:%M")
            tgt_channels = utils.get_channels(self.config.client)
            print("get_channels end. tgt_channels.len=", len(tgt_channels) > 0)
            if len(tgt_channels) > 0:
                for tgt_channel in tgt_channels:
                    if tgt_channel.name.upper() not in servers_info:
                        msg = "{}　{}　データ取得エラー.".format(timestr, tgt_channel.name.upper())
                        await self.send_message(tgt_channel, msg)
                        continue
                    server_info = servers_info[tgt_channel.name.upper()]
                    if server_info is None:
                        continue

                    server_name = server_info["server_name"]
                    player_count = server_info["player_count"]
                    player_sbn_count = server_info["player_sbn_count"]
                    blacklist_players = server_info["blacklist_players"]

                    # 定例メッセージ送信
                    msg = "{}　{}　人数:{}　BL対象者:{}".format(timestr, server_name, player_count, blacklist_players)
                    await self.send_message(tgt_channel, msg)

                    # 警告メッセージ(人数急増)
                    if self.config.player_sbn_count <= player_sbn_count:
                        msg = "@everyone サーバ人数急増. 閾値:{} 増加人数:{}".format(self.config.player_sbn_count, player_sbn_count)
                        await self.send_message(tgt_channel, msg)

                    # 警告メッセージ(ブラックリスト対象の侵入)
                    if len(blacklist_players) > 0:
                        if server_name not in self.config.blacklist_notice_server_names:
                            msg = "@everyone ブラックリスト対象侵入. 対象:{}".format(blacklist_players)
                            await self.send_message(tgt_channel, msg)
                            self.config.blacklist_notice_server_names.append(server_name)

                    # 通常メッセージ(ブラックリスト対象者0になった)
                    if len(blacklist_players) == 0 and server_name in self.config.blacklist_notice_server_names:
                        msg = "ブラックリスト対象はいなくなりました."
                        await self.send_message(tgt_channel, msg)
                        self.config.blacklist_notice_server_names.remove(server_name)

            # 今回取得したサーバ情報を保持
            self.config.last_servers_info = servers_info
            await asyncio.sleep(self.config.watch_interval)
        return True


class StopCommand(Command):
    """
    サーバ監視終了コマンド.
    """

    def __init__(self, config):
        super().__init__(config)

    def usage(self):
        msg = "/stop : 監視を終了します."
        return msg

    def is_call(self, msg):
        return msg.startswith("/stop")

    async def execute(self, message):
        print("/stop call...")

        # コマンドヘルプ判定
        if 6 <= len(message.content):
            if self.is_cmd_help(message.content, 6):
                msg = self.usage()
                await self.send_message(message.channel, msg)
                return False
            else:
                msg = "コマンドに誤りがあります.\n" + self.usage()
                await self.send_message(message.channel, msg)
                return False

        self.config.is_watch_started = False
        msg = "監視終了."
        await self.send_message(message.channel, msg)
        return True


class AddBlackListCommand(Command):
    """
    ブラックリスト追加コマンド.
    """

    def __init__(self, config):
        super().__init__(config)

    def usage(self):
        msg = "/add bl [プレイヤー名] : ブラックリストにプレイヤーを追加します."
        return msg

    def is_call(self, msg):
        return msg.startswith('/add bl ')

    async def execute(self, message):
        print("/add bl call...")

        # コマンドヘルプ判定
        if 8 <= len(message.content):
            if self.is_cmd_help(message.content, 8):
                msg = self.usage()
                await self.send_message(message.channel, msg)
                return False

        bl_player = message.content[8:]
        if not bl_player:
            msg = "「/add bl [プレイヤー名]」を正しく入力してください."
            await self.send_message(message.channel, msg)
            return False
        self.config.add_blacklist(bl_player)
        msg = "ブラックリストに追加しました."
        await self.send_message(message.channel, msg)
        return True


class DelBlackListCommand(Command):
    """
    ブラックリスト削除コマンド.
    """

    def __init__(self, config):
        super().__init__(config)

    def usage(self):
        msg = "/del bl [プレイヤー名] : ブラックリストからプレイヤーを削除します."
        return msg

    def is_call(self, msg):
        return msg.startswith('/del bl ')

    async def execute(self, message):
        print("/del bl call...")

        # コマンドヘルプ判定
        if 8 <= len(message.content):
            if self.is_cmd_help(message.content, 8):
                msg = self.usage()
                await self.send_message(message.channel, msg)
                return False

        bl_player = message.content[8:]
        if not bl_player:
            msg = "「/del bl [プレイヤー名]」を正しく入力してください."
            await self.send_message(message.channel, msg)
            return False
        self.config.del_blacklist(bl_player)
        msg = "ブラックリストから削除しました."
        await self.send_message(message.channel, msg)
        return True


class ListBlackListCommand(Command):
    """
    ブラックリスト一覧表示コマンド.
    """

    def __init__(self, config):
        super().__init__(config)

    def usage(self):
        msg = "/list bl : ブラックリストの一覧を表示します."
        return msg

    def is_call(self, msg):
        return msg.startswith("/list bl")

    async def execute(self, message):
        print("/list bl call...")

        # コマンドヘルプ判定
        if 9 <= len(message.content):
            if self.is_cmd_help(message.content, 9):
                msg = self.usage()
                await self.send_message(message.channel, msg)
                return False
            else:
                msg = "コマンドに誤りがあります.\n" + self.usage()
                await self.send_message(message.channel, msg)
                return False

        msg = "ブラックリスト: {}".format(self.config.blacklist)
        await self.send_message(message.channel, msg)
        return True


class AddServerCommand(Command):
    """
    監視対象サーバ追加コマンド.
    """

    def __init__(self, config):
        super().__init__(config)

    def usage(self):
        msg = "/add server [サーバー名(A1-O15)] : Discordにサーバー監視報告用のチャンネルを追加します."
        return msg

    def is_call(self, msg):
        return msg.startswith("/add server")

    async def execute(self, message):
        print("/add server call...")

        # コマンドヘルプ判定
        if 12 <= len(message.content):
            if self.is_cmd_help(message.content, 12):
                msg = self.usage()
                await self.send_message(message.channel, msg)
                return False

        # バリデーション
        server_name = message.content[12:].upper()
        if server_name not in consts.SERVER_NAMES:
            msg = "コマンドに誤りがあります.\n" + self.usage()
            await self.send_message(message.channel, msg)
            return False
        if not message.server:
            msg = "サーバが見つかりません."
            await self.send_message(message.channel, msg)
            return False
        if utils.exists_channel(message.server, server_name):
            msg = "対象サーバは既に監視対象です."
            await self.send_message(message.channel, msg)
            return False

        # 処理
        print("サーバ監視報告チャンネル作成. name={}".format(server_name))
        await self.config.client.create_channel(message.server, server_name, type=ChannelType.text)
        print("サーバ監視報告チャンネル作成完了.")
        msg = "{}チャンネル追加. 監視情報はそこに出力します.".format(server_name)
        await self.send_message(message.channel, msg)
        return True


class DelServerCommand(Command):
    """
    監視対象サーバ削除コマンド.
    """

    def __init__(self, config):
        super().__init__(config)

    def usage(self):
        msg = "/del server [サーバー名(A1-O15)] : Discordのサーバー監視報告用のチャンネルを削除します."
        return msg

    def is_call(self, msg):
        return msg.startswith("/del server")

    async def execute(self, message):
        print("/del server call...")

        # コマンドヘルプ判定
        if 12 <= len(message.content):
            if self.is_cmd_help(message.content, 12):
                msg = self.usage()
                await self.send_message(message.channel, msg)
                return False

        # バリデーション
        server_name = message.content[12:].upper()
        if server_name not in consts.SERVER_NAMES:
            msg = "コマンドに誤りがあります.\n" + self.usage()
            await self.send_message(message.channel, msg)
            return False
        if not message.server:
            msg = "サーバが見つかりません."
            await self.send_message(message.channel, msg)
            return False
        channel = utils.find_channel(message.server, server_name)
        if not channel:
            msg = "対象サーバは監視対象ではありません."
            await self.send_message(message.channel, msg)
            return False

        # 処理
        print("サーバ監視報告チャンネル削除. name={}".format(server_name))
        await self.config.client.delete_channel(channel)
        print("サーバ監視報告チャンネル作成完了.")
        msg = "{}チャンネル削除.".format(server_name)
        await self.send_message(message.channel, msg)
        return True


class StatusCommand(Command):
    """
    ステータス表示コマンド.
    """

    def __init__(self, config):
        super().__init__(config)

    def usage(self):
        msg = "/status : 設定値など現在の状態を表示します."
        return msg

    def is_call(self, msg):
        return msg.startswith("/status")

    async def execute(self, message):
        print("/status call...")

        # コマンドヘルプ判定
        if 8 <= len(message.content):
            if self.is_cmd_help(message.content, 8):
                msg = self.usage()
                await self.send_message(message.channel, msg)
                return False
            else:
                msg = "コマンドに誤りがあります.\n" + self.usage()
                await self.send_message(message.channel, msg)
                return False

        msg_started = "監視中" if self.config.is_watch_started else "-"
        msg = "監視状態:{}\n監視ワールド:{}\n監視間隔(秒):{}\n通知対象プレイヤー増加数:{}\nブラックリスト:{}\nブラックリスト侵入中サーバ:{}".format(
            msg_started, self.config.watch_world, self.config.watch_interval, self.config.player_sbn_count, self.config.blacklist, self.config.blacklist_notice_server_names)
        await self.send_message(message.channel, msg)
        return True


class SetWatchWorldCommand(Command):
    """
    監視ワールド設定コマンド.
    """

    def __init__(self, config):
        super().__init__(config)

    def usage(self):
        msg = "/set world [NA or EU] : 監視ワールドを設定します."
        return msg

    def is_call(self, msg):
        return msg.startswith('/set world')

    async def execute(self, message):
        print("/set world  call...")

        # コマンドヘルプ判定
        if 11 <= len(message.content):
            if self.is_cmd_help(message.content, 11):
                msg = self.usage()
                await self.send_message(message.channel, msg)
                return False

        val = message.content[11:]
        is_val = val == "NA" or val == "EU"
        if not val or not is_val:
            msg = "コマンドが不正です. 正しい値を設定してください."
            await self.send_message(message.channel, msg)
            return False

        self.config.watch_interval = val

        msg = "監視ワールドを{}秒に設定しました.".format(val)
        await self.send_message(message.channel, msg)
        return True


class SetWatchIntervalCommand(Command):
    """
    監視間隔設定コマンド.
    """

    def __init__(self, config):
        super().__init__(config)

    def usage(self):
        msg = "/set interval : 監視間隔(秒)を設定します."
        return msg

    def is_call(self, msg):
        return msg.startswith('/set interval')

    async def execute(self, message):
        print("/set interval call...")

        # コマンドヘルプ判定
        if 14 <= len(message.content):
            if self.is_cmd_help(message.content, 14):
                msg = self.usage()
                await self.send_message(message.channel, msg)
                return False

        val = message.content[14:]
        if not val or not val.isdecimal():
            msg = "コマンドが不正です. 数値を設定してください."
            await self.send_message(message.channel, msg)
            return False

        int_val = int(val)
        if int_val < 30:
            msg = "指定した数値が30秒未満のため、30秒を設定します."
            await self.send_message(message.channel, msg)
            int_val = 30
        self.config.watch_interval = int_val

        msg = "監視間隔を{}秒に設定しました.".format(int_val)
        await self.send_message(message.channel, msg)
        return True


class SetPlayerSbnCountCommand(Command):
    """
    通知対象プレイヤー増加数設定コマンド.
    """

    def __init__(self, config):
        super().__init__(config)

    def usage(self):
        msg = "/set player_count : 通知対象プレイヤー増加数を設定します."
        return msg

    def is_call(self, msg):
        return msg.startswith('/set player_count')

    async def execute(self, message):
        print("/set player_count call...")

        # コマンドヘルプ判定
        if 18 <= len(message.content):
            if self.is_cmd_help(message.content, 18):
                msg = self.usage()
                await self.send_message(message.channel, msg)
                return False

        val = message.content[18:]
        if not val or not val.isdecimal():
            msg = "コマンドが不正です. 数値を設定してください."
            await self.send_message(message.channel, msg)
            return False

        int_val = int(val)
        if int_val < 3:
            msg = "指定した数値が3人未満のため、3人を設定します."
            await self.send_message(message.channel, msg)
            int_val = 3
        self.config.player_sbn_count = int_val

        msg = "通知対象プレイヤー増加数を{}人に設定しました.".format(int_val)
        await self.send_message(message.channel, msg)
        return True


class FuckYeahCommand(Command):
    """
    Fuck YEAH !!
    """

    def __init__(self, config):
        super().__init__(config)

    def usage(self):
        msg = "/fuckxxx : Fuck YEAH !!"
        return msg

    def is_call(self, msg):
        return msg.startswith("/fuck")

    async def execute(self, message):
        print("/fuckxxx call...")

        # コマンドヘルプ判定
        if 6 <= len(message.content):
            if self.is_cmd_help(message.content, 6):
                msg = self.usage()
                await self.send_message(message.channel, msg)
                return False

        msg = "Fuck YEAH !!"
        await self.send_message(message.channel, msg)
        msg = "https://www.youtube.com/watch?v=IhnUgAaea4M&feature=youtu.be&t=8"
        await self.send_message(message.channel, msg)
        return True
