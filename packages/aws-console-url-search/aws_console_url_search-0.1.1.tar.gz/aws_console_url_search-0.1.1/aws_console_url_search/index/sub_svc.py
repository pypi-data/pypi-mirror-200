# -*- coding: utf-8 -*-

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


class SubServiceSchema(fields.SchemaClass):
    id = fields.NGRAM(
        minsize=2,
        maxsize=10,
        stored=True,
        sortable=True,
    )
    id_kw = fields.KEYWORD(stored=False)
    name = fields.NGRAM(
        minsize=2,
        maxsize=10,
        stored=True,
    )
    short_name = fields.NGRAM(
        minsize=2,
        maxsize=10,
        stored=True,
    )
    url = fields.STORED()
    weight = fields.NUMERIC(
        sortable=True,
        stored=True,
    )
    search_terms = fields.NGRAM(
        minsize=2,
        maxsize=10,
        stored=False,
        field_boost=2.0,
    )
    main_svc_id = fields.KEYWORD(stored=True)


sub_service_schema = SubServiceSchema()


@dataclasses.dataclass
class SubServiceDocument(BaseModel):
    main_svc_id: str = dataclasses.field()
    id: str = dataclasses.field()
    name: str = dataclasses.field()
    url: str = dataclasses.field()
    weight: int = dataclasses.field()
    short_name: T.Optional[str] = dataclasses.field(default=None)

    @property
    def title(self) -> str:
        return f"{self.main_svc_id}-{self.id}"

    @property
    def subtitle(self) -> str:
        if self.short_name:
            return f"{self.name} ({self.short_name})"
        else:
            return self.name


@dataclasses.dataclass
class SubServiceIndex(SearchIndex):
    @classmethod
    def new(
        cls,
        dir_index: Path = dir_sub_service_index,
    ) -> "SubServiceIndex":
        return SubServiceIndex(
            schema=sub_service_schema,
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
        if multi_thread:  # pragma: no cover
            writer = idx.writer(procs=os.cpu_count())
        else:
            writer = idx.writer()

        for main_service in main_services:
            for sub_service in main_service.sub_services:
                document = {
                    "id": sub_service.id,
                    "id_kw": sub_service.id,
                    "name": sub_service.name,
                    "short_name": sub_service.short_name,
                    "url": sub_service.url,
                    "search_terms": " ".join(sub_service.search_terms),
                    "weight": sub_service.weight,
                }
                new_document = {k: v for k, v in document.items() if bool(v)}
                new_document["main_svc_id"] = main_service.id
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
    def get_by_id(
        self,
        main_svc_id: str,
        sub_svc_id: str,
    ) -> T.Optional[SubServiceSchema]:
        q = query.And(
            [
                query.Term("main_svc_id", main_svc_id),
                query.Term("id_kw", sub_svc_id),
            ]
        )
        idx = self.get_index()
        with idx.searcher() as searcher:
            doc_list = [hit.fields() for hit in searcher.search(q, limit=1)]
        try:
            return SubServiceDocument.from_dict(doc_list[0])
        except IndexError:
            return None

    @cache.memoize(expire=CACHE_EXPIRE)
    def top_k(
        self,
        main_svc_id: str,
        k: int = 20,
    ) -> T.List[SubServiceDocument]:
        q = query.Term("main_svc_id", main_svc_id)
        idx = self.get_index()
        multi_facet = sorting.MultiFacet()
        multi_facet.add_field("weight", reverse=True)
        multi_facet.add_field("id")
        doc_list = list()
        with idx.searcher() as searcher:
            for hit in searcher.search(q, sortedby=multi_facet, limit=k):
                doc_list.append(SubServiceDocument.from_dict(hit.fields()))
        return doc_list

    @cache.memoize(expire=CACHE_EXPIRE)
    def search(
        self,
        main_svc_id: str,
        query_str: str,
        limit: int = 20,
    ) -> T.List[SubServiceDocument]:
        q = query.And(
            [
                query.Term("main_svc_id", main_svc_id),
                qparser.MultifieldParser(
                    [
                        "id",
                        "name",
                        "short_name",
                        "search_terms",
                    ],
                    schema=self.schema,
                ).parse(query_str),
            ]
        )
        index = self.get_index()
        multi_facet = sorting.MultiFacet()
        multi_facet.add_field("weight", reverse=True)
        multi_facet.add_field("id")
        doc_list = list()
        with index.searcher() as searcher:
            for hit in searcher.search(q, sortedby=multi_facet, limit=limit):
                doc_list.append(SubServiceDocument.from_dict(hit.fields()))

        # if the "id" starts with the query str, prioritize it
        doc_list_1 = list()
        doc_list_2 = list()
        for doc in doc_list:
            if doc.id.startswith(query_str):
                doc_list_1.append(doc)
            else:
                doc_list_2.append(doc)
        doc_list_1.extend(doc_list_2)
        return doc_list_1
