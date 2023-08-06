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


class MapMarkerGroupEndpoint(Endpoint):

    def __init__(self, client: 'AragornApiClient'):
        super().__init__(client)
        self.path = 'markergroup'
        self.path_markers = 'markergroup/markers'

    def get(self, identifier: str, granularity: int) -> Dict[str, Any]:
        """Get the metadata of a specific map marker groups.

        :param identifier:  The identifier of the map marker groups.
        :param granularity: The granularity is between -1 and 2. Determines the amount of information returned by the
                            api.
        :return:            Map marker groups metadata
        """
        return self._get_request(self.path, {'id': identifier, 'granularity': str(granularity)})

    def put(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new map marker groups. Required parameters for the creation of this entity are "title" and "world.id".

        {
            "title": "Town Map marker groups",
            "world": {
                "id":"{{worldId}}"
            }
        }

        :param content:     Metadata of the new map marker groups with at least he required fields.
        :return:            Metadata of the created map marker groups with the id.
        """
        return self._put_request(self.path, content)

    def patch(self, identifier: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update (patch) the content of a map marker groups.

        :param identifier:  The id of the map marker groups to be updated.
        :param content:     All the fields that should be updated.
        :return:            Metadata of the map marker groups.
        """
        return self._patch_request(self.path, {'id': identifier}, content)

    def delete(self, identifier: str):
        """
        Delete a map marker groups.

        :param identifier:  The id of the map marker groups to be deleted.
        """
        self._delete_request(self.path, {'id': identifier})


    def markers(self, map_maker_group_id: str) -> Iterable[Dict[str, Any]]:
        """
        List the markers of a specific group.

        :param map_maker_group_id:      The id of the group.
        :return:            Iterable of all layers.
        """
        return self._scroll_collection(self.path_markers, {'id': map_maker_group_id}, 'entities')