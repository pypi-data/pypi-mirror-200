from typing import BinaryIO

from elftools.elf.elffile import ELFFile
from elftools.elf.sections import NoteSection, Section

__EI_ABIVERSION: int = 8
__ELFABIVERSION_AMDGPU_HSA_V3: int = 1
__ELFABIVERSION_AMDGPU_HSA_V4: int = 2
__ELFABIVERSION_AMDGPU_HSA_V5: int = 3
__CODE_OBJECT_VERSION: dict[int, int] = {
    __ELFABIVERSION_AMDGPU_HSA_V3: 3,
    __ELFABIVERSION_AMDGPU_HSA_V4: 4,
    __ELFABIVERSION_AMDGPU_HSA_V5: 5,
}

__EF_AMDGPU_MACH_MASK: int = 0x0ff
__EF_AMDGPU_MACH: dict[int, str] = {
    # RDNA
    0x033: 'gfx1010',
    0x034: 'gfx1011',
    0x035: 'gfx1012',
    0x042: 'gfx1013',
    # RDNA2
    0x036: 'gfx1030',
    0x037: 'gfx1031',
    0x038: 'gfx1032',
    0x039: 'gfx1033',
    0x03e: 'gfx1034',
    0x03d: 'gfx1035',
    0x045: 'gfx1036',
    # RDNA3
    0x041: 'gfx1100',
    0x046: 'gfx1101',
    0x047: 'gfx1102',
    0x044: 'gfx1103',
}

__NT_AMDGPU_METADATA: int = 32


def __extract_code_object_version(elf: ELFFile) -> int:
    e_ident: bytes = elf.e_ident_raw
    abi_ver: int = e_ident[__EI_ABIVERSION]
    co_ver: int | None = __CODE_OBJECT_VERSION.get(abi_ver)
    assert co_ver is not None, \
        f'unknown code object version: e_ident[EI_ABIVERSION] == {abi_ver}'
    return co_ver


def __extract_arch(elf: ELFFile) -> str:
    e_flags: int = elf.header['e_flags']
    mach: int = e_flags & __EF_AMDGPU_MACH_MASK
    arch: str | None = __EF_AMDGPU_MACH.get(mach)
    assert arch is not None, f'unknown target arch: {mach}'
    return arch


def __extract_metadata(elf: ELFFile) -> bytes:
    note_section: NoteSection = elf.get_section_by_name('.note')
    assert isinstance(note_section, NoteSection), \
        'bad binary format: missed ".note" section'
    notes: list[bytes] = [note.n_desc
                          for note in note_section.iter_notes()
                          if note.n_name == 'AMDGPU'
                          and note.n_type == __NT_AMDGPU_METADATA]
    assert len(notes) == 1, \
        'bad binary format: bad ".note" section'
    return notes[0]


def __extract_section(elf: ELFFile, name: str) -> bytes:
    section: Section = elf.get_section_by_name(name)
    assert isinstance(section, Section), \
        f'bad binary format: missed {name} section'
    return section.data()


def __extract_rodata(elf: ELFFile) -> bytes:
    return __extract_section(elf, '.rodata')


def __extract_text(elf: ELFFile) -> bytes:
    return __extract_section(elf, '.text')


def extract_elf(stream: BinaryIO) -> (int, str, bytes, bytes, bytes):
    elf: ELFFile = ELFFile(stream)
    assert isinstance(elf, ELFFile), 'bad binary format: not an ELF'
    co_ver: int = __extract_code_object_version(elf)
    arch: str = __extract_arch(elf)
    metadata: bytes = __extract_metadata(elf)
    rodata: bytes = __extract_rodata(elf)
    text: bytes = __extract_text(elf)
    return co_ver, arch, metadata, rodata, text
