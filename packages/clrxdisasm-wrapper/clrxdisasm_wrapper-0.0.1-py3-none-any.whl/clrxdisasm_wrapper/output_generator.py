import io
import re

from .metadata import KernelArgumentMetadata, KernelMetadata, Metadata


def __generate_kernel_descriptor_config(descriptor, stdout: io.StringIO):
    dims = "xyz"[:1 + descriptor.COMPUTE_PGM_RSRC2.ENABLE_VGPR_WORKITEM_ID]
    shared_vgprs = descriptor.COMPUTE_PGM_RSRC3.SHARED_VGPR_COUNT
    dx10clamp = descriptor.COMPUTE_PGM_RSRC1.ENABLE_DX10_CLAMP
    ieeemode = descriptor.COMPUTE_PGM_RSRC1.ENABLE_IEEE_MODE
    priority = descriptor.COMPUTE_PGM_RSRC1.PRIORITY
    pgmrsrc1 = descriptor.compute_pgm_rsrc1()
    pgmrsrc2 = descriptor.compute_pgm_rsrc2()
    pgmrsrc3 = descriptor.compute_pgm_rsrc3()
    group_segment_fixed_size = descriptor.GROUP_SEGMENT_FIXED_SIZE
    private_segment_fixed_size = descriptor.PRIVATE_SEGMENT_FIXED_SIZE
    kernel_code_entry_offset = descriptor.KERNEL_CODE_ENTRY_BYTE_OFFSET
    use_private_segment_buffer = descriptor.ENABLE_SGPR_PRIVATE_SEGMENT_BUFFER
    use_dispatch_ptr = descriptor.ENABLE_SGPR_DISPATCH_PTR
    use_kernarg_segment_ptr = descriptor.ENABLE_SGPR_KERNARG_SEGMENT_PTR
    use_wave32 = descriptor.ENABLE_WAVEFRONT_SIZE32

    stdout.write('    .config\n')
    stdout.write(f'        .dims {dims}\n')
    stdout.write(f'        .shared_vgprs {shared_vgprs}\n')
    if dx10clamp:
        stdout.write('        .dx10clamp\n')
    if ieeemode:
        stdout.write('        .ieeemode\n')
    stdout.write(f'        .priority {priority}\n')
    stdout.write(f'        .pgmrsrc1 0x{pgmrsrc1:0>8x}\n')
    stdout.write(f'        .pgmrsrc2 0x{pgmrsrc2:0>8x}\n')
    stdout.write(f'        .pgmrsrc3 0x{pgmrsrc3:0>8x}\n')
    stdout.write(f'        .group_segment_fixed_size {group_segment_fixed_size}\n')
    stdout.write(f'        .private_segment_fixed_size {private_segment_fixed_size}\n')
    stdout.write(f'        .kernel_code_entry_offset 0x{kernel_code_entry_offset:x}\n')
    if use_private_segment_buffer:
        stdout.write('        .use_private_segment_buffer\n')
    if use_dispatch_ptr:
        stdout.write('        .use_dispatch_ptr\n')
    if use_kernarg_segment_ptr:
        stdout.write('        .use_kernarg_segment_ptr\n')
    if use_wave32:
        stdout.write('        .use_wave32\n')


def __generate_kernel_arg_value_kind(value_kind: str) -> str:
    return {
        'hidden_none': 'none',
        'hidden_global_offset_z': 'goz',
        'hidden_global_offset_y': 'goy',
        'hidden_global_offset_x': 'gox',
        'by_value': 'value',
        'global_buffer': 'globalbuf',
    }.get(value_kind, value_kind)


