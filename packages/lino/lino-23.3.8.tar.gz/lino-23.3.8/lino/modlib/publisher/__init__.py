# -*- coding: UTF-8 -*-
# Copyright 2020-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api.ad import Plugin

from lino.core.dashboard import DashboardItem


class PublisherDashboardItem(DashboardItem):

    def __init__(self, pv, **kwargs):
        self.publisher_view = pv
        super().__init__(str(pv), **kwargs)
        # print("20220927 dashboard item", pv.publisher_location)

    def render(self, ar, **kwargs):
        yield "<h3>{}</h3>".format(self.publisher_view.table_class.label)
        sar = self.publisher_view.table_class.request(parent=ar)
        for obj in sar:
            yield "<p>{}</p>".format(sar.row_as_paragraph(obj))


class Plugin(Plugin):

    needs_plugins = ["lino.modlib.jinja", "lino.modlib.bootstrap3"]

    home_view = None
    admin_location = "/admin/"

    def on_init(self):

        if not self.admin_location.endswith('/'):
            raise Exception("`publisher.admin_location` must end with a '/'!")
        if not self.admin_location.startswith('/'):
            raise Exception("`publisher.admin_location` must start with a '/'!")

        if self.home_view is not None:
            self.site.site_prefix = self.admin_location
        super().on_init()

    def on_ui_init(self, kernel):
        from .renderer import Renderer
        self.renderer = Renderer(self)
        # ui.bs3_renderer = self.renderer


    # ui_handle_attr_name = "publisher"

    def get_patterns(self):
        from django.urls import re_path as url
        from lino.core.utils import models_by_base
        from . import views
        from .mixins import Publishable
        from .choicelists import PublisherViews
        # raise Exception("20220927")
        # print("20220927", list(PublisherViews.get_list_items()))

        for pv in PublisherViews.get_list_items():
            # print("20220927", pv.publisher_location)
            if pv.publisher_location is not None:
                if pv.publisher_location == self.home_view:
                    yield url("^$", views.Element.as_view(publisher_view=pv), {'pk': 1})

                yield url('^{}/(?P<pk>.+)$'.format(pv.publisher_location),
                    views.Element.as_view(publisher_view=pv))

        # for m in models_by_base(Publishable):
        #     if m.publisher_location is not None:
        #         yield url('^{}/(?P<pk>.+)$'.format(m.publisher_location),
        #             views.Element.as_view(publisher_model=m))
        #         yield url('^{}/$'.format(m.publisher_location),
        #             views.Element.as_view(publisher_model=m))
        # yield url('^$',views.Index.as_view())
        # yield url('^login$',views.Login.as_view())

    def unused_get_dashboard_items(self, user):
        # print("20210112 get_dashboard_items")
        from .choicelists import PublisherViews
        for pv in PublisherViews.get_list_items():
            # print("20210112 ", pv.model.publisher_location)
            yield PublisherDashboardItem(pv)
        # from lino.core.utils import models_by_base
        # from .mixins import Publishable
        # for m in models_by_base(Publishable):
        #     # print("20210112 ", m, m.publisher_location)
        #     yield PublisherDashboardItem(m)
