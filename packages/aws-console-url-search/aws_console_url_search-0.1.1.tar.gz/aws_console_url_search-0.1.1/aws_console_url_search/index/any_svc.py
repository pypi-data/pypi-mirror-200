# -*- coding: utf-8 -*-

"""
A wrapper around the whoosh index object.
"""

import typing as T
import os
import dataclasses
from pathlib_mate import Path
from whoosh import fields, qparser, query, sorting

from ..model import BaseModel, MainService, load_data
from ..paths import dir_sub_service_index
from ..cache import cache
from ..constants import CACHE_EXPIRE
from .base import SearchIndex


class AnyServiceSchema(fields.SchemaClass):
    main_svc_id = fields.NGRAM(
        minsize=2,
        maxsize=10,
        stored=True,
        sortable=True,
        field_boost=3.0,
    )
    main_svc_id_kw = fields.KEYWORD(stored=False)
    main_svc_name = fields.NGRAM(
        minsize=2,
        maxsize=10,
        stored=True,
    )
    main_svc_short_name = fields.NGRAM(
        minsize=2,
        maxsize=10,
        stored=True,
        field_boost=3.0,
    )
    main_svc_description = fields.STORED()
    main_svc_url = fields.STORED()
    main_svc_regional = fields.BOOLEAN(stored=True)
    main_svc_weight = fields.NUMERIC(
        sortable=True,
        stored=True,
    )
    main_svc_search_terms = fields.NGRAM(
        minsize=2,
        maxsize=10,
        stored=False,
        field_boost=2.0,
    )
    main_svc_has_sub_svc = fields.STORED()

    sub_svc_id = fields.NGRAM(
        minsize=2,
        maxsize=10,
        stored=True,
        sortable=True,
    )
    sub_svc_id_kw = fields.KEYWORD(stored=False)
    sub_svc_name = fields.NGRAM(
        minsize=2,
        maxsize=10,
        stored=True,
    )
    sub_svc_short_name = fields.NGRAM(
        minsize=2,
        maxsize=10,
        stored=True,
    )
    sub_svc_url = fields.STORED()
    sub_svc_weight = fields.NUMERIC(
        sortable=True,
        stored=True,
    )
    sub_svc_search_terms = fields.NGRAM(
        minsize=2,
        maxsize=10,
        stored=False,
        field_boost=2.0,
    )


any_service_schema = AnyServiceSchema()


@dataclasses.dataclass
class AnyServiceDocument(BaseModel):
    main_svc_id: str = dataclasses.field()
    main_svc_name: str = dataclasses.field()
    main_svc_url: str = dataclasses.field()
    main_svc_regional: bool = dataclasses.field()
    main_svc_weight: int = dataclasses.field()
    main_svc_has_sub_svc: bool = dataclasses.field()
    main_svc_short_name: T.Optional[str] = dataclasses.field(default=None)
    main_svc_description: T.Optional[str] = dataclasses.field(default=None)

    sub_svc_id: T.Optional[str] = dataclasses.field(default=None)
    sub_svc_name: T.Optional[str] = dataclasses.field(default=None)
    sub_svc_url: T.Optional[str] = dataclasses.field(default=None)
    sub_svc_weight: T.Optional[int] = dataclasses.field(default=None)
    sub_svc_short_name: T.Optional[str] = dataclasses.field(default=None)

    @property
    def title(self) -> str:
        if self.sub_svc_id:
            return f"{self.main_svc_id}-{self.sub_svc_id}"
        else:
            return self.main_svc_id

    @property
    def subtitle(self) -> str:
        if self.sub_svc_id:
            if self.sub_svc_short_name:
                return f"{self.sub_svc_name} ({self.sub_svc_short_name})"
            else:
                return self.sub_svc_name
        else:
            if self.main_svc_description:
                return f"{self.main_svc_name} - {self.main_svc_description}"
            else:
                return self.main_svc_name


