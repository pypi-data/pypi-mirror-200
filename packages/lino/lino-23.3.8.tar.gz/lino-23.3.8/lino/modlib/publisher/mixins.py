# -*- coding: UTF-8 -*-
# Copyright 2020-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd, rt, _

from django import http
from django.conf import settings
from django.utils.translation import get_language
from lino.core.renderer import add_user_language
from lino.utils import buildurl
from lino.modlib.printing.mixins import Printable
from lino.modlib.printing.choicelists import BuildMethods
from .choicelists import PublisherViews

from inspect import isclass

class PreviewPublication(dd.Action):
    label = _("Preview")
    select_rows = True

    def run_from_ui(self, ar, **kw):
        # sr_selected = not isclass(self)
        # if sr_selected:
        #     ar.success(open_url=self.publisher_url())
        # else:
        #     ar.success(open_url=self.publisher_url(self, not sr_selected))
        obj = ar.selected_rows[0]
        ar.success(open_url=obj.publisher_url(ar))

    def get_view_permission(self, user_type):
        if not dd.is_installed('publisher'):
            return False
        return super().get_view_permission(user_type)


class Publishable(Printable):
    class Meta:
        abstract = True
        app_label = 'publisher'

    publisher_template = "publisher/page.pub.html"

    preview_publication = PreviewPublication()

    # @dd.action(select_rows=False)
    # def preview_publication(self, ar):
    #     sr_selected = not isclass(self)
    #     if sr_selected:
    #         ar.success(open_url=self.publisher_url())
    #     else:
    #         ar.success(open_url=self.publisher_url(self, not sr_selected))

    def publisher_url(self, ar, **kw):
        for i in PublisherViews.get_list_items():
            if isinstance(self, i.table_class.model):
                # return "/{}/{}".format(i.publisher_location, self.pk)
                add_user_language(kw, ar)
                # return buildurl("/" + i.publisher_location, str(self.pk), **dd.urlkwargs())
                return buildurl("/", i.publisher_location, str(self.pk), **kw)
        # return "Oops 20220927"  # publisher_location is now in PublisherView

    def get_preview_context(self, ar):
        return ar.get_printable_context(obj=self)

    # def render_from(self, tplname, ar):
    #     env = settings.SITE.plugins.jinja.renderer.jinja_env
    #     context = self.get_preview_context(ar)
    #     template = env.get_template(tplname)
    #     # print("20210112 publish {} {} using {}".format(cls, obj, template))
    #     # context = dict(obj=self, request=request, language=get_language())
    #     return template.render(**context)
    #
    def get_publisher_response(self, ar):
        context = self.get_preview_context(ar)
        html = ''.join(self.as_page(ar))
        # context.update(content=html, admin_site_prefix=dd.plugins.publisher.admin_location)
        context.update(content=html)
        template = settings.SITE.plugins.jinja.renderer.jinja_env.get_template(self.publisher_template)
        return http.HttpResponse(template.render(**context), content_type='text/html;charset="utf-8"')
