import time, json, logging, threading, re, io
from .logger import set_logging
from weixin_client_python import WeixinHelper
from typing import Callable, Tuple, Union, List
from enum import Enum
import xmltodict
from pyqrcode import QRCode

logger = logging.getLogger('weixin')


class MsgType(Enum):
    TEXT = 0x01
    PICTURE = 0x03
    VOICE = 0x22
    CARD = 0x2A
    ARTICLE = 0x1F
    SYSTEM = 0x2710


class TryAgain(RuntimeError): ...


class Message(dict):
    """
    消息
    """

    @property
    def type(self) -> MsgType:
        """
        消息类型
        """
        return MsgType(int(self.get("type"), 16))

    @property
    def wxid(self) -> str:
        """
        消息所在聊天ID
        """
        return self.get("wxid")

    @property
    def sender(self) -> str:
        """
        消息发送者的ID
        """
        return self.get("sender")

    @property
    def source(self) -> str:
        """
        消息xml源
        """
        return self.get("source")

    @property
    def content(self) -> str:
        """
        消息内容
        """
        return self.get("content")


class Profile(dict):
    """
    当前登录微信账号信息
    """

    @property
    def wxid(self) -> str:
        """
        微信ID
        """
        return self.get("wxid")

    @property
    def wxnum(self) -> str:
        """
        微信号
        """
        return self.get("wxnum")

    @property
    def nickname(self) -> str:
        """
        微信昵称
        """
        return self.get("nickname")

    @property
    def big_avatar(self) -> str:
        """
        微信大头像
        """
        return self.get("big_avatar")

    @property
    def small_avatar(self) -> str:
        """
        微信小头像
        """
        return self.get("small_avatar")

    @property
    def phone_number(self) -> str:
        """
        微信号绑定电话
        """
        return self.get("phone_number")


class Contact(dict):
    """
    联系人信息
    """

    @property
    def wxid(self) -> str:
        """
        微信ID
        """
        return self.get("wxid")

    @property
    def wxnum(self) -> str:
        """
        微信号
        """
        return self.get("wxnum")

    @property
    def nickname(self) -> str:
        """
        微信昵称
        """
        return self.get("nickname")

    @property
    def remark(self) -> str:
        """
        备注
        """
        return self.get("remark")


