#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from requests import Session
from lementpro.data.user import User
from lementpro.tools.logger import logger


class Sender:

    """
    A Sender utility class for handling HTTP requests using the `requests`

Provides set of static methods for sending requests, setting user information, 
and logging request and response information.

Basic Usage:

  >>> from lementpro import Sender
  >>> response = Sender.send_request(request_data)
  <Response [200]>

Or, for custom user information:

  >>> from lementpro import Sender, User
  >>> user = User(access_token="my_access_token")
  >>> response = Sender.send_request(request_data, by_user=user)
  <Response [200]>

Also supports logging of request and response information:

  >>> Sender.logging(prepped)
  [DEBUG] sent request:
   url: http://example.com/api/v1/user/1234
   method: POST
   headers: {'Content-Type': 'application/json', 'Authorization': 'Bearer <access_token>'}
   body: {"name": "John Doe"}

  >>> Sender.logging(prepped)
  [DEBUG] received response:
   code: 200 OK
   headers: {'Content-Type': 'application/json', 'Server': 'example-server'}
   content: {"message": "Request successful."}

To use the `Sender` class, simply import it from the `lementpro` library and call its static methods
It can be used as a standalone class or in conjunction with the `User` class to set user information for requests. 
It also provides logging functionality for easy debugging of requests and responses.
    """

    @staticmethod
    def send_request(request_data, by_user=None):
        session = Sender().__set_user(by_user=by_user)
        request_data.url = by_user.root_url + request_data.url
        prepped = session.prepare_request(request_data)
        Sender.logging(prepped=prepped)
        response = session.send(request=prepped, timeout=30, verify=True)
        Sender.logging(prepped=response)
        return response

    @staticmethod
    def __set_user(by_user: User):
        session = Session()
        if by_user and by_user.access_token is not None:
            session.headers.update(
                Authorization=f'Bearer {by_user.access_token}')
        elif by_user and by_user.cookies is not None:
            session.cookies = by_user.cookies
        return session

    @staticmethod
    def logging(prepped):
        if isinstance(prepped, requests.models.PreparedRequest):
            url, method, headers, body = prepped.url, prepped.method, prepped.headers, prepped.body
            info = f"sent request:\n url: {url}\n method: {method}\n headers: {headers}\n body: {body}\n "
        else:
            headers = prepped.headers
            info = f"received response:\n code: {prepped.status_code} {prepped.reason} \n headers: {headers} \n content: {prepped.text}"
        logger.debug("len logging =%s" % str(len(info)))
        if len(info) < 10000:
            logger.debug(f'\n\n{info}')
        else:
            logger.debug("Log is too large.")
            logger.debug("Return only header = %s" % headers)
