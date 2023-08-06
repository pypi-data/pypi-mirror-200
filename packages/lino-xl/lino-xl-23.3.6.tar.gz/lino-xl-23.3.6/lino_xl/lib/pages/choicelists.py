# -*- coding: UTF-8 -*-
# Copyright 2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import logging ; logger = logging.getLogger(__name__)

import os
import io
from copy import copy

from django.conf import settings
from django.utils import translation


try:
    from django.template import TemplateDoesNotExist
except ImportError:
    from django.template.loader import TemplateDoesNotExist

from django.template.loader import select_template

from lino.core.choicelists import ChoiceList, Choice
from lino.utils.media import MediaFile
from lino.api import rt, _


class NodeType(Choice):

    def register(self):
        NodeTypes.add_item_instance(self)

    def get_previewable_text(self, obj):
        return ""


class DataViewNodeType(NodeType):

    data_view = None

    def __init__(self, data_view, *args, **kwargs):
        self.data_view = data_view
        super().__init__(str(data_view), *args, **kwargs)


class NodeTypes(ChoiceList):
    # verbose_name = _("Build method")
    verbose_name = _("Node type")
    item_class = NodeType
    # app_label = 'lino'
    max_length = 50
