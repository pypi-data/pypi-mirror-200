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


class VariableCollectionEndpoint(Endpoint):

    def __init__(self, client: 'AragornApiClient'):
        super().__init__(client)
        self.path = 'variablecollection'
        self.path_variables = f"{self.path}/variables"

    def get(self, identifier: str, granularity: int) -> Dict[str, Any]:
        """Get the metadata of a specific variable collection.

        :param identifier:  The identifier of the variable collection.
        :param granularity: The granularity is between -1 and 2. Determines the amount of information returned by the
                            api.
        :return:            VariableCollection metadata
        """
        return self._get_request(self.path, {'id': identifier, 'granularity': str(granularity)})

    def put(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new variable collection. Required parameters for the creation of this entity are "title" and "world".

        {
            "title":"Variables Collection",
            "description":"All variables used in this world.",
            "world":"{{worldId}}",
            "prefix":"1",
            "state":"public"
        }

        :param content:     Metadata of the new variable collection with at least he required fields.
        :return:            Metadata of the created variable collection with the id.
        """
        return self._put_request(self.path, content)

    def patch(self, identifier: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update (patch) the content of a variable collection.

        :param identifier:  The id of the variable collection to be updated.
        :param content:     All the fields that should be updated.
        :return:            Metadata of the variable collection.
        """
        return self._patch_request(self.path, {'id': identifier}, content)

    def delete(self, identifier: str):
        """
        Delete a variable collection.

        :param identifier:  The id of the variable collection to be deleted.
        """
        self._delete_request(self.path, {'id': identifier})

    def variables(self, world_id: str, variable_collection_id: str, complete: bool = True, limit: int = 50, offset: int = 0) -> Iterable[Dict[str, Any]]:
        """
        List all variables by a category given, filtered with a limit of entities shown and an offset.

        :param world_id:                The id of the world the variables should be returned from.
        :param variable_collection_id:  The id of the variable collection to return the variables from.
        :param complete                 Ignore limit and offset and return all the variables as an iterable. Will fetch a new batch
                                        every 50 variables.
        :param limit:                   Determines how many variables are returned. Value between 1 and 50.
        :param offset:                  Determines the offset at which variables are returned. Has to be a positive integer.
        :return:
        """
        if complete:
            return self._scroll_collection(self.path_variables, {'id': world_id}, 'entities', 'variableCollection', variable_collection_id)
        return self._post_request(self.path_variables,
                                  {'id': world_id},
                                  {'limit': limit, 'offset': offset, 'variableCollection': {'id': variable_collection_id}})['entities']
