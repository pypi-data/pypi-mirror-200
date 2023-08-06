# Copyright 2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# See https://dev.lino-framework.org/plugins/linod.html

import re
from lino.api import ad, _

try:
    import channels
except ImportError:
    channels = None


class Plugin(ad.Plugin):
    verbose_name = _("Lino daemon")

    if channels is not None:
        # otherwise pm install would fail
        needs_plugins = ['channels']

    def on_plugins_loaded(self, site):
        assert self.site is site
        sd = site.django_settings
        # the dict which will be used to create settings
        cld = {}
        sd['CHANNEL_LAYERS'] = {"default": cld}
        sd['ASGI_APPLICATION'] = "lino.modlib.linod.routing.application"
        cld["BACKEND"] = "channels_redis.core.RedisChannelLayer"
        cld['CONFIG'] = {
            "hosts": [("localhost", 6379)],
            "channel_capacity": {
                "http.request": 200,
                "http.response!*": 10,
                re.compile(r"^websocket.send\!.+"): 80,
            }
        }

    def get_requirements(self, site):
        yield 'channels'
        yield 'channels_redis'
        yield 'daphne'


    def get_used_libs(self, html=None):
        if channels is None:
            version = self.site.not_found_msg
        else:
            version = channels.__version__
        yield ("Channels", version, "https://github.com/django/channels")
