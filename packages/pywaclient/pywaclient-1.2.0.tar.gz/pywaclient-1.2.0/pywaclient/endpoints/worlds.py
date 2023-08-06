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


class WorldEndpoint(Endpoint):

    def __init__(self, client: 'AragornApiClient'):
        super().__init__(client)
        self.path = 'world'
        self.path_categories = 'world/categories'
        self.path_block_folders = 'world/blockfolders'
        self.path_variable_collections = 'world/variablecollections'
        self.path_subscriber_groups = 'world/subscribergroups'
        self.path_secrets = 'world/secrets'
        self.path_manuscripts = 'world/manuscripts'
        self.path_maps = 'world/maps'
        self.path_images = 'world/images'
        self.path_histories = 'world/histories'
        self.path_timelines = 'world/timelines'
        self.path_chronicles = 'world/chronicles'
        self.path_canvases = 'world/canvases'
        self._path_notebooks = 'world/notebooks'

    def get(self, identifier: str, granularity: int) -> Dict[str, Any]:
        """Get the metadata of a specific world.

        :param identifier:  Identifier of the world.
        :param granularity: The level of details of the returned metadata. Is a number from -1 to 2.
        :return:            World metadata.
        """
        assert -1 <= granularity <= 2
        return self._get_request(self.path, {'id': identifier, 'granularity': str(granularity)})

    def put(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new world. Required parameters for the creation of this entity are "title".

        {
            "title": "A bright new World"
        }

        :param content:     The fields and their values with which to create the new world.
        :return:            The entity of the new world.
        """
        return self._put_request(self.path, content)

    def patch(self, identifier: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """Update (patch) the world configuration and fields.

        :param identifier:  The identifier of the world.
        :param content:     The fields and values which should be updated.
        :return:            The world entity.
        """
        return self._patch_request(self.path, {'id': identifier}, content)

    def delete(self, identifier: str):
        """
        Delete a world.

        :param identifier:  The id of the world to be deleted.
        """
        self._delete_request(self.path, {'id': identifier})

    def categories(self, world_id: str, complete: bool = True, limit: int = 50, offset: int = 0) -> Iterable[
        Dict[str, Any]]:
        """
        List all categories by a world given, filtered with a limit of entities shown and an offset.

        :param world_id:    The id of the world the folders should be returned from.
        :param complete:    Return the entire list of entities as a list. Only loads 50 categories at a time.
        :param limit:       Determines how many folders are returned. Value between 1 and 50.
        :param offset:      Determines the offset at which folders are returned. Has to be a positive integer.
        :return:
        """
        if complete:
            return self._scroll_collection(self.path_categories, {'id': world_id}, 'entities')
        return self._post_request(self.path_categories,
                                  {'id': world_id},
                                  {'limit': limit, 'offset': offset})['entities']

    def statblock_folders(self, world_id: str, complete: bool = True, limit: int = 50, offset: int = 0) -> Iterable[
        Dict[str, Any]]:
        """
        List all statblock folders of a specific world.

        :param world_id:    The id of the world
        :param complete:    Return the entire list of entities as an iterable. This ignores limit and offset when
                            set to true.
        :param limit:       The number of entries returned per request. 1 <= limit <= 50
        :param offset:      The offset in the list of entries to return from. offset >=
        :return:            An iterable of statblock folder entities.
        """
        assert 1 <= limit <= 50
        assert offset >= 0
        if complete:
            return self._scroll_collection(self.path_block_folders, {'id': world_id}, 'entities')
        return self._post_request(self.path_block_folders,
                                  {'id': world_id},
                                  {'limit': limit, 'offset': offset})['entities']

    def variable_collections(self, world_id: str, complete: bool = True, limit: int = 50, offset: int = 0) -> Iterable[
        Dict[str, Any]]:
        """
        List all variable collections of a specific world.

        :param world_id:    The id of the world
        :param complete:    Return the entire list of entities as an iterable. This ignores limit and offset when
                            set to true.
        :param limit:       The number of entries returned per request. 1 <= limit <= 50
        :param offset:      The offset in the list of entries to return from. offset >=
        :return:            An iterable of variable collection entities.
        """
        assert 1 <= limit <= 50
        assert offset >= 0
        if complete:
            return self._scroll_collection(self.path_variable_collections, {'id': world_id}, 'entities')
        return self._post_request(self.path_variable_collections,
                                  {'id': world_id},
                                  {'limit': limit, 'offset': offset})['entities']

    def subscriber_groups(self, world_id: str, complete: bool = True, limit: int = 50, offset: int = 0) -> Iterable[
        Dict[str, Any]]:
        """
        List all subscriber groups of a specific world.

        :param world_id:    The id of the world
        :param complete:    Return the entire list of entities as an iterable. This ignores limit and offset when
                            set to true.
        :param limit:       The number of entries returned per request. 1 <= limit <= 50
        :param offset:      The offset in the list of entries to return from. offset >=
        :return:            An iterable of subscriber group entities.
        """
        assert 1 <= limit <= 50
        assert offset >= 0
        if complete:
            return self._scroll_collection(self.path_subscriber_groups, {'id': world_id}, 'entities')
        return self._post_request(self.path_subscriber_groups,
                                  {'id': world_id},
                                  {'limit': limit, 'offset': offset})['entities']

    def secrets(self, world_id: str, complete: bool = True, limit: int = 50, offset: int = 0) -> Iterable[
        Dict[str, Any]]:
        """
        List all secrets of a specific world.

        :param world_id:    The id of the world
        :param complete:    Return the entire list of entities as an iterable. This ignores limit and offset when
                            set to true.
        :param limit:       The number of entries returned per request. 1 <= limit <= 50
        :param offset:      The offset in the list of entries to return from. offset >=
        :return:            An iterable of secret entities.
        """
        assert 1 <= limit <= 50
        assert offset >= 0
        if complete:
            return self._scroll_collection(self.path_secrets, {'id': world_id}, 'entities')
        return self._post_request(self.path_secrets,
                                  {'id': world_id},
                                  {'limit': limit, 'offset': offset})['entities']

    def manuscripts(self, world_id: str, complete: bool = True, limit: int = 50, offset: int = 0) -> Iterable[
        Dict[str, Any]]:
        """
        List all manuscripts of a specific world.

        :param world_id:    The id of the world
        :param complete:    Return the entire list of entities as an iterable. This ignores limit and offset when
                            set to true.
        :param limit:       The number of entries returned per request. 1 <= limit <= 50
        :param offset:      The offset in the list of entries to return from. offset >=
        :return:            An iterable of manuscript entities.
        """
        assert 1 <= limit <= 50
        assert offset >= 0
        if complete:
            return self._scroll_collection(self.path_manuscripts, {'id': world_id}, 'entities')
        return self._post_request(self.path_manuscripts,
                                  {'id': world_id},
                                  {'limit': limit, 'offset': offset})['entities']

    def maps(self, world_id: str, complete: bool = True, limit: int = 50, offset: int = 0) -> Iterable[
        Dict[str, Any]]:
        """
        List all maps of a specific world.

        :param world_id:    The id of the world
        :param complete:    Return the entire list of entities as an iterable. This ignores limit and offset when
                            set to true.
        :param limit:       The number of entries returned per request. 1 <= limit <= 50
        :param offset:      The offset in the list of entries to return from. offset >=
        :return:            An iterable of map entities.
        """
        assert 1 <= limit <= 50
        assert offset >= 0
        if complete:
            return self._scroll_collection(self.path_maps, {'id': world_id}, 'entities')
        return self._post_request(self.path_maps,
                                  {'id': world_id},
                                  {'limit': limit, 'offset': offset})['entities']

    def images(self, world_id: str, complete: bool = True, limit: int = 50, offset: int = 0) -> Iterable[
        Dict[str, Any]]:
        """
        List all images of a specific world.

        :param world_id:    The id of the world
        :param complete:    Return the entire list of entities as an iterable. This ignores limit and offset when
                            set to true.
        :param limit:       The number of entries returned per request. 1 <= limit <= 50
        :param offset:      The offset in the list of entries to return from. offset >=
        :return:            An iterable of image entities.
        """
        assert 1 <= limit <= 50
        assert offset >= 0
        if complete:
            return self._scroll_collection(self.path_images, {'id': world_id}, 'entities')
        return self._post_request(self.path_images,
                                  {'id': world_id},
                                  {'limit': limit, 'offset': offset})['entities']

    def histories(self, world_id: str, complete: bool = True, limit: int = 50, offset: int = 0) -> Iterable[
        Dict[str, Any]]:
        """
        List all histories of a specific world.

        :param world_id:    The id of the world
        :param complete:    Return the entire list of entities as an iterable. This ignores limit and offset when
                            set to true.
        :param limit:       The number of entries returned per request. 1 <= limit <= 50
        :param offset:      The offset in the list of entries to return from. offset >=
        :return:            An iterable of history entities.
        """
        assert 1 <= limit <= 50
        assert offset >= 0
        if complete:
            return self._scroll_collection(self.path_histories, {'id': world_id}, 'entities')
        return self._post_request(self.path_histories,
                                  {'id': world_id},
                                  {'limit': limit, 'offset': offset})['entities']

    def timelines(self, world_id: str, complete: bool = True, limit: int = 50, offset: int = 0) -> Iterable[
        Dict[str, Any]]:
        """
        List all timelines of a specific world.

        :param world_id:    The id of the world
        :param complete:    Return the entire list of entities as an iterable. This ignores limit and offset when
                            set to true.
        :param limit:       The number of entries returned per request. 1 <= limit <= 50
        :param offset:      The offset in the list of entries to return from. offset >=
        :return:            An iterable of timeline entities.
        """
        assert 1 <= limit <= 50
        assert offset >= 0
        if complete:
            return self._scroll_collection(self.path_timelines, {'id': world_id}, 'entities')
        return self._post_request(self.path_timelines,
                                  {'id': world_id},
                                  {'limit': limit, 'offset': offset})['entities']

    def chronicles(self, world_id: str, complete: bool = True, limit: int = 50, offset: int = 0) -> Iterable[
        Dict[str, Any]]:
        """
        List all chronicles of a specific world.

        :param world_id:    The id of the world
        :param complete:    Return the entire list of entities as an iterable. This ignores limit and offset when
                            set to true.
        :param limit:       The number of entries returned per request. 1 <= limit <= 50
        :param offset:      The offset in the list of entries to return from. offset >=
        :return:            An iterable of chronicle entities.
        """
        assert 1 <= limit <= 50
        assert offset >= 0
        if complete:
            return self._scroll_collection(self.path_chronicles, {'id': world_id}, 'entities')
        return self._post_request(self.path_chronicles,
                                  {'id': world_id},
                                  {'limit': limit, 'offset': offset})['entities']

    def canvases(self, world_id: str, complete: bool = True, limit: int = 50, offset: int = 0) -> Iterable[
        Dict[str, Any]]:
        """
        List all canvases of a specific world.

        :param world_id:    The id of the world
        :param complete:    Return the entire list of entities as an iterable. This ignores limit and offset when
                            set to true.
        :param limit:       The number of entries returned per request. 1 <= limit <= 50
        :param offset:      The offset in the list of entries to return from. offset >=
        :return:            An iterable of canvas entities.
        """
        assert 1 <= limit <= 50
        assert offset >= 0
        if complete:
            return self._scroll_collection(self.path_canvases, {'id': world_id}, 'entities')
        return self._post_request(self.path_canvases,
                                  {'id': world_id},
                                  {'limit': limit, 'offset': offset})['entities']


    def notebooks(self, identifier: str) -> Iterable[Dict[str, Any]]:
        """Returns a list of all worlds owned by this user.

        :param identifier:  The identifier of the user that the worlds should be returned from.
        :return:            An iterable of the world entities.
        """
        return self._scroll_collection(self._path_notebooks, {'id': identifier}, 'entities')
