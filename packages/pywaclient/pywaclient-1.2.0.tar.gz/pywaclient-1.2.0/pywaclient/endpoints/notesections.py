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


class NoteSectionEndpoint(Endpoint):

    def __init__(self, client: 'AragornApiClient'):
        super().__init__(client)
        self.path = 'notesection'
        self.list_path = 'notesection/notes'

    def get(self, identifier: str, granularity: int) -> Dict[str, Any]:
        """Get the metadata of a specific notesections.

        :param identifier:  The identifier of the notesections.
        :param granularity: The granularity is between -1 and 2. Determines the amount of information returned by the
                            api.
        :return:            Notesections metadata
        """
        return self._get_request(self.path, {'id': identifier, 'granularity': str(granularity)})

    def put(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new notesections. Required parameters for the creation of this entity is "title" and "notebook.id".

        :param content:     Metadata of the new notesections with at least he required fields.
        :return:            Metadata of the created notesections with the id.
        """
        return self._put_request(self.path, content)

    def patch(self, identifier: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update (patch) the content of a notesections.

        :param identifier:  The id of the notesections to be updated.
        :param content:     All the fields that should be updated.
        :return:            Metadata of the notesections.
        """
        return self._patch_request(self.path, {'id': identifier}, content)

    def delete(self, identifier: str):
        """
        Delete a notesections.

        :param identifier:  The id of the notesections to be deleted.
        """
        self._delete_request(self.path, {'id': identifier})

    def notes(self, note_section_id: str, complete: bool = True, limit: int = 50, offset: int = 0) -> Iterable[Dict[str, Any]]:
        """
        Retrieve an iterable of all the note references within one section.

        :param note_section_id: The id of the parent note section.
        :param complete:        Ignore the limit and offsets and return all the entities.
        :param limit:           The number of returned references between 1 and 50.
        :param offset:          The offset in the returned list.
        :return:
        """
        if complete:
            return self._scroll_collection(self.list_path, {'id': note_section_id}, 'entities')
        assert offset >= 0
        assert 1 <= limit <= 50
        return self._post_request(self.list_path, {'id': note_section_id}, {'limit': limit, 'offset': offset})['entities']