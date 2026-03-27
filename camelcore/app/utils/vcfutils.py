from pathlib import Path

from cyvcf2 import VCF


def is_multi_sample(vcf_file: Path) -> bool:
    """
    Function to check whether a VCF file contains multiple sample
    :param vcf_file: the vcf file to be checked (with complete path)
    :return: True if is a multiple sample VCF file
    """
    with VCF(str(vcf_file)) as vcf_reader:
        return len(vcf_reader.samples) > 1


def retrieve_variants(vcf_file: Path, types: list[str] = None, excluded_types: list[str] = None):
    """
    Function to retrieve certain types of variants. Parameter
    'types' and 'excluded_types' is mutual exclusive. Either specify
    'types' to retrieved only certain variants or specify
    'excluded_types' to exclude variants.

    TYPES: 'unknown', ''indel', 'snp'
    SUBTYPES: 'tv', 'ts', 'ins', 'del'

    :param vcf_file: [optional] the vcf file to retrieve data
    :param types: [optional] types of variants to be retrieved
    :param excluded_types: types of variants to be excluded
    :return: list of records of types
    """
    types = [] if types is None else types
    excluded_types = [] if excluded_types is None else excluded_types

    if len(types) > 0 and len(excluded_types) > 0:
        raise ValueError("The parameters 'types' and 'excluded_types' are mutually exclusive. Please specify only one.")

    vcf_reader = VCF(str(vcf_file))
    records = []
    if len(types) > 0:
        # only set types
        for rcd in vcf_reader:
            if any(x in types for x in [rcd.var_type, rcd.var_subtype]):
                records.append(rcd)
    elif len(excluded_types) > 0:
        # only set excluded_types
        for rcd in vcf_reader:
            if all(x not in excluded_types for x in [rcd.var_type, rcd.var_subtype]):
                records.append(rcd)
    else:
        # no conditions
        records = list(vcf_reader)
    return records


def count_variants(vcf_file: Path, include_filtered: bool = False) -> int:
    """
    Counts the number of variants in a VCF file.
    :param vcf_file: Path to the VCF file.
    :param include_filtered: If True, counts all variants; if False, counts only PASS variants.
    :return: Number of variants
    """
    with VCF(str(vcf_file)) as vcf_reader:
        for row in vcf_reader:
            print(row)
            print(row.FILTER)
    with VCF(str(vcf_file)) as vcf_reader:
        return sum(1 for variant in vcf_reader if include_filtered or variant.FILTER is None)
