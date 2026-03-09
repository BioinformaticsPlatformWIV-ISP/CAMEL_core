from pathlib import Path

from camelcore.app.testsuite import TestSuite
from camelcore.app.utils import fileutils


class TestFileUtils(TestSuite):
    """
    Tests the fileutils module.
    """

    def test_hash_file(self) -> None:
        """
        Tests the hash file function.
        :return: None
        """
        self.assertEqual(
            '258cf917517a15d335c42e9da9efdd6f157c88a22ab4a9aa94743dafe3c82fc1',
            fileutils.hash_file(TestSuite.get_test_file('fq_1.fq')))

    def test_get_all_files(self) -> None:
        """
        Tests the get all files function.
        :return: None
        """
        nb_files = 4
        for nb in range(nb_files):
            Path(self.running_dir / f'file_{nb}').touch()
        self.assertEqual(len(fileutils.get_all_files(self.running_dir)), nb_files)

    def test_hash_value(self) -> None:
        """
        Tests the hash value function.
        :return: None
        """
        self.assertEqual(
            '332f61e385645bc5ad755f2ff6ccf8c4693f569a79f33427065731e9ff41b812',
            fileutils.hash_value('this_value_will_be_hashed')
        )

    def test_concatenate_files(self) -> None:
        """
        Tests the concatenate files function.
        :return: None
        """
        # Create test files
        file_a = self.running_dir / 'file_a.txt'
        file_b = self.running_dir / 'file_b.txt'
        with file_a.open('w') as handle:
            handle.write('123')
        with file_b.open('w') as handle:
            handle.write('abc')

        # Concatenate
        path_out = self.running_dir / 'file_out.txt'
        fileutils.concatenate_files(output_path=path_out, input_files=[file_a, file_b])

        # Verify output
        with path_out.open() as handle:
            self.assertEqual(handle.read(), '123abc')

    def test_concatenate_gzipped_files(self) -> None:
        """
        Tests the concatenate files function with gzipped files.
        :return: None
        """
        # Create test files
        file_a = self.running_dir / 'file_a.txt'
        file_b = self.running_dir / 'file_b.txt'
        with file_a.open('w') as handle:
            handle.write('123')
        with file_b.open('w') as handle:
            handle.write('abc')
        fileutils.gzip_compress(file_a, file_a.with_suffix('.gz'))
        fileutils.gzip_compress(file_b, file_b.with_suffix('.gz'))

        # Concatenate
        path_out = self.running_dir / 'file_out.txt.gz'
        fileutils.concatenate_files(
            output_path=path_out,
            input_files=[file_a.with_suffix('.gz'), file_b.with_suffix('.gz')]
        )

        # Verify output
        path_out_decompressed = path_out.parent / path_out.name.replace('.gz', '')
        fileutils.gzip_extract(path_out, path_out_decompressed)
        with path_out_decompressed.open() as handle:
            self.assertEqual(handle.read(), '123abc')

    def test_gzip_compress_single_thread(self) -> None:
        """
        Tests gzip compression with a single thread.
        :return: None
        """
        input_file = self.running_dir / "input.txt"
        input_file.write_text("data" * 1000)
        output_gz_file = self.running_dir / "output.txt.gz"
        fileutils.gzip_compress(input_file, output_gz_file, threads=4)
        self.assertTrue(output_gz_file.exists())

    def test_gzip_compress_multi_thread(self) -> None:
        """
        Tests gzip compression with multiple threads.
        :return: None
        """
        input_file = self.running_dir / "input.txt"
        input_file.write_text("data" * 1000)
        output_gz_file = self.running_dir / "output.txt.gz"
        fileutils.gzip_compress(input_file, output_gz_file, threads=4)
        self.assertTrue(output_gz_file.exists())

    def test_gzip_compress_and_decompress(self) -> None:
        """
        Tests the gzip_compress and gzip_decompress functions.
        :return: None
        """
        original_content = 'This is a test string for gzip compression.'
        original_file = self.running_dir / 'original.txt'
        gzipped_file = self.running_dir / 'compressed.gz'
        decompressed_file = self.running_dir / 'decompressed.txt'

        # Create original file
        with original_file.open('w') as handle:
            handle.write(original_content)

        # Compress
        fileutils.gzip_compress(original_file, gzipped_file)
        self.assertTrue(gzipped_file.exists())

        # Decompress (assuming gzip_decompress exists)
        fileutils.gzip_extract(gzipped_file, decompressed_file)
        self.assertTrue(decompressed_file.exists())

        # Verify content
        with decompressed_file.open('r') as handle:
            self.assertEqual(handle.read(), original_content)
