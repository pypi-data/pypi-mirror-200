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


class BlockTemplateEndpoint(Endpoint):

    def __init__(self, client: 'AragornApiClient'):
        super().__init__(client)
        self.path = 'blocktemplate'
        self.list_path = 'blocktemplate/blocktemplateparts'

    def get(self, identifier: str, granularity: int) -> Dict[str, Any]:
        """Get the metadata of a specific block template.

        :param identifier:  The identifier of the block template.
        :param granularity: The granularity is between -1 and 2. Determines the amount of information returned by the
                            api.
        :return:            Block template metadata
        """
        return self._get_request(self.path, {'id': identifier, 'granularity': str(granularity)})

    def put(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """

        :param content:     Metadata of the new block template with at least he required fields.
        :return:            Metadata of the created block template with the id.
        """
        return self._put_request(self.path, content)

    def patch(self, identifier: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update (patch) the content of an block template.

        {
            "authornotes":"This is the first draft of this block template.",
            "prompt":{
                "id":"{{promptId}}"
            }
        }

        :param identifier:  The id of the block template to be updated.
        :param content:     All the fields that should be updated.
        :return:            Metadata of the block template.
        """
        return self._patch_request(self.path, {'id': identifier}, content)

    def delete(self, identifier: str):
        """
        Delete an block template.

        :param identifier:  The id of the block template to be deleted.
        """
        self._delete_request(self.path, {'id': identifier})

    def block_template_parts(self, block_template_id: str, complete: bool = True, limit: int = 50,
                             offset: int = 0) -> Iterable[Dict[str, Any]]:
        """
        List all parts of a block template as a list of entities.

        :param block_template_id:   The identifier of the block template.
        :param complete             Ignore limit and offset and return all the block template parts as an iterable.
        :param limit:               Determines how many articles are returned. Value between 1 and 50.
        :param offset:              Determines the offset at which articles are returned. Has to be a positive integer.
        :return:                    An iterable of block templates.
        """
        if complete:
            return self._scroll_collection(self.list_path, {'id': block_template_id }, 'entities')
        return self._post_request(self.list_path,
                                  {'id': block_template_id},
                                  {'limit': limit, 'offset': offset})['entities']
