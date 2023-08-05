#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _io
from dataclasses import dataclass
from requests import Request


@dataclass
class Build:
    url: str

    def post(self, **kwargs):
        return Request(method="post", url=self.url, json=kwargs)

    def post_with_file(self, file: _io.BufferedReader, form_field_name: str, **kwargs):
        file = {form_field_name: file}
        return Request(method="post", url=self.url, data=kwargs, files=file)

    def get(self, **kwargs):
        return Request(method="get", url=self.url, json=kwargs)

    def get_with_params(self, **kwargs):
        return Request(method="get", url=self.url, params=kwargs)

    def get_with_param_in_url(self, arg):
        return Request(method="get", url=self.url.format(str(arg)))

    def delete_with_param_in_url(self, arg):
        return Request(method="delete", url=self.url.format(str(arg)))
