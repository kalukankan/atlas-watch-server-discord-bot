# -*- coding: utf-8 -*-

from discord import ChannelType

import consts


async def send_message(client, channel, msg):
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


def get_channels(client):
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
            if channel.name.upper() not in consts.SERVER_NAMES:
                continue
            ret.append(channel)
    return ret


def get_none_cmd_channel_servers(client):
    """
    Botコマンド用チャンネルのないサーバのリストを取得する.
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


def get_cmd_channels(client):
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


def find_channel(server, channel_name):
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


def exists_channel(server, channel_name):
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
