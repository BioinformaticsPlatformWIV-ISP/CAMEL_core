from camelcore.app.testsuite import TestSuite
from camelcore.app.utils import vcfutils


class TestVCFUtils(TestSuite):
    """
    Contains tests for the vcfutils module.
    """

    def test_is_multi_sample(self) -> None:
        """
        Tests the is_multi_sample function.
        :return: None
        """
        path_vcf_single = TestSuite.get_test_file('variants-filt.vcf.gz')
        self.assertFalse(vcfutils.is_multi_sample(path_vcf_single))

    def test_count_variants(self) -> None:
        """
        Tests the count_variants function.
        :return: None
        """
        path_vcf = TestSuite.get_test_file('variants-filt.vcf.gz')

        # Count variants
        count = vcfutils.count_variants(path_vcf, include_filtered=True)
        self.assertIsInstance(count, int)
        self.assertGreaterEqual(count, 0)

        # Count variants passing filtering
        count_without_filtered = vcfutils.count_variants(path_vcf, include_filtered=False)
        self.assertIsInstance(count_without_filtered, int)
        self.assertGreater(count, count_without_filtered)
