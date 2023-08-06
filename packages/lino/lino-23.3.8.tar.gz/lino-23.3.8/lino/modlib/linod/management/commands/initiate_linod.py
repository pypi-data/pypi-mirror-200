# -*- coding: UTF-8 -*-
# Copyright 2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import asyncio
from django.core.management.base import BaseCommand
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from lino.modlib.linod.utils import LINOD

import time

class Command(BaseCommand):
    def handle(self, *args, **options):
        async def do():
            layer = get_channel_layer()
            await asyncio.sleep(1)
            await layer.send(LINOD, {'type': 'log.server'})
            await asyncio.sleep(1)
            await layer.send(LINOD, {'type': 'run.schedule'})
        async_to_sync(do)()