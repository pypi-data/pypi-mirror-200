from dataclasses import dataclass

from ormsgpack import unpackb

__AMDHSA_VERSION: str = 'amdhsa.version'
__AMDHSA_KERNELS: str = 'amdhsa.kernels'
__AMDHSA_TARGET: str = 'amdhsa.target'

__AMDHSA_VERSION_VALUES: dict[int, list[int]] = {
    3: [1, 0],
    4: [1, 1],
    5: [1, 2],
}


@dataclass
class KernelArgumentMetadata:
    data: dict
    name: str | None
    type_name: str | None
    size: int
    offset: int
    value_kind: str
    pointee_align: int | None
    address_space: str | None
    access: str | None
    actual_access: str | None
    is_const: bool | None
    is_restrict: bool | None
    is_volatile: bool | None
    is_pipe: bool | None


@dataclass
class KernelMetadata:
    """AMDHSA Kernel Metadata.

    Attributes:
        name (str)
        symbol (str)
        language (:obj:`str`, optional)
        language_version (:obj:`list[int]`, optional)
        args (:obj:`list[KernelArgumentMetadata]`, optional)
        reqd_workgroup_size (:obj:`list[int]`, optional)
        workgroup_size_hint (:obj:`list[int]`, optional)
        vec_type_hint (:obj:`str`, optional)
        device_enqueue_symbol (:obj:`str`, optional)
        kernarg_segment_size (int)
        group_segment_fixed_size (int)
        private_segment_fixed_size (int)
        kernarg_segment_align (int)
        wavefront_size (int)
        sgpr_count (int)
        vgpr_count (int)
        max_flat_workgroup_size (int)
        sgpr_spill_count (:obj:`int`, optional)
        vgpr_spill_count (:obj:`int`, optional)
        kind (:obj:`str`, optional)
    """
    name: str
    symbol: str
    language: str | None
    language_version: list[int] | None
    args: list[KernelArgumentMetadata] | None
    reqd_workgroup_size: list[int] | None
    workgroup_size_hint: list[int] | None
    vec_type_hint: str | None
    device_enqueue_symbol: str | None
    kernarg_segment_size: int
    group_segment_fixed_size: int
    private_segment_fixed_size: int
    kernarg_segment_align: int
    wavefront_size: int
    sgpr_count: int
    vgpr_count: int
    max_flat_workgroup_size: int
    sgpr_spill_count: int | None
    vgpr_spill_count: int | None
    kind: str | None


@dataclass
class Metadata:
    amdhsa_version: list[int]
    amdhsa_kernels: list[KernelMetadata]
    amdhsa_target: str


def __parse_str(data: dict, name: str) -> str:
    res: str = data[name]
    assert isinstance(res, str)
    return res


def __parse_str_opt(data: dict, name: str) -> str | None:
    res: str | None = data.get(name)
    assert isinstance(res, str) or res is None
    return res


def __parse_int(data: dict, name: str) -> int:
    res: int = data[name]
    assert isinstance(res, int)
    return res


def __parse_int_opt(data: dict, name: str) -> int | None:
    res: int | None = data.get(name)
    assert isinstance(res, int) or res is None
    return res


def __parse_bool_opt(data: dict, name: str) -> bool | None:
    res: bool | None = data.get(name)
    assert isinstance(res, bool) or res is None
    return res


def __parse_int_seq_opt(data: dict, name: str, size: int) -> list[int] | None:
    res: list[int] | None = data.get(name)
    assert res is None \
           or isinstance(res, list) \
           and len(res) == size \
           and all(isinstance(r, int) for r in res)
    return res


def __parse_amdhsa_kernel_arg(data: dict) -> KernelArgumentMetadata:
    return KernelArgumentMetadata(
        data,
        __parse_str_opt(data, '.name'),
        __parse_str_opt(data, '.type_name'),
        __parse_int(data, '.size'),
        __parse_int(data, '.offset'),
        __parse_str(data, '.value_kind'),
        __parse_int_opt(data, '.pointee_align'),
        __parse_str_opt(data, '.address_space'),
        __parse_str_opt(data, '.access'),
        __parse_str_opt(data, '.actual_access'),
        __parse_bool_opt(data, '.is_const'),
        __parse_bool_opt(data, '.is_restrict'),
        __parse_bool_opt(data, '.is_volatile'),
        __parse_bool_opt(data, '.is_pipe'),
    )