class WeixinClient:

    def __init__(self, ip="127.0.0.1", port1=10086, port2=10010):
        self._ip = ip
        self._port1 = port1
        self._port2 = port2
        self._helper = None
        self._running = False
        self._logging = False
        self._func_dict = dict()

    @property
    def helper(self):
        if self._helper is None:
            self._helper = WeixinHelper(self._ip, self._port1, self._port2)

        return self._helper

    def _check_login(self):
        if not self.helper.IsLogin():
            raise RuntimeError("not login!")

    def send_text(self, wxid: str, text: str):
        self._check_login()
        self.helper.SendText(wxid, text)

    def send_image(self, wxid: str, path: str):
        """
        发送图片消息
        :param wxid: 发送用户
        :param path: 图片路径
        :return:
        """
        self._check_login()
        logger.debug("send_image wxid:%s, path:%s", wxid, path)
        self.helper.SendImage(wxid, path)

    def send_file(self, wxid: str, path: str):
        """
        发送文件消息
        :param wxid: 发送用户
        :param path: 文件路径
        :return:
        """
        self._check_login()
        logger.debug("send_file wxid:%s, path:%s", wxid, path)
        self.helper.SendFile(wxid, path)

    def send_at_text(self, wxid: str, text: str, at_wxid: [str]):
        """
        群聊中发送at消息
        :param wxid: 发送用户
        :param text: 发送内容
        :param at_wxid: At用户列表
        :return:
        """
        self._check_login()
        logger.debug("send_at_text wxid:%s, text:%s, at_wxid:%s", wxid, text, at_wxid)
        self.helper.SendAtText(wxid, at_wxid, text)

    def send_card(self, wxid: str, share_wxid: str):
        """
        发送名片消息
        :param wxid: 发送用户
        :param share_wxid: 分享的用户
        :return:
        """
        self._check_login()
        logger.debug("send_card wxid:%s, share_wxid:%s", wxid, share_wxid)
        self.helper.SendCard(wxid, share_wxid)

    def send_link(self, wxid: str, title: str, description: str, url: str):
        """
        发送链接消息
        :param wxid: 发送用户
        :param title: 链接标题
        :param description: 链接描述
        :param url: 链接地址
        :return:
        """
        self._check_login()
        logger.debug("send_link wxid:%s, title:%s, description: %s, url: %s", wxid, title, description, url)
        self.helper.SendLink(wxid, title, description, url)

    def get_profile(self) -> Profile:
        """
        获取登录用户信息
        Returns:
            登录用户信息
        """
        self._check_login()
        profile = self.helper.GetProfile()
        return Profile({
            "wxid": profile.wxid,
            "wxnum": profile.wxnum,
            "nickname": profile.nickname,
            "big_avatar": profile.big_avatar,
            "small_avatar": profile.small_avatar,
            "phone_number": profile.phone_number
        })

    def get_contact_list(self) -> List[Contact]:
        self._check_login()
        contact_list = self.helper.GetContactList()
        return [Contact({
            "wxid": contact.wxid,
            "wxnum": contact.wxnum,
            "nickname": contact.nickname,
            "remark": contact.remark,
        }) for contact in contact_list]

    def get_contact(self, wxid: str) -> Contact:
        self._check_login()
        contact = self.helper.GetContact(wxid)
        return Contact({
            "wxid": contact.wxid,
            "wxnum": contact.wxnum,
            "nickname": contact.nickname,
            "remark": contact.remark,
        })

    def get_chatroom_member(self, wxid: str):
        self._check_login()
        return self.helper.GetChatRoomMember(wxid)

    def login(self, cb: Callable[[str, bytes], None] = None, enable_cmd_qrcode=True) -> Profile:
        if self.helper.IsLogin():
            return self.get_profile()
        self._logging = True
        last_uuid = None
        while self._logging and not self.helper.IsLogin():
            curr_uuid = self.helper.GetQRCode()

            if curr_uuid is None or len(curr_uuid) == 0:
                self.helper.ShowQRCode()
            elif last_uuid != curr_uuid:
                last_uuid = curr_uuid
                storage = io.BytesIO()
                qrcode = QRCode("http://weixin.qq.com/x/%s" % curr_uuid)
                qrcode.png(storage, scale=10)
                if cb is not None:
                    cb(curr_uuid, storage.getvalue())
                else:
                    if enable_cmd_qrcode:
                        print(qrcode.terminal())

            time.sleep(1)
        self._logging = False
        return self.get_profile()

    def message(self, wxid: str = None, msgtype: Union[MsgType, List[MsgType], Tuple[MsgType]] = None,
                keywords: Union[str, List[str], Tuple[str]] = None,
                at_users: Union[str, List[str], Tuple[str]] = None):

        endpoint = "chat/%s" % wxid if wxid is not None else "chat"

        if msgtype and not (isinstance(msgtype, list) or isinstance(msgtype, tuple)):
            msgtype = [msgtype]

        if keywords and not (isinstance(keywords, list) or isinstance(keywords, tuple)):
            keywords = [keywords]

        if at_users and not (isinstance(at_users, list) or isinstance(at_users, tuple)):
            at_users = [at_users]

        def register(func: Callable[[Message], None]):
            if endpoint not in self._func_dict:
                self._func_dict[endpoint] = []

            def func_proxy(payload):
                message = Message(payload)

                if msgtype and len(msgtype) and message.type not in msgtype:
                    return

                if keywords and len(keywords) and message.content:
                    flag = True

                    for keyword in keywords:
                        if re.search(keyword, message.content):
                            flag = False

                    if flag:
                        return

                if at_users and len(at_users) and message.source:
                    source = xmltodict.parse(message.source)
                    if not source or "msgsource" not in source or "atuserlist" not in source["msgsource"]:
                        return

                    flag = True
                    for item in at_users:
                        if source["msgsource"]["atuserlist"] and item in source["msgsource"]["atuserlist"]:
                            flag = False
                    if flag:
                        return

                func(message)

            self._func_dict[endpoint].append(func_proxy)
            return func_proxy

        return register

    def receive_message(self):
        message = self.helper.ReceiveMessage(1)
        if message and ":" in message:
            logger.debug("receive_message:%s", message)
            topic, payload = message.split(":", 1)
            return topic, json.loads(payload)
        raise TryAgain

    def terminate(self):
        self._running = False

    def run_forever(self, debug=False, block=True):
        def main_loop():
            if debug:
                set_logging(loggingLevel=logging.DEBUG)

            logger.info("start receive message...")
            self.helper.Subscribe("")
            self._running = True
            while self._running:
                try:
                    topic, payload = self.receive_message()
                    for endpoint in self._func_dict:
                        if re.match(endpoint, topic):
                            callback_func = self._func_dict[endpoint]
                            for func in callback_func:
                                func(payload)
                except TryAgain:
                    continue
                except KeyboardInterrupt:
                    logger.debug('received ^C and exit.')
                    logger.info('Bye~')
                    break
            self._running = False
            self.helper.UnSubscribe("")

        if block:
            main_loop()
        else:
            thread = threading.Thread(target=main_loop)
            thread.setDaemon(True)
            thread.start()
