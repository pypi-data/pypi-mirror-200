import argparse
import io
import sys

from .clrxdisasm_utils import run_clrxdisasm
from .elf_utils import extract_elf
from .kernel_descriptor import unpack_kernel_descriptors
from .metadata import unpack_metadata
from .output_generator import generate_config, generate_prefix, generate_text


def main(filename, clrxdisasm):
    with io.StringIO() as stdout:
        with open(f"{filename}", 'rb') as stdin:
            co_ver, arch, metadata, rodata, text = extract_elf(stdin)

        metadata = unpack_metadata(metadata, co_ver)
        kernel_descriptors = unpack_kernel_descriptors(rodata)
        wavefront_size = metadata.amdhsa_kernels[0].wavefront_size
        text = run_clrxdisasm(clrxdisasm, arch[:-2], wavefront_size, filename, text)
        kernels_names = [kernel.name for kernel in metadata.amdhsa_kernels]

        generate_prefix(filename, arch, stdout)
        generate_config(metadata, kernel_descriptors, stdout)
        generate_text(text, kernels_names, stdout)

        return stdout.getvalue()


def start_point():
    parser = argparse.ArgumentParser('clrxdisasm-wrapper')
    parser.add_argument('input_file', help='path to input binary file')
    parser.add_argument('clrxdisasm', help='path to clrxdisasm')
    namespace = parser.parse_args(sys.argv[1:])
    print(main(namespace.input_file, namespace.clrxdisasm))


start_point()
