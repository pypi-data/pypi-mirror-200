# -*- coding: utf-8 -*-

from pathlib_mate import Path

_dir_here = Path.dir_here(__file__)

dir_project_root = _dir_here.parent
dir_data = _dir_here.joinpath("data")

# ------------------------------------------------------------------------------
# ${HOME}/.aws_console_url_search/ dir related
# ------------------------------------------------------------------------------
dir_home = Path.home()
dir_aws_console_url_search = dir_home.joinpath(".aws_console_url_search")
dir_cache = dir_aws_console_url_search.joinpath("cache")
dir_main_service_index = dir_aws_console_url_search.joinpath("main_service_index")
dir_sub_service_index = dir_aws_console_url_search.joinpath("sub_service_index")
dir_any_service_index = dir_aws_console_url_search.joinpath("any_service_index")

# ------------------------------------------------------------------------------
# test related
# ------------------------------------------------------------------------------
dir_tests = dir_project_root.joinpath("tests")
