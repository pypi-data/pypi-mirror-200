# -*- coding: UTF-8 -*-
# Copyright 2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)


from lino.core import constants as ext_requests
from lino.core.renderer import HtmlRenderer
from lino.core.renderer import add_user_language

from lino.modlib.bootstrap3.renderer import Renderer

class Renderer(Renderer):
    def get_request_url(self, ar, *args, **kw):
        obj = ar.selected_rows[0]
        return obj.publisher_url(ar, **kw)
