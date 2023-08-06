import asyncio
import json
import logging
import socket
import ssl
import time
import urllib.parse
from typing import List, Dict



class Yumikogram:
    """
    A class for interacting with Telegram Bot API using asyncio.
    Parameters:
        bot_token (str): The token of the Telegram bot.
        api_id (int): The API ID for the bot.
        api_hash (str): The API hash for the bot.
        string_session (Optional[str]): The string session used for user authorization.
    Attributes:
        server (str): The URL of the Telegram API server.
        port (int): The port of the Telegram API server.
        ssl_context (ssl.SSLContext): The SSL context for making secure connections.
        last_update_id (int): The ID of the last received update from the API.
    """

    def __init__(self, bot_token: str, api_id: int, api_hash: str, string_session: Optional[str] = None):
        """
        Initializes a new Yumikogram object with the specified bot token, API ID, and API hash.
        Args:
            bot_token (str): The token of the Telegram bot.
            api_id (int): The API ID for the bot.
            api_hash (str): The API hash for the bot.
            string_session (Optional[str]): The string session used for user authorization.
        """
        self.bot_token = bot_token
        self.api_id = api_id
        self.api_hash = api_hash
        self.server = 'api.telegram.org'
        self.port = 443
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        self.last_update_id = None
        self.string_session = string_session

    async def send_message(self, chat_id: int, text: str, **kwargs) -> Dict:
        """
        Sends a message to a chat.

        Args:
            chat_id (int): The ID of the chat to send the message to.
            text (str): The text of the message.
            **kwargs: Optional arguments to pass to the Telegram Bot API.

        Returns:
            Dict: The response from the Telegram Bot API as a dictionary.
        """
        url = f'https://{self.server}:{self.port}/bot{self.bot_token}/sendMessage'
        data = {'chat_id': chat_id, 'text': text}
        data.update(kwargs)
        response = await self._send_request(url, data)
        return response.get('result', {})

    async def get_updates(self, **kwargs) -> List[Dict]:
        """
        Gets the latest updates from the Telegram Bot API.

        Args:
            **kwargs: Optional arguments to pass to the Telegram Bot API.

        Returns:
            List[Dict]: A list of updates as dictionaries.
        """
        url = f'https://{self.server}:{self.port}/bot{self.bot_token}/getUpdates'
        data = {'timeout': 60}
        if self.last_update_id:
            data['offset'] = self.last_update_id + 1
        data.update(kwargs)
        response = await self._send_request(url, data)
        updates = response.get('result', [])
        for update in updates:
            self.last_update_id = update['update_id']
        return updates

    async def _send_request(self, url: str, data: Dict) -> Dict:
        """
        Sends a request to the Telegram Bot API.

        Args:
            url (str): The URL of the Telegram Bot API endpoint.
            data (Dict): The data to send to the Telegram Bot API.

        Returns:
            Dict: The response from the Telegram Bot API as a dictionary.
        """
        encoded_data = json.dumps(data).encode('utf-8')
        headers = {
            'Content-Type': 'application/json
        }
    try:
        async with asyncio.open_connection(self.server, self.port, ssl=self.ssl_context) as conn:
            request = (f'POST {url} HTTP/1.1\r\n'
                       f'Host: {self.server}\r\n'
                       f'Content-Length: {len(encoded_data)}\r\n'
                       f'Connection: close\r\n\r\n').encode('utf-8') + encoded_data
            conn.write(request)
            response = await conn.read()
    except (socket.gaierror, socket.error) as e:
        logging.error(f'Error connecting to Telegram API: {e}')
        return {}
    try:
        response = response.decode('utf-8')
        headers, body = response.split('\r\n\r\n', 1)
        status_code = int(headers.split()[1])
        if status_code != 200:
            logging.error(f'Request failed with status code {status_code}: {body}')
            return {}
        return json.loads(body)
    except Exception as e:
        logging.error(f'Error parsing response from Telegram API: {e}')
        return {}

async def get_dialogs(self) -> List[Dict]:
    """
    Gets the list of dialogs for the authorized user.
    Returns:
        List[Dict]: A list of dialogs as dictionaries.
    """
    if not self.string_session:
        raise ValueError('No string session provided for user authorization.')
    url = f'https://{self.server}:{self.port}/user/get_dialogs'
    data = {'session_string': self.string_session}
    response = await self._send_request(url, data)
    return response.get('dialogs', [])