def __generate_kernel_arg(arg: KernelArgumentMetadata, stdout: io.StringIO):
    value_kind = __generate_kernel_arg_value_kind(arg.value_kind)
    address_space = "" if arg.address_space is None else arg.address_space
    address_space = __generate_kernel_arg_value_kind(address_space)
    if value_kind == 'globalbuf' and address_space == 'global':
        struct_ = 'struct, global, default'
    else:
        struct_ = 'struct'
    stdout.write(f'        .arg {"" if arg.name is None else arg.name}')
    stdout.write(f', "{"" if arg.type_name is None else arg.type_name}"')
    stdout.write(f', {arg.size}')
    stdout.write(f', {arg.offset}')
    stdout.write(f', {value_kind}')
    stdout.write(f', {struct_}')
    stdout.write('\n')


def __generate_kernel_metadata_config(metadata: KernelMetadata,
                                      stdout: io.StringIO):
    language_version = ", ".join(map(str, metadata.language_version))
    reqd_work_group_size = ", ".join(map(str, metadata.reqd_workgroup_size))
    stdout.write("    .config\n")
    stdout.write(f'        .md_symname "{metadata.symbol}"\n')
    stdout.write(f'        .md_language "{metadata.language}", {language_version}\n')
    stdout.write(f'        .reqd_work_group_size {reqd_work_group_size}\n', )
    stdout.write(f"        .md_kernarg_segment_size {metadata.kernarg_segment_size}\n")
    stdout.write(f"        .md_kernarg_segment_align {metadata.kernarg_segment_align}\n")
    stdout.write(f"        .md_group_segment_fixed_size {metadata.group_segment_fixed_size}\n")
    stdout.write(f"        .md_private_segment_fixed_size {metadata.private_segment_fixed_size}\n")
    stdout.write(f"        .md_wavefront_size {metadata.wavefront_size}\n")
    stdout.write(f"        .md_sgprsnum {metadata.sgpr_count}\n")
    stdout.write(f"        .md_vgprsnum {metadata.vgpr_count}\n")
    stdout.write(f"        .spilledsgprs {metadata.sgpr_spill_count}\n")
    stdout.write(f"        .spilledvgprs {metadata.vgpr_spill_count}\n")
    stdout.write(f"        .max_flat_work_group_size {metadata.max_flat_workgroup_size}\n")
    for arg in metadata.args:
        __generate_kernel_arg(arg, stdout)


def __generate_kernel_config(metadata: KernelMetadata,
                             descriptor,
                             stdout: io.StringIO):
    stdout.write(f'.kernel {metadata.name}\n')
    __generate_kernel_descriptor_config(descriptor, stdout)
    __generate_kernel_metadata_config(metadata, stdout)


def generate_prefix(filename, arch, stdout: io.StringIO):
    stdout.write(f"/* Disassembling '{filename}' */\n")
    stdout.write(f'.gpu {arch.upper()}\n')
    stdout.write(f'.arch_minor {arch[-2]}\n')
    stdout.write(f'.arch_stepping {arch[-1]}\n')


def generate_config(metadata: Metadata,
                    kernel_descriptors: list,
                    stdout: io.StringIO):
    md_version = ", ".join(map(str, metadata.amdhsa_version))
    stdout.write(f'.md_version {md_version}\n')
    for kernel_metadata, kernel_descriptor \
            in zip(metadata.amdhsa_kernels, kernel_descriptors):
        __generate_kernel_config(kernel_metadata, kernel_descriptor, stdout)


def generate_text(text, kernels_names, stdout: io.StringIO):
    text_it = iter(text)
    while next(text_it, ".text") != ".text":
        pass
    stdout.write('.text\n')
    kernels_names = iter(kernels_names)
    print_name = True
    for line in text_it:
        line = line.strip()
        if re.fullmatch(r"^/\*[0-9a-fA-F]+\*/\s+s_endpgm$", line):
            print_name = True
        elif print_name and not re.match(r"^/\*[0-9a-fA-F]+\*/\s+(s_nop\s+0x[0-9a-fA-F]+|s_code_end)$", line):
            stdout.write(f'{next(kernels_names, None)}:\n')
            print_name = False
        stdout.write(f'{line}\n')
