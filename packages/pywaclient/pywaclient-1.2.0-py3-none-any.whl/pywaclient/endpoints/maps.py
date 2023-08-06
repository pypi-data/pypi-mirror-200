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


class MapEndpoint(Endpoint):

    def __init__(self, client: 'AragornApiClient'):
        super().__init__(client)
        self.path = 'map'
        self.path_layers = 'map/layers'
        self.path_groups = 'map/markergroups'

    def get(self, identifier: str, granularity: int) -> Dict[str, Any]:
        """Get the metadata of a specific map.

        :param identifier:  The identifier of the map.
        :param granularity: The granularity is between -1 and 2. Determines the amount of information returned by the
                            api.
        :return:            Map metadata
        """
        return self._get_request(self.path, {'id': identifier, 'granularity': str(granularity)})

    def put(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new map. Required parameters for the creation of this entity are "title" and "world.id".

        {
            "title": "Town Map",
            "world": {
                "id":"{{worldId}}"
            }
        }

        :param content:     Metadata of the new map with at least he required fields.
        :return:            Metadata of the created map with the id.
        """
        return self._put_request(self.path, content)

    def patch(self, identifier: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update (patch) the content of a map.

        :param identifier:  The id of the map to be updated.
        :param content:     All the fields that should be updated.
        :return:            Metadata of the map.
        """
        return self._patch_request(self.path, {'id': identifier}, content)

    def delete(self, identifier: str):
        """
        Delete a map.

        :param identifier:  The id of the map to be deleted.
        """
        self._delete_request(self.path, {'id': identifier})

    def marker_groups(self, map_id: str) -> Iterable[Dict[str, Any]]:
        """
        List the marker groups of a specific map.

        :param map_id:      The id of the map.
        :return:            Iterable of all marker groups.
        """
        return self._scroll_collection(self.path_groups, {'id': map_id}, 'entities')

    def layers(self, map_id: str) -> Iterable[Dict[str, Any]]:
        """
        List the layers of a specific map.

        :param map_id:      The id of the map.
        :return:            Iterable of all layers.
        """
        return self._scroll_collection(self.path_layers, {'id': map_id}, 'entities')
