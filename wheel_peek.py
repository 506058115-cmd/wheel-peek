#!/usr/bin/env python3
"""Read selected metadata from a Python wheel without installing it."""

import argparse
from email.parser import BytesParser
from pathlib import Path
import sys
import zipfile


MAX_METADATA_BYTES = 1024 * 1024
MAX_REQUIREMENTS = 40


def terminal_safe(value):
    return "".join(
        char if char.isprintable() else char.encode("unicode_escape").decode("ascii")
        for char in value
    )


def read_member(archive, info):
    if info.file_size > MAX_METADATA_BYTES:
        raise ValueError(f"元数据文件超过 {MAX_METADATA_BYTES} 字节")
    with archive.open(info) as stream:
        data = stream.read(MAX_METADATA_BYTES + 1)
    if len(data) > MAX_METADATA_BYTES:
        raise ValueError("元数据解压后超出大小限制")
    return data


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="静态查看 Python wheel 的分发元数据；不会安装或执行其中的代码。"
    )
    parser.add_argument("wheel", help=".whl 文件路径")
    args = parser.parse_args(argv)

    try:
        with zipfile.ZipFile(args.wheel) as archive:
            metadata_files = [
                item for item in archive.infolist()
                if item.filename.endswith(".dist-info/METADATA")
            ]
            if len(metadata_files) != 1:
                raise ValueError("wheel 必须且只能包含一个 .dist-info/METADATA")
            metadata = BytesParser().parsebytes(read_member(archive, metadata_files[0]))
            wheel_name = metadata_files[0].filename.rsplit("/", 1)[0] + "/WHEEL"
            wheel_files = [item for item in archive.infolist() if item.filename == wheel_name]
            wheel_meta = (
                BytesParser().parsebytes(read_member(archive, wheel_files[0]))
                if len(wheel_files) == 1 else None
            )

            infos = archive.infolist()
            print(f"文件: {terminal_safe(str(Path(args.wheel)))}")
            print(f"名称: {terminal_safe(metadata.get('Name', '(缺失)'))}")
            print(f"版本: {terminal_safe(metadata.get('Version', '(缺失)'))}")
            print(f"Requires-Python: {terminal_safe(metadata.get('Requires-Python', '(未声明)'))}")
            print(f"License: {terminal_safe(metadata.get('License-Expression') or metadata.get('License') or '(未声明)')}")
            print(f"归档条目: {len(infos)}；声明的解压总大小: {sum(item.file_size for item in infos)} 字节")

            if wheel_meta is None:
                print("Wheel 标签: WHEEL 元数据缺失或重复")
            else:
                tags = wheel_meta.get_all("Tag", [])
                print("Wheel 标签: " + (", ".join(terminal_safe(tag) for tag in tags) or "(未声明)"))

            requirements = metadata.get_all("Requires-Dist", [])
            print(f"声明依赖: {len(requirements)}")
            for requirement in requirements[:MAX_REQUIREMENTS]:
                print(f"  {terminal_safe(requirement)}")
            if len(requirements) > MAX_REQUIREMENTS:
                print(f"  ……另有 {len(requirements) - MAX_REQUIREMENTS} 项未显示")
        return 0
    except (OSError, ValueError, zipfile.BadZipFile, RuntimeError) as error:
        print(f"wheel-peek: {terminal_safe(str(error))}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("wheel-peek: 已中断。", file=sys.stderr)
        raise SystemExit(130)
