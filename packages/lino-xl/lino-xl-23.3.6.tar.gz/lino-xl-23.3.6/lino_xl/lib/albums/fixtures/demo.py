# -*- coding: UTF-8 -*-
# Copyright 2009-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from pathlib import Path
from lino.api import rt, dd, _
from lino.utils import Cycler
from lino.modlib.uploads.mixins import make_uploaded_file

srcpath = Path(__file__).parent


def objects():
    Album = rt.models.albums.Album
    File = rt.models.uploads.Upload
    # FileUsage = rt.models.albums.FileUsage

    demo_date = dd.demo_date()

    year = Album(designation=str(demo_date.year))
    yield year
    for month in "01 02 03 04 05 06 07 08 09 10 11 12".split():
        yield Album(parent=year, designation=month)

    yield Album(**dd.str2kw("designation", _("Furniture")))
    yield Album(**dd.str2kw("designation", _("Things")))
    yield Album(**dd.str2kw("designation", _("Services")))

    books = Album(**dd.str2kw("designation", _("Books")))
    yield books

    yield Album(parent=books, **dd.str2kw("designation", _("Biographies")))
    yield Album(parent=books, **dd.str2kw("designation", _("Business")))
    yield Album(parent=books, **dd.str2kw("designation", _("Culture")))
    yield Album(parent=books, **dd.str2kw("designation", _("Children")))
    yield Album(parent=books, **dd.str2kw("designation", _("Medicine")))

    thrill = Album(parent=books, **dd.str2kw("designation", _("Thriller")))
    yield thrill

    for cover in """\
MurderontheOrientExpress.jpg Murder_on_the_orient_express_cover
StormIsland.jpg Storm_island_cover
AndThenThereWereNone.jpg And_then_there_were_none
FirstThereWereTen.jpg First_there_were_ten
""".splitlines():
        name, description = cover.split()
        file = make_uploaded_file(name, srcpath / "images" / name, demo_date)
        yield File(album=thrill, file=file, description=description.replace('_', ' '))

    # if dd.is_installed('products'):
    #     FILES = Cycler(File.objects.all())
    #     OWNERS = Cycler(rt.models.products.Product.objects.all())
    #     for i in range(10):
    #         yield FileUsage(file=FILES.pop(), owner=OWNERS.pop())

    if dd.is_installed("uploads"):

        Volume = rt.models.uploads.Volume
        root_dir = srcpath.parent / 'static/albums/demo'
        vol = Volume(ref="demo", description="Static images demo",
            root_dir=root_dir, base_url="/static/albums/demo")
        yield vol

        for fn in root_dir.iterdir():
            print("20230325 {}".format(fn))
            # yield File
