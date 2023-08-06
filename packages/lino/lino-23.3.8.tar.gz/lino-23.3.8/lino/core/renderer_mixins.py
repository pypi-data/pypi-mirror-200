# -*- coding: UTF-8 -*-
# Copyright 2009-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
Defines :class:`JsCacheRenderer`.
"""

import logging ; logger = logging.getLogger(__name__)
import os
import time

from django.conf import settings
from django.utils import translation

from lino.core import kernel
from lino.core import layouts
from lino.core.actions import resolve_layout
from lino.modlib.users.utils import get_user_profile


class JsCacheRenderer():
    """
    Mixin for:
    :class:`lino_react.react.renderer.Renderer`,
    :class:`lino.modlib.extjs.ext_renderer.ExtRenderer` and
    :class:`lino_extjs6.extjs.ext_renderer.ExtRenderer`.

    Includes linoweb.js cacheing functionality.

    """
    lino_web_template = "extjs/linoweb.js"

    def __init__(self):
        self.prepare_layouts()

    def write_lino_js(self, f):
        """

        :param f: File object
        :return: 1
        """
        raise NotImplementedError("Need to implement a lino_web.js writing script")

        user_type = get_user_profile()

        context = dict(
            ext_renderer=self,
            site=settings.SITE,
            settings=settings,
            lino=lino,
            language=translation.get_language(),
            # ext_requests=constants,
            constants=constants,
            extjs=self.plugin,  # 20171227
        )

        context.update(_=_)

        tpl = self.linolib_template()

        f.write(tpl.render(**context) + '\n')

        return 1

    def prepare_layouts(self):

        self.actors_list = [
            rpt for rpt in kernel.master_tables
                           + kernel.slave_tables
                           + list(kernel.generic_slaves.values())
                           + kernel.virtual_tables
                           + kernel.frames_list
                           + list(kernel.CHOICELISTS.values())]

        # self.actors_list.extend(
        #     [a for a in kernel.CHOICELISTS.values()
        #      if settings.SITE.is_installed(a.app_label)])

        # don't generate JS for abstract actors
        self.actors_list = [a for a in self.actors_list
                            if not a.is_abstract()]

        # Lino knows three types of form layouts:

        self.form_panels = set()
        self.param_panels = set()
        self.action_param_panels = set()
        self.other_panels = set()

        def add(res, collector, fl, formpanel_name, choice_name=None):
            # res: an actor class or action instance
            # collector: one of form_panels, param_panels or
            # action_param_panels
            # fl : a FormLayout
            # if str(fl).endswith("Given"):
            #     print("20210223 add", fl)
            # if str(res).endswith("MyCoursesGiven"):
            #     print("20210223 gonna add {} for {}".format(fl, res))
            if fl is None:
                return
            if fl._datasource is None:
                # raise Exception("20210223 {}".format(res))
                return  # 20130804

            if fl._datasource != res:
                fl.add_datasource(res)
                # if str(res).endswith("MyCoursesGiven"):
                #     print("20210223 added", fl._other_datasources)
                # if str(res).startswith('newcomers.AvailableCoaches'):
                #     logger.info("20150716 %s also needed by %s", fl, res)
                # if str(res) == 'courses.Pupils':
                #     print("20160329 ext_renderer.py {2}: {0} != {1}".format(
                #         fl._datasource, res, fl))

            if False:
                try:
                    lh = fl.get_layout_handle()
                except Exception as e:
                    logger.exception(e)
                    raise Exception("Could not define %s for %r: %s" % (
                        formpanel_name, res, e))

                # lh.main.loosen_requirements(res)
                for e in lh.main.walk():
                    e.loosen_requirements(res)

            if fl not in collector:
                fl._formpanel_name = formpanel_name
                fl._url = res.actor_url()
                if choice_name:
                    fl.choice_name = choice_name
                collector.add(fl)
                # if str(res) == 'courses.Pupils':
                #     print("20160329 ext_renderer.py collected {}".format(fl))

        for res in self.actors_list:
            add(res, self.form_panels, res.detail_layout,
                "%s.DetailFormPanel" % res)
            for name, fl in res.extra_layouts.items():
                add(res, self.form_panels, fl,
                    "{}._{}_DetailFormPanel".format(res, name), name)
            add(res, self.form_panels, res.insert_layout,
                "%s.InsertFormPanel" % res)
            # if res.parameters is not None:
            add(res, self.param_panels, res.params_layout,
                "%s.ParamsPanel" % res)
            add(res, self.other_panels, res.card_layout,
                "%s.CardsPanel" % res)
            add(res, self.other_panels, res.list_layout,
                "%s.ItemsPanel" % res)

            for ba in res.get_actions():
                if ba.action.parameters:
                    add(res, self.action_param_panels,
                        ba.action.params_layout,
                        "%s.%s_ActionFormPanel" % (res, ba.action.action_name))

    def lino_js_parts(self):
        user_type = get_user_profile()
        filename = 'lino_'
        file_type = self.lino_web_template.rsplit(".")[-1]
        if user_type is not None:
            filename += user_type.value + '_'
        filename += translation.get_language() + '.' + file_type
        return ('cache', file_type, filename)

    def linolib_template(self):
        # env = jinja2.Environment(loader=jinja2.FileSystemLoader(
        #     os.path.dirname(__file__)))
        # return env.get_template('linoweb.js')
        env = settings.SITE.plugins.jinja.renderer.jinja_env
        return env.get_template(self.lino_web_template)


    def build_js_cache(self, force):
        """Build the :term:`site cache` files for the current user type and the
        current language.  If the file exists and is up to date, don't
        generate it unless `force` is `True`.

        """
        fn = os.path.join(*self.lino_js_parts())

        def write(f):
            self.write_lino_js(f)

        return settings.SITE.kernel.make_cache_file(fn, write, force)
