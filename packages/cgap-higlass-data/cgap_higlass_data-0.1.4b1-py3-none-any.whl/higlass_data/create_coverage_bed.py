import click
import pandas as pd
import vcf
import negspy.coordinates as nc

TILE_SIZE = 1024  # Higlass tile size for 1D tracks
MAX_ZOOM_LEVEL = 23


class Coverage:

    input_filepath = ""
    output_filepath = ""
    chromosomes = []
    variants = []
    variants_multires = []
    variants_df = []
    variants_by_id = {}
    tile_sizes = []
    chrom_info = ""
    quiet = True

    def __init__(
        self,
        input_filepath,
        output_filepath,
        assembly,
        quiet,
    ):
        self.input_filepath = input_filepath
        self.output_filepath = output_filepath
        self.quiet = quiet
        self.variants = self.load_variants()
        self.chromosomes = self.get_chromosomes()
        self.tile_sizes = [TILE_SIZE * (2**i) for i in range(0, MAX_ZOOM_LEVEL)]
        self.chrom_info = nc.get_chrominfo(assembly)

    def load_variants(self):
        if not self.quiet:
            print("Loading variants...")
        variants = []
        vcf_reader = vcf.Reader(open(self.input_filepath, "r"))

        for record in vcf_reader:
            variants.append(record)

        if not self.quiet:
            print("Loading variants complete.")
        return variants

    # Create a matrix of the data that we use for filtering
    def create_variants_dataframe(self):
        chromosomes = []
        ids = []
        pos = []
        absPos = []

        if not self.quiet:
            print("Creating data frame for easy querying during aggregation.")

        for variant in self.variants:

            chromosomes.append(variant.CHROM)
            ids.append(variant.ID)
            pos.append(variant.POS)
            absPos.append(
                nc.chr_pos_to_genome_pos(variant.CHROM, variant.POS, self.chrom_info)
            )

        d = {
            "chr": chromosomes,
            "id": ids,
            "pos": pos,
            "absPos": absPos
        }
        self.variants_df = pd.DataFrame(data=d)

    def get_chromosomes(self):
        if not self.quiet:
            print("Extracting chromosomes...")
        chrs = list(set(map(lambda v: v.CHROM, self.variants)))
        if "chrM" in chrs:
            chrs.remove("chrM")
        chrs.sort()
        if not self.quiet:
            print("Chromosomes used: ", chrs)
        return chrs

    def create_coverage_bed(self):
        self.create_variants_dataframe()

        with open(self.output_filepath, "w") as output:

            for chr in self.chromosomes:
                current_pos = 0
                current_index = 0
                chr_variants = self.variants_df[self.variants_df.chr == chr]
                last_pos = chr_variants["pos"].iloc[-1]
                while current_pos < last_pos:
                    new_index = current_index + 1
                    new_pos = TILE_SIZE * new_index
                    variants_in_bin = chr_variants[
                        (chr_variants.pos >= current_pos) & (chr_variants.pos < new_pos)
                    ]
                    num_variants_in_bin = len(variants_in_bin.index)
                    line = f"{chr}\t{current_pos}\t{new_pos}\t.\t{num_variants_in_bin}\n"
                    output.write(line)
                    current_index = new_index
                    current_pos = new_pos

    

@click.command()
@click.help_option("--help", "-h")
@click.option("-i", "--input-vcf", required=True, type=str)
@click.option("-o", "--output-bed", required=True, type=str)
@click.option("-a", "--assembly", required=True, type=str)
@click.option("-q", "--quiet", required=False, default=True, type=bool)
def create_coverage_bed(
    input_vcf, output_bed, assembly, quiet
):
    input_filepath = input_vcf
    output_bed_filepath = output_bed

    cov = Coverage(
        input_filepath,
        output_bed_filepath,
        assembly,
        quiet,
    )

    cov.create_coverage_bed()


if __name__ == "__main__":
    create_coverage_bed()
