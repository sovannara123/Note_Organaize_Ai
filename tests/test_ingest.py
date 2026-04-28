import os
import tempfile
import unittest

from core.ingest import NoteIngester


class TestNoteIngester(unittest.TestCase):
    """
    Unit tests for NoteIngester.
    """

    def setUp(self):
        """
        Create temporary test files before each test.
        """
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_folder = self.temp_dir.name

    def tearDown(self):
        """
        Clean up temporary files after each test.
        """
        self.temp_dir.cleanup()

    def _create_file(self, filename: str, content: str = "") -> str:
        """
        Helper method to create test files.

        Args:
            filename (str): Name of file.
            content (str): File content.

        Returns:
            str: Full file path.
        """
        file_path = os.path.join(self.test_folder, filename)

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

        return file_path

    def test_load_txt_file_success(self):
        """
        Should successfully load .txt file.
        """
        file_path = self._create_file("note.txt", "Hello world")

        ingester = NoteIngester(file_path)
        result = ingester.load_file()

        self.assertEqual(result, "Hello world")

    def test_load_md_file_success(self):
        """
        Should successfully load .md file.
        """
        file_path = self._create_file("note.md", "# My Notes")

        ingester = NoteIngester(file_path)
        result = ingester.load_file()

        self.assertEqual(result, "# My Notes")

    def test_file_not_found(self):
        """
        Should raise FileNotFoundError for missing file.
        """
        file_path = os.path.join(self.test_folder, "missing.txt")

        ingester = NoteIngester(file_path)

        with self.assertRaises(FileNotFoundError):
            ingester.load_file()

    def test_unsupported_extension(self):
        """
        Should raise ValueError for unsupported file type.
        """
        file_path = self._create_file("note.docx", "test")

        ingester = NoteIngester(file_path)

        with self.assertRaises(ValueError):
            ingester.load_file()

    def test_empty_file(self):
        """
        Should raise ValueError for empty file.
        """
        file_path = self._create_file("empty.txt", "")

        ingester = NoteIngester(file_path)

        with self.assertRaises(ValueError):
            ingester.load_file()

    def test_whitespace_only_file(self):
        """
        Should raise ValueError for whitespace-only file.
        """
        file_path = self._create_file("blank.txt", "   \n   ")

        ingester = NoteIngester(file_path)

        with self.assertRaises(ValueError):
            ingester.load_file()


if __name__ == "__main__":
    unittest.main()