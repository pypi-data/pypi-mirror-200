import io
import unittest
import zipfile
from pathlib import Path
from typing import Optional, NamedTuple

from wwwpy import StringResource, PathResource
from wwwpy.resources import default_resource_filter, from_filesystem_once, build_archive

parent = Path(__file__).parent


class Test_bundle_definition(unittest.TestCase):
    support_data = parent / 'support_data/bundle_definition'

    def test_one_file(self):
        folder = self.support_data / 'one_file'
        actual = set(from_filesystem_once(folder))
        expect = set([PathResource('foo.py', folder / 'foo.py')])
        self.assertEqual(expect, actual)

    def test_zero_file(self):
        folder = self.support_data / 'zero_file'
        folder.mkdir(exist_ok=True)  # git does not commit empty folders
        actual = set(from_filesystem_once(folder))
        expect = set([])
        self.assertEqual(expect, actual)

    def test_selective(self):
        folder = self.support_data / 'relative_to'
        actual = set(from_filesystem_once(folder / 'yes', relative_to=folder))
        expect = set([PathResource('yes/yes.txt', folder / 'yes/yes.txt')])
        self.assertEqual(expect, actual)

    def test_item_filter(self):
        folder = self.support_data / 'item_filter'
        reject = folder / 'yes/reject'

        pycache = folder / 'yes/__pycache__'
        pycache.mkdir(exist_ok=True)
        (pycache / 'cache.txt').write_text('some cache')

        def item_filter(item: PathResource) -> Optional[PathResource]:
            if item.filepath == reject:
                return None
            return default_resource_filter(item)

        actual = set(from_filesystem_once(folder, resource_filter=item_filter))
        expect = set([PathResource('yes/yes.txt', folder / 'yes/yes.txt')])
        self.assertEqual(expect, actual)


class Test_build_archive(unittest.TestCase):
    support_data = parent / 'support_data/build_archive'

    def test_simple(self):
        class ZFile(NamedTuple):
            filename: str
            content: bytes

        folder = self.support_data / 'simple'
        (folder / 'empty_dir').mkdir(exist_ok=True)  # should be ignored by build_archive

        archive_bytes = build_archive(list(from_filesystem_once(folder)) +
                                      [StringResource('dir1/baz.txt', "#baz")])

        actual_files = set()
        with zipfile.ZipFile(io.BytesIO(archive_bytes)) as zf:
            for il in zf.infolist():
                with zf.open(il, 'r') as file:
                    actual_files.add(ZFile(il.filename, file.read()))

        expected_files = {
            ZFile('foo.txt', '#foo'.encode()),
            ZFile('dir1/bar.txt', '#bar'.encode()),
            ZFile('dir1/baz.txt', '#baz'.encode()),
        }

        self.assertEqual(expected_files, actual_files)


if __name__ == '__main__':
    unittest.main()
