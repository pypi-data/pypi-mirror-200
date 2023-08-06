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


class SubscriberGroupEndpoint(Endpoint):

    def __init__(self, client: 'AragornApiClient'):
        super().__init__(client)
        self.path = 'subscribergroup'

    def get(self, identifier: str, granularity: int) -> Dict[str, Any]:
        """Get the metadata of a specific subscriber group.

        :param identifier:  The identifier of the subscriber group.
        :param granularity: The granularity is between -1 and 2. Determines the amount of
                                information returned by the api.
        :return:            VariableCollection metadata
        """
        return self._get_request(self.path, {'id': identifier, 'granularity': str(granularity)})

    def put(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new subscriber group . Required parameters for the creation of this entity are "title" and "world.id".

        {
            "title": "Campaign Players",
            "world": {
                "id":"{{worldId}}"
            }
        }

        :param content:     Metadata of the new subscriber group  with at least he required fields.
        :return:            Metadata of the created subscriber group  with the id.
        """
        return self._put_request(self.path, content)

    def patch(self, identifier: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update (patch) the content of a subscriber group.

        {
            "isDefault": false,
            "isHidden": true,
            "isAssignable": false
        }

        :param identifier:  The id of the subscriber group to be updated.
        :param content:     All the fields that should be updated.
        :return:            Metadata of the subscriber group.
        """
        return self._patch_request(self.path, {'id': identifier}, content)

    def delete(self, identifier: str):
        """
        Delete a subscriber group.

        :param identifier:  The id of the subscriber group to be deleted.
        """
        self._delete_request(self.path, {'id': identifier})
