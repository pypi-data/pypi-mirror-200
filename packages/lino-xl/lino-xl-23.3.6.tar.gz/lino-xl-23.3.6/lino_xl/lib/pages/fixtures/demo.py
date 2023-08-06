# -*- coding: UTF-8 -*-
# Copyright 2012-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lorem import get_paragraph
from django.utils import translation
from django.conf import settings
from lino.api import rt, dd, _
from lino.utils import Cycler
from lino.modlib.comments.fixtures.demo2 import lorem, short_lorem

welcome = _("""Welcome to our great website. We are proud to present
the best content about foo, bar and baz.
""")

# BODIES = Cycler([lorem, short_lorem])
# blog_body = "[eval sar.show(settings.SITE.models.blogs.LatestEntries)]"
blog_body = "[show blogs.LatestEntries]"
blog_body = ""
site_pages = [
    (_("Home"), welcome, [
        (_("Services"), None, [
            (_("Washing"), None, []),
            (_("Drying"), None, [
                (_("Air drying"), None, []),
                (_("Machine drying"), None, [])]),
            (_("Ironing"), None, []),
        ]),
        (_("Prices"), None, []),
        (_("Blog"), blog_body, []),
        (_("About us"), None, [
            (_("Team"), None, []),
            (_("History"), None, []),
            (_("Contact"), None, []),
            (_("Terms & conditions"), None, []),
        ])
    ])
]

# from pprint import pprint
# pprint(pages)

def objects():
    Node = rt.models.pages.Node
    # for lc in settings.SITE.LANGUAGE_CHOICES:
    #     language = lc[0]
    #     kwargs = dict(language=language, ref='index')
    #     with translation.override(language):
    # counter = {None: 0}

    def make_pages(pages, parent=None):
        for title, body, children in pages:
            kwargs = dict()
            if parent is None:
                kwargs.update(ref='index')
            kwargs = dd.str2kw("title", title, **kwargs)
            if body is None:
                kwargs.update(body=get_paragraph())
            else:
                kwargs = dd.str2kw("body", body, **kwargs)
            # for i in range(counter[None]):
            #     body += paragraph()
            # if counter[None] > 0:
            #     kwargs.pop('ref', None)
            # p = Node(title=str(title), body=str(body), parent=parent, **kwargs)
            p = Node(parent=parent, **kwargs)
            yield p
            # ref = None
            # counter[None] += 1
            # print("20230324", title, kwargs)
            yield make_pages(children, p)
    yield make_pages(site_pages)
