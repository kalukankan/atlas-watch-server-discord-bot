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
            if not exists_server_name(channel.name.upper()):
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


def get_watch_server_names(client):
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
            if not exists_server_name(channel.name.upper()):
                continue
            ret.append(channel.name.upper())
    return list(set(ret))


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


def get_object(key_name, key, items):
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


def get_value(key_name, key, value_name, items):
    """
    配列内の辞書より指定キーと一致する指定値を取得する.
    :param key_name: キー名
    :type key_name: str
    :param key: 検索するキー
    :param value_name: 取得したい値の名前
    :type value_name: str
    :param items: 対象のリスト
    :return: 検索結果.値が取得できない場合Noneを返却.
    """
    for x in items:
        if not x or key_name not in x or value_name not in x:
            continue
        if x[key_name] == key:
            return x[value_name]
    return None


def exists_value(key_name, value, items):
    """
    配列内の辞書に指定キーと一致する値が存在するか.
    :param key_name: キー名
    :type key_name: str
    :param value: 検索する値
    :param items: 対象のリスト
    :return: 判定結果.
    """
    for x in items:
        if not x or key_name not in x:
            continue
        if x[key_name] == value:
            return True
    return False


def get_server_id(cluster_id, server_name):
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
    server = get_object("name", server_name, consts.SERVER_NAMES)
    if not server:
        raise ValueError("サーバ名はA1-O15の値を渡してください. server_name:{}".format(server_name))
    return (cluster_id - 1) * 225 + server["id"]


def exists_server_name(server_name):
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
