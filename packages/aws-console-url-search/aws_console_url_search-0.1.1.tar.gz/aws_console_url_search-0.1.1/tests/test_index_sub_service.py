# -*- coding: utf-8 -*-

import typing as T
from aws_console_url_search.tests import run_cov_test
from aws_console_url_search.index.sub_svc import (
    SubServiceIndex,
)
from aws_console_url_search.paths import dir_tests


class TestSubServiceIndex:
    index: T.Optional[SubServiceIndex] = None

    @classmethod
    def setup_class(cls):
        cls.index = SubServiceIndex.new(
            dir_index=dir_tests.joinpath("tmp", "sub_service_index")
        )
        cls.index.build_index(rebuild=True)
        cls.index.clear_cache()

    def test_search_one(self):
        test_cases = [
            ("ec2", "securitygroups", "securitygroups"),
            ("ec2", "invalid", None),
        ]
        for main_svc_id, sub_svc_id, expected_sub_svc_id in test_cases:
            if expected_sub_svc_id is None:
                assert self.index.get_by_id(main_svc_id, sub_svc_id) is None
            else:
                assert (
                    self.index.get_by_id(main_svc_id, sub_svc_id).id
                    == expected_sub_svc_id
                )

    def test_top_k(self):
        for _ in range(10):
            ids = [doc.id for doc in self.index.top_k("ec2")]
            assert ids[:4] == [
                "instances",
                "securitygroups",
                "amis",
                "volumes",
            ]

    def test_search(self):
        test_cases = [
            ("ec2", "inst", "instances"),
            ("ec2", "instance", "instances"),
            ("ec2", "security group", "securitygroups"),
            ("ec2", "securitygroup", "securitygroups"),
            ("ec2", "sg", "securitygroups"),
            ("ec2", "ebs", "volumes"),
            ("ec2", "volume", "volumes"),
            ("ec2", "elastic block storage", "volumes"),
            ("iam", "role", "roles"),
            ("iam", "policy", "policies"),
        ]
        for main_svc_id, query_str, sub_svc_id in test_cases:
            assert self.index.search(main_svc_id, query_str)[0].id == sub_svc_id

    def test_title_and_subtitle(self):
        for doc in self.index.top_k("ec2"):
            _ = doc.title
            _ = doc.subtitle


if __name__ == "__main__":
    run_cov_test(__file__, "aws_console_url_search.index.sub_svc", preview=False)
