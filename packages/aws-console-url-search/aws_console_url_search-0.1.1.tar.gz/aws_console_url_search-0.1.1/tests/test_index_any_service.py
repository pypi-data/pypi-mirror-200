# -*- coding: utf-8 -*-

import typing as T
from aws_console_url_search.tests import run_cov_test
from aws_console_url_search.index.any_svc import (
    AnyServiceIndex,
)
from aws_console_url_search.paths import dir_tests


class TestAnyServiceIndex:
    index: T.Optional[AnyServiceIndex] = None

    @classmethod
    def setup_class(cls):
        cls.index = AnyServiceIndex.new(
            dir_index=dir_tests.joinpath("tmp", "any_service_index")
        )
        cls.index.build_index(rebuild=True)
        cls.index.clear_cache()

    def test_search(self):
        test_cases = [
            ("ec2 inst", "ec2", "instances"),
            ("ec2 sg", "ec2", "securitygroups"),
        ]
        for query_str, main_svc_id, sub_svc_id in test_cases:
            doc = self.index.search(query_str)[0]
            assert doc.main_svc_id == main_svc_id
            assert doc.sub_svc_id == sub_svc_id

    def test_title_and_subtitle(self):
        for doc in self.index.search("ec2"):
            _ = doc.title
            _ = doc.subtitle


if __name__ == "__main__":
    run_cov_test(__file__, "aws_console_url_search.index.any_svc", preview=False)
