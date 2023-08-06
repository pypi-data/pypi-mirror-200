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
from typing import Dict, Any, Iterable, List

from pywaclient.endpoints import Endpoint


class UserEndpoint(Endpoint):

    def __init__(self, client: 'AragornApiClient'):
        super().__init__(client)
        self.identity_path = 'identity'
        self.path = 'user'
        self.path_blocktemplates = 'user/blocktemplates'
        self.path_worlds = 'user/worlds'

    def identity(self):
        """Get the user that is associated with the authentication token provided."""
        return self._get_request(self.identity_path, {})

    def get(self, identifier: str, granularity: int) -> Dict[str, Any]:
        """Retrieve a user with their identifier.

        :param identifier:  The identifier of the user.
        :param granularity: A value between -1 and 2. Determines how much metadata is returned.
        :return:            User metadata.
        """
        return self._get_request(self.path, {'id': identifier, 'granularity': str(granularity)})

    def update(self, identifier: str, content: Dict[str, Any]) -> Dict[str, str]:
        """Update (patch) the content of a user.

        :param identifier:  The identifier of the user.
        :param content:     The fields to be updated.
        :return:            Basic user metadata.
        """
        return self._patch_request(self.path, {'id': identifier}, content)

    def block_templates(self, identifier: str) -> Iterable[Dict[str, Any]]:
        """Returns a list of all the block templates owned by this user.

        :param identifier:  The identifier of the user that the block templates should be returned from.
        :return:            An iterable of the block template entities.
        """
        return self._scroll_collection(self.path_blocktemplates, {'id': identifier}, 'entities')

    def worlds(self, identifier: str) -> Iterable[Dict[str, Any]]:
        """Returns a list of all worlds owned by this user.

        :param identifier:  The identifier of the user that the worlds should be returned from.
        :return:            An iterable of the world entities.
        """
        return self._scroll_collection(self.path_worlds, {'id': identifier}, 'entities')
