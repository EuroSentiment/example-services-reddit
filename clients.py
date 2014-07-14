#!/usr/bin/python
# -*- coding: utf-8 -*-
#    Copyright 2014 J. Fernando Sánchez Rada - Grupo de Sistemas Inteligentes
#                                                       DIT, UPM
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
'''
Wrappers around the EUROSENTIMENT APIs.
'''

import json
import requests

class ServiceClient():

    def __init__(self, token, endpoint):
        self.endpoint = endpoint
        self.token = token

    def request(self, **kwargs):
        headers = {'x-eurosentiment-token': self.token}
        response = requests.post(self.endpoint,
                                 data=kwargs,
                                 headers=headers)
        return json.loads(response.content)
