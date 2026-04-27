from __future__ import annotations

import keyword
import re
from pathlib import Path
from typing import Any

import yaml


# -------------------------
# Registry for exports
# -------------------------

_GENERATED_FUNCTIONS: list[str] = []
_GENERATED_STRUCTS: list[str] = []


def to_snake_case(name: str) -> str:
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    s2 = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1)
    result = s2.lower().strip("_")
    if keyword.iskeyword(result):
        result += "_"
    return result


def python_type_expr(type_expr: str, defined_struct_names: set[str]) -> str:
    """
    Convert a ctypes/wintypes expression into a Python-facing annotation string
    for the generated wrapper signatures.
    """
    mapping = {
        "ctypes.c_bool": "bool",
        "wintypes.BOOL": "bool",
        "ctypes.c_byte": "int",
        "ctypes.c_ubyte": "int",
        "ctypes.c_short": "int",
        "ctypes.c_ushort": "int",
        "ctypes.c_int": "int",
        "ctypes.c_uint": "int",
        "ctypes.c_long": "int",
        "ctypes.c_ulong": "int",
        "ctypes.c_longlong": "int",
        "ctypes.c_ulonglong": "int",
        "ctypes.c_size_t": "int",
        "ctypes.c_ssize_t": "int",
        "ctypes.c_void_p": "int | None",
        "ctypes.c_char_p": "bytes | None",
        "ctypes.c_wchar_p": "str | None",
        "wintypes.BYTE": "int",
        "wintypes.WORD": "int",
        "wintypes.DWORD": "int",
        "wintypes.UINT": "int",
        "wintypes.INT": "int",
        "wintypes.LONG": "int",
        "wintypes.ULONG": "int",
        "wintypes.ATOM": "int",
        "wintypes.HANDLE": "int",
        "wintypes.HWND": "int",
        "wintypes.HINSTANCE": "int",
        "wintypes.HMODULE": "int",
        "wintypes.HMENU": "int",
        "wintypes.HICON": "int",
        "wintypes.HCURSOR": "int",
        "wintypes.HBRUSH": "int",
        "wintypes.HDC": "int",
        "wintypes.WPARAM": "int",
        "wintypes.LPARAM": "int",
        "LRESULT": "int",
        "wintypes.LPCWSTR": "str | None",
        "wintypes.LPWSTR": "str | None",
        "wintypes.LPVOID": "int | None",
        "ctypes.RECT": "ctypes.RECT",
        "ctypes.MSG": "ctypes.MSG",
    }

    if type_expr in mapping:
        return mapping[type_expr]

    if type_expr.startswith("ctypes.pointer(") and type_expr.endswith(")"):
        inner = type_expr[len("ctypes.pointer(") : -1]
        if inner in defined_struct_names:
            return inner
        return "int"

    if type_expr in defined_struct_names:
        return type_expr

    if "*" in type_expr:
        return "Any"

    return "Any"


def emit_struct(struct_spec: dict[str, Any], type_lookup: dict[str, str]) -> str:
    c_name = struct_spec["c_name"]
    py_name = struct_spec.get("py_name", c_name)
    fields: dict[str, str] = struct_spec["fields"]

    _GENERATED_STRUCTS.append(py_name)

    lines: list[str] = []
    lines.append(f"class {py_name}(ctypes.Structure):")
    lines.append(f'    """ctypes.Structure for {c_name}."""')
    lines.append("    _fields_ = [")
    for field_name, field_type_name in fields.items():
        resolved_type = type_lookup.get(field_type_name, field_type_name)
        lines.append(f'        ("{field_name}", {resolved_type}),')
    lines.append("    ]")
    lines.append("")
    return "\n".join(lines)


def emit_function(
    func_spec: dict[str, Any],
    type_lookup: dict[str, str],
    defined_struct_names: set[str],
) -> str:
    dll = func_spec["dll"]
    c_name = func_spec["c_name"]
    py_name = func_spec.get("py_name", to_snake_case(c_name))
    _GENERATED_FUNCTIONS.append(py_name)

    params: dict[str, str] = func_spec.get("params", {})
    return_type_name = func_spec["return_type"]

    resolved_argtypes = [type_lookup.get(tp, tp) for tp in params.values()]
    resolved_restype = type_lookup.get(return_type_name, return_type_name)

    signature_parts: list[str] = []
    call_parts: list[str] = []

    for param_name, type_name in params.items():
        resolved = type_lookup.get(type_name, type_name)
        py_annot = python_type_expr(resolved, defined_struct_names)
        signature_parts.append(f"{param_name}: {py_annot}")
        if resolved.startswith("ctypes.pointer("):
            call_parts.append(f"ctypes.byref({param_name})")
        else:
            call_parts.append(param_name)
    signature = ", ".join(signature_parts)
    call_args = ", ".join(call_parts)
    py_return = python_type_expr(resolved_restype, defined_struct_names)

    lines: list[str] = []
    lines.append(f"{c_name} = _get_dll({dll!r}).{c_name}")
    lines.append(
        f"{c_name}.argtypes = ({', '.join(resolved_argtypes)}{',' if len(resolved_argtypes) == 1 else ''})"
    )
    lines.append(f"{c_name}.restype = {resolved_restype}")
    lines.append("")
    lines.append(f"def {py_name}({signature}) -> {py_return}:")
    lines.append(f"    return {c_name}({call_args})")
    lines.append("")
    return "\n".join(lines)


def generate_python_from_yaml(yaml_path: str | Path, output_path: str | Path) -> None:
    """
    Read a YAML Win32 spec and write a Python module containing ctypes structs
    and wrapped Win32 functions.
    """
    yaml_path = Path(yaml_path)
    output_path = Path(output_path)

    with yaml_path.open("r", encoding="utf-8") as f:
        spec = yaml.safe_load(f)

    type_lookup: dict[str, str] = dict(spec.get("types", {}))
    structs: list[dict[str, Any]] = list(spec.get("structs", []))
    functions: list[dict[str, Any]] = list(spec.get("functions", []))

    defined_struct_names = {
        struct_spec.get("py_name", struct_spec["c_name"]) for struct_spec in structs
    }

    # Make struct names resolvable from YAML type strings too.
    for struct_spec in structs:
        c_name = struct_spec["c_name"]
        py_name = struct_spec.get("py_name", c_name)
        type_lookup[c_name] = py_name
        type_lookup[py_name] = py_name

    lines: list[str] = [
        "from __future__ import annotations",
        "",
        "import ctypes",
        "from ctypes import wintypes",
        "from typing import Any",
        "",
        "_DLL_CACHE: dict[str, ctypes.WinDLL] = {}",
        "LRESULT = c_uint64",
        "",
        "def _get_dll(name: str) -> ctypes.WinDLL:",
        "    key = name.lower()",
        "    dll = _DLL_CACHE.get(key)",
        "    if dll is None:",
        "        dll = ctypes.WinDLL(name, use_last_error=True)",
        "        _DLL_CACHE[key] = dll",
        "    return dll",
        "",
    ]

    if structs:
        for struct_spec in structs:
            lines.append(emit_struct(struct_spec, type_lookup))

    if functions:
        for func_spec in functions:
            lines.append(emit_function(func_spec, type_lookup, defined_struct_names))

    lines.append("__all__ = [\n")
    for symbol in _GENERATED_FUNCTIONS + _GENERATED_STRUCTS:
        lines.append(f'\t"{symbol}",')
    lines.append("]\n")

    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    generate_python_from_yaml(
        Path(__file__).with_suffix(".yaml"),
        Path(__file__).with_name("winapi_gen.py"),
    )
