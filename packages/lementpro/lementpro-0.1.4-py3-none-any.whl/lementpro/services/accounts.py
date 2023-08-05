#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lementpro.builders import Build
from lementpro.data.user import User
from lementpro.sender import Sender


class Accounts:
    """Service for working with accounts"""

    def login(self, by_user: User, login=None, password=None):
        """POST /api/accounts/login"""
        request_data = Build(url="/api/accounts/login").post(login=login, password=password)
        return Sender().send_request(request_data, by_user=by_user)
