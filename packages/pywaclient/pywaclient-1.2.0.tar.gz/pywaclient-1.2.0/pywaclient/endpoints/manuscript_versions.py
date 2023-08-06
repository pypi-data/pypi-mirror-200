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
from pywaclient.endpoints.manuscript_stats import ManuscriptStatEndpoint
from pywaclient.endpoints.manuscript_plots import ManuscriptPlotEndpoint
from pywaclient.endpoints.manuscript_parts import ManuscriptPartEndpoint


class ManuscriptVersionEndpoint(Endpoint):

    def __init__(self, client: 'AragornApiClient'):
        super().__init__(client)
        self._path = 'manuscript_version'
        self.part = ManuscriptPartEndpoint(client)
        self._path_parts = 'manuscript_parts'
        self.plot = ManuscriptPlotEndpoint(client)
        self._path_plots = 'manuscript_plots'
        self.stat = ManuscriptStatEndpoint(client)
        self._path_stats = 'manuscript_stats'

    def get(self, identifier: str, granularity: int) -> Dict[str, Any]:
        """Get the metadata of a specific entity

        :param identifier:  The identifier of the entity
        :param granularity: Determines the amount of metadata returned.
        :return:            A json object of the metadata or an error.
        """
        return self._get_request(self._path, {'id': identifier, 'granularity': str(granularity)})

    def put(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new entity with the given content.

        :param content:     An object with at least the required fields of the entity.
        :return:            The reference object of the created entity.
        """
        return self._put_request(self._path, content)

    def patch(self, identifier: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """Update the one or more fields of the entity.

        :param identifier:  The identifier of the target entity.
        :param content:     A dictionary with the fields that should be updated.
        :return:            The reference object of the updated entity.
        """
        return self._patch_request(self._path, {'id': identifier}, content)

    def delete(self, identifier: str):
        """Delete the entity.

        :param identifier:  The identifier of the entity to delete.
        """
        self._delete_request(self._path, {'id': identifier})

    def parts(self, identifier: str) -> Iterable[Dict[str, Any]]:
        """Retrieve an iterable of all the parts of a manuscript version.

        :param identifier:  Identifier of the manuscript version.
        :return:            Iterable dictionary of the entities.
        """
        return self._scroll_collection(self._path_parts, {'id': identifier}, 'entities')

    def plots(self, identifier: str) -> Iterable[Dict[str, Any]]:
        """Retrieve an iterable of all the plots of a manuscript version.

        :param identifier:  Identifier of the manuscript version.
        :return:            Iterable dictionary of the entities.
        """
        return self._scroll_collection(self._path_plots, {'id': identifier}, 'entities')

    def stats(self, identifier: str) -> Iterable[Dict[str, Any]]:
        """Retrieve an iterable of all the stats of a manuscript version.

        :param identifier:  Identifier of the manuscript version.
        :return:            Iterable dictionary of the entities.
        """
        return self._scroll_collection(self._path_stats, {'id': identifier}, 'entities')