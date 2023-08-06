import click, os
from higlass_data.utils import does_tool_exist
from importlib_resources import files
import higlass_data.data as data


@click.command()
@click.help_option("--help", "-h")
@click.option("-i", "--input-bed", required=True, type=str)
@click.option("-o", "--output-bw", required=True, type=str)
@click.option("-a", "--assembly", required=True, type=str)
@click.option("-l", "--num-header-lines", required=True, type=int)
def convert_bed_to_bw(
    input_bed, output_bw, assembly, num_header_lines
):
    if not does_tool_exist("bedGraphToBigWig"):
        raise Exception("bedGraphToBigWig is not installed.")
    
    chrom_sizes_path = files(data).joinpath(f"{assembly}.chromsizes")
    if not os.path.exists(chrom_sizes_path):
        raise Exception(f"Assembly {assembly} not found.")
    
    cmd = "tail -n +NUM_HEADER_LINES INPUT_BED | sort -k1,1 -k2,2n | awk '{ if (NF >= 4) print $1 \"\t\" $2 \"\t\" $3 \"\t\" $5}' > OUTPUT_BW.tmp;"
    cmd = cmd.replace("NUM_HEADER_LINES", str(num_header_lines+1))
    cmd = cmd.replace("INPUT_BED", input_bed)
    cmd = cmd.replace("OUTPUT_BW", output_bw)
    os.system(cmd)
    cmd = f"bedGraphToBigWig {output_bw}.tmp {chrom_sizes_path} {output_bw}"
    os.system(cmd)
    cmd = f"rm {output_bw}.tmp"
    os.system(cmd)