def __parse_kernel_args(data: dict) -> list[KernelArgumentMetadata] | None:
    args: list[dict] | None = data.get(".args")
    if args is None:
        return None
    assert isinstance(args, list) \
           and all(isinstance(r, dict) for r in args)
    return [__parse_amdhsa_kernel_arg(arg) for arg in args]


def __parse_kernel(data: dict) -> KernelMetadata:
    try:
        assert isinstance(data, dict)
        return KernelMetadata(
            __parse_str(data, '.name'),
            __parse_str(data, '.symbol'),
            __parse_str_opt(data, '.language'),
            __parse_int_seq_opt(data, '.language_version', 2),
            __parse_kernel_args(data),
            __parse_int_seq_opt(data, '.reqd_workgroup_size', 3),
            __parse_int_seq_opt(data, '.workgroup_size_hint', 3),
            __parse_str_opt(data, '.vec_type_hint'),
            __parse_str_opt(data, '.device_enqueue_symbol'),
            __parse_int(data, '.kernarg_segment_size'),
            __parse_int(data, '.group_segment_fixed_size'),
            __parse_int(data, '.private_segment_fixed_size'),
            __parse_int(data, '.kernarg_segment_align'),
            __parse_int(data, '.wavefront_size'),
            __parse_int(data, '.sgpr_count'),
            __parse_int(data, '.vgpr_count'),
            __parse_int(data, '.max_flat_workgroup_size'),
            __parse_int_opt(data, '.sgpr_spill_count'),
            __parse_int_opt(data, '.vgpr_spill_count'),
            __parse_str_opt(data, '.kind'),
        )
    except (KeyError, AssertionError) as exc:
        raise AssertionError('bad kernel metadata format') from exc


def __parse_amdhsa_version(data: dict, co_ver: int) -> list[int]:
    assert __AMDHSA_VERSION in data, \
        f'bad metadata format: no "{__AMDHSA_VERSION}" field'
    amdhsa_version: list[int] = data[__AMDHSA_VERSION]
    assert isinstance(amdhsa_version, list), \
        f'bad metadata format: bad format of "{__AMDHSA_VERSION}" field'
    assert amdhsa_version == __AMDHSA_VERSION_VALUES[co_ver], \
        'bad file: elf and metadata code object versions do not match'
    return amdhsa_version


def __parse_amdhsa_kernels(data: dict) -> list[KernelMetadata]:
    assert __AMDHSA_KERNELS in data, \
        f'bad metadata format: no "{__AMDHSA_KERNELS}" field'
    amdhsa_kernels: list[dict] = data[__AMDHSA_KERNELS]
    assert isinstance(amdhsa_kernels, list), \
        f'bad metadata format: bad format of "{__AMDHSA_KERNELS}" field'
    return [__parse_kernel(kernel) for kernel in amdhsa_kernels]


def __parse_amdhsa_target(data: dict, co_ver: int) -> str:
    assert __AMDHSA_TARGET in data or co_ver < 4, \
        f'bad metadata format: no "{__AMDHSA_TARGET}" field'
    amdhsa_target: str = '' if co_ver < 4 else data[__AMDHSA_TARGET]
    assert isinstance(amdhsa_target, str), \
        f'bad metadata format: bad format of "{__AMDHSA_TARGET}" field'
    return amdhsa_target


def __parse_metadata(metadata: dict, co_ver: int) -> Metadata:
    return Metadata(
        __parse_amdhsa_version(metadata, co_ver),
        __parse_amdhsa_kernels(metadata),
        __parse_amdhsa_target(metadata, co_ver),
    )


def __unpack_metadata(data: bytes) -> dict:
    metadata: dict = unpackb(data)
    assert isinstance(metadata, dict), 'bad metadata format'
    return metadata


def unpack_metadata(data: bytes, co_ver: int) -> Metadata:
    metadata: dict = __unpack_metadata(data)
    return __parse_metadata(metadata, co_ver)
