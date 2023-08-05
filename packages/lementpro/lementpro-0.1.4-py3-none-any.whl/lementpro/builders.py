#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _io
from dataclasses import dataclass
from requests import Request


@dataclass
class Build:
    '''
    The Build class is a data class that allows you to construct HTTP requests to interact with the Lement Pro platform. 
    It provides several methods for constructing requests with the appropriate HTTP method, URL, and parameters.
    
    Basic usage is as follows:
    >>> from lementpro import Build
    >>> b = Build('https://example.com')
    >>> response = b.get()
    Or you can use the class methods to construct more specialized requests, such as:
    >>> response = b.post_with_file(file=open('example.txt', 'rb'), form_field_name='file')
    The Build class makes it easy to interface with the Lement Pro platform and build custom requests 
    that meet specific requirements.
    '''
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
