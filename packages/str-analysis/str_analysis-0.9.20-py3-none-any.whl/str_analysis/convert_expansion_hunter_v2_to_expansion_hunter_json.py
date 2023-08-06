"""This script converts ExpansionHunter v2 output .json to the .json format ExpansionHunter v5 uses to output results.
This makes it easier to pass these results to downstream scripts.
"""

"""
ExpansionHunter v2 format:
{
    "1-101334163-101334198-AAAAC": {
        "AnchoredIrrCount": 0,
        "Genotype": "6/6",
        "GenotypeCi": "6-6/6-6",
        "GenotypeSupport": "8-6-0/8-6-0",
        "IrrCount": 0,
        "RepeatId": "1-101334163-101334198-AAAAC",
        "RepeatSizes": {
            "Repeat1": {
                "NumSupportingReads": 8,
                "Size": 6,
                "Source": "SPANNING"
            }
        },
        "RepeatUnit": "AAAAC",
        "TargetRegion": "chr1:101334164-101334198",
        "UnalignedIrrCount": 0
    },
...
}
"""

"""
ExpansionHunter output format:

  "LocusResults": {
        "chr12-57610122-57610131-GCA": {
          "AlleleCount": 2,
          "Coverage": 50.469442942130875,
          "FragmentLength": 433,
          "LocusId": "chr12-57610122-57610131-GCA",
          "ReadLength": 151,
          "Variants": {
            "chr12-57610122-57610131-GCA": {
              "CountsOfFlankingReads": "(1, 1), (2, 4)",
              "CountsOfInrepeatReads": "()",
              "CountsOfSpanningReads": "(2, 1), (3, 48), (6, 1)",
              "Genotype": "3/3",
              "GenotypeConfidenceInterval": "3-3/3-3",
              "ReferenceRegion": "chr12:57610122-57610131",
              "RepeatUnit": "GCA",
              "VariantId": "chr12-57610122-57610131-GCA",
              "VariantSubtype": "Repeat",
              "VariantType": "Repeat"
            }
          }
        },

  "SampleParameters": {
        "SampleId": "NA19239",
        "Sex": "Female"
  }
"""


import argparse
import json
import re


def main():
    p = argparse.ArgumentParser()
    p.add_argument("json_path", nargs="+", help="ExpansionHunter v2 json path(s)")
    args = p.parse_args()

    for json_path in args.json_path:
        print(f"Processing {json_path}")
        locus_results = process_expansion_hunter_v2_json(json_path)

        output_json_path = json_path.replace(".json", "").replace(".gz", "") + ".eh.json"
        print(f"Writing results for", len(locus_results["LocusResults"]), f"loci to {output_json_path}")
        with open(output_json_path, "wt") as f:
            json.dump(locus_results, f, indent=3)


def process_expansion_hunter_v2_json(json_path):
    locus_results = {
        "LocusResults": {},
        "SampleParameters": {
            "SampleId": None,
            "Sex": None,
        },
    }

    with open(json_path, "rt") as f:
        data = json.load(f)

        if "BamStats" in data:
            #median_coverage = data["BamStats"]["MedianCoverage"]
            #read_length = data["BamStats"]["ReadLength"]
            del data["BamStats"]

        for locus_id, locus_data in data.items():

            try:
                chrom, start_1based, end_1based = re.split("[:-]", locus_data["TargetRegion"])
            except KeyError as e:
                print(f"ERROR: {e} in {locus_data}")
                continue

            start_1based = int(start_1based)
            end_1based = int(end_1based)

            coverage = sum([v["NumSupportingReads"] for v in locus_data["RepeatSizes"].values()])
            genotypes = locus_data["Genotype"].split("/")
            is_hom = len(set(genotypes)) == 1
            genotype_support = locus_data["GenotypeSupport"].split("/")
            if is_hom:
                spanning_read_count, flanking_read_count, irr_read_count = genotype_support[0].split("-")
            else:
                spanning_read_count1, flanking_read_count1, irr_read_count1 = genotype_support[0].split("-")
                spanning_read_count2, flanking_read_count2, irr_read_count2 = genotype_support[1].split("-")
                spanning_read_count = int(spanning_read_count1) + int(spanning_read_count2)
                flanking_read_count = int(flanking_read_count1) + int(flanking_read_count2)
                irr_read_count = int(irr_read_count1) + int(irr_read_count2)

            locus_results["LocusResults"][locus_id] = {
                "AlleleCount": 2,
                "LocusId": locus_id,
                "Coverage": coverage,  #10.757737459978655,
                "ReadLength": None,
                "FragmentLength": None,
                "Variants": {
                    locus_id: {
                        "Genotype": locus_data["Genotype"],
                        "GenotypeConfidenceInterval": locus_data["GenotypeCi"],
                        "ReferenceRegion": f"{chrom}:{start_1based - 1}-{end_1based}",
                        "RepeatUnit": locus_data["RepeatUnit"],
                        "VariantId": locus_id,
                        "VariantSubtype": "Repeat",
                        "VariantType": "Repeat",

                        "CountsOfFlankingReads": f"({genotypes[0]}, {spanning_read_count})",
                        "CountsOfInrepeatReads": f"({genotypes[0]}, {flanking_read_count})",
                        "CountsOfSpanningReads": f"({genotypes[0]}, {irr_read_count})",
                    }
                },
            }

    return locus_results


if __name__ == "__main__":
    main()
