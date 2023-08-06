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


class RpgSystemEndpoint(Endpoint):

    def __init__(self, client: 'AragornApiClient'):
        super().__init__(client)
        self.path = 'rpgsystem'
        self.list_path = 'rpgsystems'

    def get(self, identifier: str, granularity: int) -> Dict[str, Any]:
        """Get the metadata of a specific rpg system.

        :param identifier:  The identifier of the article.
        :param granularity: The granularity is between -1 and 2. Determines the amount of information returned by the
                            api.
        :return:            RPG System metadata
        """
        return self._get_request(self.path, {'id': identifier, 'granularity': str(granularity)})

    def list(self, complete: bool = True, limit: int = 50, offset: int = 0) -> Iterable[Dict[str, Any]]:
        """
        List all RPG systems, filtered with a limit of entities shown and an offset.

        :param complete:    Ignore the limit and offsets and return all the entities.
        :param limit:       Determines how many RPG systems are returned. Value between 1 and 50.
        :param offset:      Determines the offset at which RPG systems are returned. Has to be a positive integer.
        :return:
        """
        if complete:
            return self._scroll_collection(self.list_path, {}, 'entities')
        assert offset >= 0
        assert 1 <= limit <= 50
        return self._post_request(self.list_path, {}, {'limit': limit, 'offset': offset})['entities']