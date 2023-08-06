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
from typing import Dict, Any, Iterable

from pywaclient.endpoints import Endpoint


class MapMarkerTypeEndpoint(Endpoint):

    def __init__(self, client: 'AragornApiClient'):
        super().__init__(client)
        self.path = 'markertype'
        self.path_list = 'markertypes'

    def get(self, identifier: str, granularity: int) -> Dict[str, Any]:
        """Get the metadata of a specific map marker type.

        :param identifier:  The identifier of the map marker type.
        :param granularity: The granularity is between -1 and 2. Determines the amount of information returned by the
                            api.
        :return:            Map marker type metadata
        """
        return self._get_request(self.path, {'id': identifier, 'granularity': str(granularity)})

    def put(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new map marker type. Required parameters for the creation of this entity are "title" and "world.id".

        {
            "title": "Town Map marker type",
            "world": {
                "id":"{{worldId}}"
            }
        }

        :param content:     Metadata of the new map marker type with at least he required fields.
        :return:            Metadata of the created map marker type with the id.
        """
        return self._put_request(self.path, content)

    def patch(self, identifier: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update (patch) the content of a map marker type.

        :param identifier:  The id of the map marker type to be updated.
        :param content:     All the fields that should be updated.
        :return:            Metadata of the map marker type.
        """
        return self._patch_request(self.path, {'id': identifier}, content)

    def delete(self, identifier: str):
        """
        Delete a map marker type.

        :param identifier:  The id of the map marker type to be deleted.
        """
        self._delete_request(self.path, {'id': identifier})

    def list(self, complete: bool = True, limit: int = 50, offset: int = 0) -> Iterable[
        Dict[str, Any]]:
        """
        List all marker types available.

        :param complete:    Return the entire list of entities as an iterable. This ignores limit and offset when
                            set to true.
        :param limit:       The number of entries returned per request. 1 <= limit <= 50
        :param offset:      The offset in the list of entries to return from. offset >=
        :return:            An iterable of marker types.
        """
        assert 1 <= limit <= 50
        assert offset >= 0
        if complete:
            return self._scroll_collection(self.path_list, {}, 'entities')
        return self._post_request(self.path_list,
                                  {},
                                  {'limit': limit, 'offset': offset})['entities']