@dataclasses.dataclass
class AnyServiceIndex(SearchIndex):
    @classmethod
    def new(
        cls,
        dir_index: Path = dir_sub_service_index,
    ) -> "AnyServiceIndex":
        return AnyServiceIndex(
            schema=any_service_schema,
            dir_index=dir_index,
        )

    def _build_index(
        self,
        main_services: T.Optional[T.List[MainService]] = None,
        multi_thread: bool = False,
    ):
        """
        Build Whoosh Index, add document.
        """
        if main_services is None:
            main_services = load_data()

        idx = self.get_index()
        if multi_thread: # pragma: no cover
            writer = idx.writer(procs=os.cpu_count())
        else:
            writer = idx.writer()

        for main_service in main_services:
            document = {
                "main_svc_id": main_service.id,
                "main_svc_id_kw": main_service.id,
                "main_svc_name": main_service.name,
                "main_svc_short_name": main_service.short_name,
                "main_svc_description": main_service.description,
                "main_svc_url": main_service.url,
                "main_svc_search_terms": " ".join(main_service.search_terms),
                "main_svc_weight": main_service.weight,
            }
            new_document = {k: v for k, v in document.items() if bool(v)}
            new_document["main_svc_has_sub_svc"] = bool(main_service.sub_services)
            new_document["main_svc_regional"] = main_service.regional
            writer.add_document(**new_document)
            for sub_service in main_service.sub_services:
                document = {
                    "main_svc_id": main_service.id,
                    "main_svc_id_kw": main_service.id,
                    "main_svc_name": main_service.name,
                    "main_svc_short_name": main_service.short_name,
                    "main_svc_description": main_service.description,
                    "main_svc_url": main_service.url,
                    "main_svc_search_terms": " ".join(main_service.search_terms),
                    "main_svc_weight": main_service.weight,
                    "sub_svc_id": sub_service.id,
                    "sub_svc_id_kw": sub_service.id,
                    "sub_svc_name": sub_service.name,
                    "sub_svc_short_name": sub_service.short_name,
                    "sub_svc_url": sub_service.url,
                    "sub_svc_search_terms": " ".join(sub_service.search_terms),
                    "sub_svc_weight": sub_service.weight,
                }
                new_document = {k: v for k, v in document.items() if bool(v)}
                new_document["main_svc_regional"] = main_service.regional
                new_document["main_svc_has_sub_svc"] = bool(main_service.sub_services)
                writer.add_document(**new_document)
        writer.commit()

    def build_index(
        self,
        main_services: T.Optional[T.List[MainService]] = None,
        multi_thread: bool = False,
        rebuild: bool = False,
    ):
        if rebuild:
            self.dir_index.remove_if_exists()
        self._build_index(
            main_services=main_services,
            multi_thread=multi_thread,
        )

    @cache.memoize(expire=CACHE_EXPIRE)
    def search(
        self,
        query_str: str,
        limit: int = 20,
    ) -> T.List[AnyServiceDocument]:
        q = query.And(
            [
                qparser.MultifieldParser(
                    [
                        "main_svc_id",
                        "main_svc_name",
                        "main_svc_short_name",
                        "main_svc_search_terms",
                        "sub_svc_id",
                        "sub_svc_name",
                        "sub_svc_short_name",
                        "sub_svc_search_terms",
                    ],
                    schema=self.schema,
                ).parse(query_str),
            ]
        )
        index = self.get_index()
        multi_facet = sorting.MultiFacet()
        multi_facet.add_field("main_svc_weight", reverse=True)
        multi_facet.add_field("main_svc_id")
        multi_facet.add_field("sub_svc_weight", reverse=True)
        multi_facet.add_field("sub_svc_id")
        doc_list = list()
        with index.searcher() as searcher:
            for hit in searcher.search(q, sortedby=multi_facet, limit=limit):
                doc_list.append(AnyServiceDocument.from_dict(hit.fields()))

        return doc_list
