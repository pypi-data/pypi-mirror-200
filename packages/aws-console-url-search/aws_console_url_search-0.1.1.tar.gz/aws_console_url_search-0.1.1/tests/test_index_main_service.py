# -*- coding: utf-8 -*-

import typing as T
from aws_console_url_search.tests import run_cov_test
from aws_console_url_search.index.main_svc import (
    MainServiceIndex,
)
from aws_console_url_search.paths import dir_tests


class TestMainServiceIndex:
    index: T.Optional[MainServiceIndex] = None

    @classmethod
    def setup_class(cls):
        cls.index = MainServiceIndex.new(
            dir_index=dir_tests.joinpath("tmp", "main_service_index")
        )
        cls.index.build_index(rebuild=True)
        cls.index.clear_cache()

    def test_search_one(self):
        test_cases = [
            ("ec2", "ec2"),
            ("s3", "s3"),
            ("vpc", "vpc"),
            ("iam", "iam"),
            ("invalid", None),
        ]
        for query_str, id in test_cases:
            if id is None:
                assert self.index.get_by_id(query_str) is None
            else:
                assert self.index.get_by_id(query_str).id == id

    def test_top_k(self):
        for _ in range(10):
            ids = [doc.id for doc in self.index.top_k()]
            assert ids[:4] == [
                "iam",
                "s3",
                "ec2",
                "vpc",
            ]

    def test_search(self):
        test_cases = [
            ("ec2", "ec2"),
            ("elastic compute", "ec2"),
            ("oss", "aos"),
            ("opensearch", "aos"),
            ("open search", "aos"),
            ("sage", "sagemaker"),
            ("sagemaker", "sagemaker"),
            ("sage maker", "sagemaker"),
            ("machine learning", "sagemaker"),
            ("ml", "sagemaker"),
        ]
        for query_str, id in test_cases:
            assert self.index.search(query_str)[0].id == id

    def test_title_and_subtitle(self):
        for doc in self.index.top_k(k=100):
            _ = doc.title
            _ = doc.subtitle


if __name__ == "__main__":
    run_cov_test(__file__, "aws_console_url_search.index.main_svc", preview=False)
