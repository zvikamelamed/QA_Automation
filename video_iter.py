import warnings

from allegroai import DataView
from allegroai_api.session.client import APIClient
from allegroai_api.session.datamodel import UnusedKwargsWarning
from allegroai_api.services.v2_2.frames import Dataview


def get_videos(dataview: DataView, page_size=500):
    client = APIClient()

    with warnings.catch_warnings():
        warnings.simplefilter('ignore', UnusedKwargsWarning)
        dv = Dataview.from_dict(dataview._get_dataview().data.to_dict())

    paging_id = None
    page = 0

    while True:
        res = client.frames.get_snippets_for_dataview(
            dataview=dv,
            page=page,
            page_size=page_size,
            paging_id=paging_id,
        )

        # print(f"{res.page}/{res.pages_total}")

        paging_id = res.paging_id
        page += 1

        if res.frames:
            yield from res.frames

        # if res.frames:
        #     yield from (
        #         f.meta["csv_data"]["seq_id"]
        #         for f in res.frames
        #         if f.sources[0].content_type.startswith("video/")
        #     )

        if page >= res.pages_total:
            break