#    Copyright 2020 Jonas Waeber
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
from typing import Dict, Any

from pywaclient.endpoints import Endpoint


class HistoryEndpoint(Endpoint):

    def __init__(self, client: 'AragornApiClient'):
        super().__init__(client)
        self.path = 'history'

    def get(self, identifier: str, granularity: int) -> Dict[str, Any]:
        """Get the metadata of a specific history.

        :param identifier:  The identifier of the history.
        :param granularity: The granularity is between -1 and 2. Determines the amount of information returned by the
                            api.
        :return:            History metadata
        """
        return self._get_request(self.path, {'id': identifier, 'granularity': str(granularity)})

    def put(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new history. Required parameters for the creation of this entity are "title", "templateType" and "world".

        {
            "title":"History Title",
            "templateType":"history",
            "world":{
                "id": "{{worldId}}"
            }
        }

        :param content:     Metadata of the new history with at least he required fields.
        :return:            Metadata of the created history with the id.
        """
        return self._put_request(self.path, content)

    def patch(self, identifier: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update (patch) the content of an history.

        {
            "authornotes":"This is the first draft of this history.",
            "prompt":{
                "id":"{{promptId}}"
            }
        }

        :param identifier:  The id of the history to be updated.
        :param content:     All the fields that should be updated.
        :return:            Metadata of the history.
        """
        return self._patch_request(self.path, {'id': identifier}, content)

    def delete(self, identifier: str):
        """
        Delete an history.

        :param identifier:  The id of the history to be deleted.
        """
        self._delete_request(self.path, {'id': identifier})
