# -*- coding: utf-8 -*-

import typing as T
import json
import dataclasses

from .paths import dir_data


@dataclasses.dataclass
class BaseModel:
    @classmethod
    def from_dict(cls, data: T.Dict[str, T.Any]):
        new_data = {}
        for field in dataclasses.fields(cls):
            if data.get(field.name) is not None:
                new_data[field.name] = data[field.name]
        return cls(**new_data)

    def to_dict(self) -> T.Dict[str, T.Any]:
        return dataclasses.asdict(self)


@dataclasses.dataclass
class SubService(BaseModel): # pragma: no cover
    """
    Refer to a sub service of a main service. For example, AWS S3 bucket
    is a sub service of AWS S3.

    :param id: unique id, for example, "buckets" is for AWS S3 buckets
    :param name: e.g. "Buckets"
    :param url: the href part of the url, for example, "the full url" is
        https://console.aws.amazon.com/s3/buckets?region=us-east-1
        then the "url" is "/s3/buckets"
    :param weight: the sorting weight in the searching
    :param short_name: e.g. "buckets"
    :param search_terms: additional search terms for ngram search
    """

    id: str = dataclasses.field()
    name: str = dataclasses.field()
    url: str = dataclasses.field()
    weight: int = dataclasses.field(default=1)  # 1 - 100
    short_name: T.Optional[str] = dataclasses.field(default=None)
    search_terms: T.List[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class MainService(BaseModel): # pragma: no cover
    """
    Refer to a main service. For example, AWS S3 is a main service.

    :param id: unique id, for example, "s3" is for AWS S3
    :param name: e.g. "Amazon Simple Storage Service"
    :param url: the href part of the url, for example, "the full url" is
        https://console.aws.amazon.com/s3/buckets?region=us-east-1
        then the "url" is "/s3/buckets"
    :param regional: see https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/
    :param weight: the sorting weight in the searching
    :param short_name: e.g. "S3"
    :param description: a human friendly description
    :param search_terms: additional search terms for ngram search
    :param sub_services: a list of sub services
    """

    id: str = dataclasses.field()
    name: str = dataclasses.field()
    url: str = dataclasses.field()
    regional: bool = dataclasses.field(default=True)
    weight: int = dataclasses.field(default=1)  # 1 - 1000
    short_name: T.Optional[str] = dataclasses.field(default=None)
    description: T.Optional[str] = dataclasses.field(default=None)
    search_terms: T.List[str] = dataclasses.field(default_factory=list)
    sub_services: T.List[SubService] = dataclasses.field(default_factory=list)


def load_data() -> T.List[MainService]:
    main_services = list()
    for path_json in dir_data.select_by_ext(".json"):
        data = json.loads(path_json.read_text())
        data["sub_services"] = [SubService.from_dict(dct) for dct in data["sub_services"]]
        main_service = MainService.from_dict(data)
        main_services.append(main_service)
    return main_services
