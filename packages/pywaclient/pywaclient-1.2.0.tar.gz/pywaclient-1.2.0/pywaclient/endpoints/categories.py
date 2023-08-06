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


class CategoryEndpoint(Endpoint):

    def __init__(self, client: 'AragornApiClient'):
        super().__init__(client)
        self.path = 'category'
        self.path_articles = 'category/articles'

    def get(self, identifier: str, granularity: int) -> Dict:
        """Get the metadata of a specific category.

        :param identifier:  The identifier of the category.
        :param granularity: The granularity is between -1 and 2. Determines the amount of information returned by the
                            api.
        :return:            Category metadata
        """
        return self._get_request(self.path, {'id': identifier, 'granularity': str(granularity)})

    def put(self, content: Dict[str, Any]) -> Dict:
        """Create a new category. Required parameters for the creation of this entity are "title" and "world".

        :param content:     The content to create the category.
        :return:            Category metadata
        """
        return self._put_request(self.path, content)

    def patch(self, identifier: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update (patch) the content of a category.

        {
            "state":"private",
            "bookcover":{
                "id":{{imageId}}
            }
        }

        :param identifier:  The id of the category to be updated.
        :param content:     All the fields that should be updated.
        :return:            Metadata of the updated category.
        """
        return self._patch_request(self.path, {'id': identifier}, content)

    def delete(self, identifier: str):
        """
        Delete a category.

        :param identifier:  The id of the category to be deleted.
        """
        self._delete_request(self.path, {'id': identifier})

    def articles(self, world_id: str, category_id: str, complete: bool = True, limit: int = 50, offset: int = 0) -> Iterable[Dict[str, Any]]:
        """
        List all articles by a category given, filtered with a limit of entities shown and an offset.

        :param world_id:    The id of the world the articles should be returned from.
        :param category_id: The id of the category to return the articles from. To get articles without a category set
                            this value to -1. This does not return articles that have a parent article instead of a
                            category.
        :param complete     Ignore limit and offset and return all the articles as an iterable. Will fetch a new batch
                            every 50 articles.
        :param limit:       Determines how many articles are returned. Value between 1 and 50.
        :param offset:      Determines the offset at which articles are returned. Has to be a positive integer.
        :return:
        """
        if complete:
            return self._scroll_collection(self.path_articles, {'id': world_id}, 'entities', 'category', category_id)
        return self._post_request(self.path_articles,
                                  {'id': world_id},
                                  {'limit': limit, 'offset': offset, 'category': {'id': category_id}})['entities']
