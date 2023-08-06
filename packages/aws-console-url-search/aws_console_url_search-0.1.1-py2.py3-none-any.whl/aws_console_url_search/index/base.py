# -*- coding: utf-8 -*-

"""
This module provides a base class for each whoosh search index.
"""

import dataclasses
from pathlib_mate import Path
from whoosh import fields
from whoosh.index import open_dir, create_in, FileIndex
from ..cache import dir_cache


@dataclasses.dataclass
class SearchIndex:
    """
    Base class for whoosh search index. It has to implement the following methods:

    - ``build_index()``:
    - ``search()``:
    """
    schema: fields.SchemaClass = dataclasses.field()
    dir_index: Path = dataclasses.field()

    def __post_init__(self):
        self.dir_index = Path(self.dir_index)

    def get_index(self) -> FileIndex:
        if self.dir_index.exists():
            idx = open_dir(self.dir_index.abspath)
        else:
            self.dir_index.mkdir(parents=True, exist_ok=True)
            idx = create_in(dirname=self.dir_index.abspath, schema=self.schema)
        return idx

    def clear_cache(self):
        dir_cache.remove_if_exists()
