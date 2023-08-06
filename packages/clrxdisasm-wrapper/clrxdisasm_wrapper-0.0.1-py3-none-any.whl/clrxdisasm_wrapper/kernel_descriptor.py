from struct import unpack

from construct import (BitsInteger, BitStruct, Bitwise, Bytewise, Const, Flag,
                       Int32ul, Int64ul, Padding, Struct)

__COMPUTE_PGM_RSRC1 = Struct(
    "GRANULATED_WORKITEM_VGPR_COUNT" / BitsInteger(6),
    "GRANULATED_WAVEFRONT_SGPR_COUNT" / BitsInteger(4),
    "PRIORITY" / BitsInteger(2),
    "FLOAT_ROUND_MODE_32" / BitsInteger(2),
    "FLOAT_ROUND_MODE_16_64" / BitsInteger(2),
    "FLOAT_DENORM_MODE_32" / BitsInteger(2),
    "FLOAT_DENORM_MODE_16_64" / BitsInteger(2),
    "PRIV" / BitsInteger(1),
    "ENABLE_DX10_CLAMP" / BitsInteger(1),
    "DEBUG_MODE" / BitsInteger(1),
    "ENABLE_IEEE_MODE" / BitsInteger(1),
    "BULKY" / BitsInteger(1),
    "CDBG_USER" / BitsInteger(1),
    "FP16_OVFL" / BitsInteger(1),
    Padding(2),
    "WGP_MODE" / BitsInteger(1),
    "MEM_ORDERED" / BitsInteger(1),
    "FWD_PROGRESS" / BitsInteger(1),
)

__COMPUTE_PGM_RSRC2 = Struct(
    "ENABLE_PRIVATE_SEGMENT" / BitsInteger(1),
    "USER_SGPR_COUNT" / BitsInteger(5),
    "ENABLE_TRAP_HANDLER" / BitsInteger(1),
    "ENABLE_SGPR_WORKGROUP_ID_X" / BitsInteger(1),
    "ENABLE_SGPR_WORKGROUP_ID_Y" / BitsInteger(1),
    "ENABLE_SGPR_WORKGROUP_ID_Z" / BitsInteger(1),
    "ENABLE_SGPR_WORKGROUP_INFO" / BitsInteger(1),
    "ENABLE_VGPR_WORKITEM_ID" / BitsInteger(2),
    "ENABLE_EXCEPTION_ADDRESS_WATCH" / BitsInteger(1),
    "ENABLE_EXCEPTION_MEMORY" / BitsInteger(1),
    "GRANULATED_LDS_SIZE" / BitsInteger(9),
    "ENABLE_EXCEPTION_IEEE_754_FP_INVALID_OPERATION" / BitsInteger(1),
    "ENABLE_EXCEPTION_FP_DENORMAL_SOURCE" / BitsInteger(1),
    "ENABLE_EXCEPTION_IEEE_754_FP_DIVISION_BY_ZERO" / BitsInteger(1),
    "ENABLE_EXCEPTION_IEEE_754_FP_OVERFLOW" / BitsInteger(1),
    "ENABLE_EXCEPTION_IEEE_754_FP_UNDERFLOW" / BitsInteger(1),
    "ENABLE_EXCEPTION_IEEE_754_FP_INEXACT" / BitsInteger(1),
    "ENABLE_EXCEPTION_INT_DIVIDE_BY_ZERO" / BitsInteger(1),
    Padding(1),
)

__COMPUTE_PGM_RSRC3 = Struct(
    "SHARED_VGPR_COUNT" / BitsInteger(4),
    "INST_PREF_SIZE" / BitsInteger(6),
    "TRAP_ON_START" / BitsInteger(1),
    "TRAP_ON_END" / BitsInteger(1),
    Padding(19),
    "IMAGE_OP" / BitsInteger(1),
)

__KERNEL_DESCRIPTOR = BitStruct(
    "GROUP_SEGMENT_FIXED_SIZE" / Bytewise(Int32ul),
    "PRIVATE_SEGMENT_FIXED_SIZE" / Bytewise(Int32ul),
    "KERNARG_SIZE" / Bytewise(Int32ul),
    Const(b"\x00" * 4 * 8),
    "KERNEL_CODE_ENTRY_BYTE_OFFSET" / Bytewise(Int64ul),
    Const(b"\x00" * 20 * 8),
    "COMPUTE_PGM_RSRC3" / __COMPUTE_PGM_RSRC3,
    "COMPUTE_PGM_RSRC1" / __COMPUTE_PGM_RSRC1,
    "COMPUTE_PGM_RSRC2" / __COMPUTE_PGM_RSRC2,
    Const(b"\x00" * 1),
    "ENABLE_SGPR_PRIVATE_SEGMENT_SIZE" / Flag,
    "ENABLE_SGPR_FLAT_SCRATCH_INIT" / Flag,
    "ENABLE_SGPR_DISPATCH_ID" / Flag,
    "ENABLE_SGPR_KERNARG_SEGMENT_PTR" / Flag,
    "ENABLE_SGPR_QUEUE_PTR" / Flag,
    "ENABLE_SGPR_DISPATCH_PTR" / Flag,
    "ENABLE_SGPR_PRIVATE_SEGMENT_BUFFER" / Flag,
    Const(b"\x00" * 4),
    "USES_DYNAMIC_STACK" / Flag,
    "ENABLE_WAVEFRONT_SIZE32" / Flag,
    Const(b"\x00" * 2),
    Const(b"\x00" * 6 * 8),
)


def __compute_pgm_rsrc1(self):
    struct = self["COMPUTE_PGM_RSRC1"]
    return unpack("<I", Bitwise(__COMPUTE_PGM_RSRC1).build(struct))[0]


def __compute_pgm_rsrc2(self):
    struct = self["COMPUTE_PGM_RSRC2"]
    return unpack("<I", Bitwise(__COMPUTE_PGM_RSRC2).build(struct))[0]


def __compute_pgm_rsrc3(self):
    struct = self["COMPUTE_PGM_RSRC3"]
    return unpack("<I", Bitwise(__COMPUTE_PGM_RSRC3).build(struct))[0]


def unpack_kernel_descriptor(data: bytes):
    kd = __KERNEL_DESCRIPTOR.parse(data)
    kd.compute_pgm_rsrc1 = __compute_pgm_rsrc1.__get__(kd)
    kd.compute_pgm_rsrc2 = __compute_pgm_rsrc2.__get__(kd)
    kd.compute_pgm_rsrc3 = __compute_pgm_rsrc3.__get__(kd)
    return kd


def unpack_kernel_descriptors(data: bytes):
    for i in range(0, len(data), __KERNEL_DESCRIPTOR.sizeof()):
        yield unpack_kernel_descriptor(data[i:i + __KERNEL_DESCRIPTOR.sizeof()])
