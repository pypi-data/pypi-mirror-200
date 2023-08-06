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
from pywaclient.endpoints.maps import MapEndpoint
from pywaclient.endpoints.rpg_system import RpgSystemEndpoint
from pywaclient.endpoints.variables import VariableEndpoint
from pywaclient.endpoints.variable_collections import VariableCollectionEndpoint
from pywaclient.endpoints.secrets import SecretEndpoint
from pywaclient.endpoints.categories import CategoryEndpoint
from pywaclient.endpoints.articles import ArticleEndpoint
from pywaclient.endpoints.blocks import BlockEndpoint
from pywaclient.endpoints.images import ImageEndpoint
from pywaclient.endpoints.manuscripts import ManuscriptEndpoint
from pywaclient.endpoints.users import UserEndpoint
from pywaclient.endpoints.worlds import WorldEndpoint
from pywaclient.endpoints.subscriber_groups import SubscriberGroupEndpoint
from pywaclient.endpoints.histories import HistoryEndpoint
from pywaclient.endpoints.timelines import TimelineEndpoint
from pywaclient.endpoints.chronicles import ChronicleEndpoint
from pywaclient.endpoints.canvas import CanvasEndpoint
from pywaclient.endpoints.block_templates import BlockTemplateEndpoint
from pywaclient.endpoints.block_template_parts import BlockTemplatePartEndpoint
from pywaclient.endpoints.notes import NoteEndpoint
from pywaclient.endpoints.notebooks import NotebookEndpoint
from pywaclient.endpoints.notesections import NoteSectionEndpoint
from pywaclient.endpoints.block_folders import BlockFolderEndpoint
from pywaclient.endpoints.map_layers import MapLayerEndpoint
from pywaclient.endpoints.map_marker_groups import MapMarkerGroupEndpoint
from pywaclient.endpoints.map_markers import MapMarkerEndpoint
from pywaclient.endpoints.map_marker_types import MapMarkerTypeEndpoint


class BoromirApiClient:

    def __init__(self,
                 name: str,
                 url: str,
                 version: str,
                 application_key: str,
                 authentication_token: str,
                 ):
        self.headers = {
            'x-auth-token': authentication_token,
            'x-application-key': application_key,
            'Accept': 'application/json',
            'User-Agent': f'{name} ({url}, {version})'
        }
        self.headers_post = self.headers.copy()
        self.headers_post['Content-type'] = 'application/json'
        self.base_url = 'https://www.worldanvil.com/api/external/boromir/'
        self.block = BlockEndpoint(self)
        self.block_folder = BlockFolderEndpoint(self)
        self.article = ArticleEndpoint(self)
        self.image = ImageEndpoint(self)
        self.manuscript = ManuscriptEndpoint(self)
        self.user = UserEndpoint(self)
        self.secret = SecretEndpoint(self)
        self.world = WorldEndpoint(self)
        self.category = CategoryEndpoint(self)
        self.variable_collection = VariableCollectionEndpoint(self)
        self.variable = VariableEndpoint(self)
        self.rpg_system = RpgSystemEndpoint(self)
        self.subscriber_group = SubscriberGroupEndpoint(self)
        self.map = MapEndpoint(self)
        self.map_layer = MapLayerEndpoint(self)
        self.map_marker_group = MapMarkerGroupEndpoint(self)
        self.map_marker = MapMarkerEndpoint(self)
        self.map_marker_types = MapMarkerTypeEndpoint(self)
        self.history = HistoryEndpoint(self)
        self.timeline = TimelineEndpoint(self)
        self.canvas = CanvasEndpoint(self)
        self.chronicle = ChronicleEndpoint(self)
        self.block_template = BlockTemplateEndpoint(self)
        self.block_template_part = BlockTemplatePartEndpoint(self)
        self.note = NoteEndpoint(self)
        self.note_section = NoteSectionEndpoint(self)
        self.notebook = NotebookEndpoint(self)