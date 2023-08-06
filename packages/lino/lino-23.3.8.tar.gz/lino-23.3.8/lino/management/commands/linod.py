# -*- coding: UTF-8 -*-
# Copyright 2016-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import os
import time
import socket
import struct
import pickle
from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from lino.api import dd
from lino.modlib.linod.utils import LINOD
from lino.utils.socks import get_from_socket, send_through_socket

# For the schedule logger we set level to WARNING because
# otherwise it would log a message every 10 seconds when
# running an "often" job. We must do this after Django's
# logger configuration.
# import logging
# logging.getLogger('schedule').setLevel(logging.WARNING)


class Command(BaseCommand):
    help = """Run a Lino daemon for this site."""

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--list', '-l', action='store_true',
            dest='list_jobs', default=False,
            help="Just list the jobs, don't run them.")

    def handle(self, *args, **options):
        # lino.startup()
        # lino.site_startup()
        # # rt.startup()
        # schedule.logger.setLevel(logging.WARNING)
        if not settings.SITE.use_linod:
            dd.logger.info("This site does not use linod.")
            return
        import schedule
        n = len(schedule.jobs)
        # n = len(dd.SCHEDULES)
        if n == 0:
            dd.logger.info("This site has no scheduled jobs.")
            return
        dd.logger.info("%d scheduled jobs:", n)
        for i, job in enumerate(schedule.jobs, 1):
            dd.logger.info("[%d] %r", i, job)

        # Get jobs from channels worker
        sockd = str(settings.SITE.site_dir / 'sockd')
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
            try:
                os.unlink(sockd)
            except OSError:
                pass
            sock.bind(sockd)
            async_to_sync(get_channel_layer().send)(LINOD, {'type': 'job.deferred.list'})
            sock.listen(1)
            client_sock, _ = sock.accept()
            data = pickle.loads(get_from_socket(client_sock))
            client_sock.close()
            if len(data):
                dd.logger.info(f"{len(data)} deferred jobs: ")
                for item in data:
                    dd.logger.info(item)
        os.remove(sockd)
