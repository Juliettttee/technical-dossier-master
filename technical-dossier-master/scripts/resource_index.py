#!/usr/bin/env python3
"""Incremental, metadata-first discovery for Technical Dossier Resource Packs."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SUPPORTED = {
    ".pdf": "pdf", ".docx": "docx", ".txt": "text", ".md": "markdown",
    ".markdown": "markdown", ".csv": "csv", ".xlsx": "xlsx",
    ".png": "image", ".jpg": "image", ".jpeg": "image", ".tif": "image",
    ".tiff": "image", ".webp": "image", ".bmp": "image", ".gif": "image",
    ".svg": "image",
}
CONTROL_FILES = {"pack.json", "pack.local.json", "pack.local.example.json"}
INDEX_NAME = ".resource-index.json"
WORD_RE = re.compile(r"[\w\-]+", re.UNICODE)
BILINGUAL_GROUPS = (
    {"structure", "structural", "结构"},
    {"material", "materials", "材料"},
    {"water", "水"},
    {"fountain", "喷泉"},
    {"architecture", "architectural", "建筑"},
    {"electronic", "electronics", "电子"},
    {"semiconductor", "semiconductors", "半导体"},
    {"safety", "安全"},
    {"installation", "安装"},
    {"maintenance", "维护", "检修"},
)


def utc_iso(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp, timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def terms(value: str) -> list[str]:
    found: set[str] = set()
    normalized = value.casefold().replace("_", " ").replace("/", " ").replace("\\", " ")
    for token in WORD_RE.findall(normalized):
        token = token.strip("-")
        if len(token) >= 2:
            found.add(token)
        if any("\u4e00" <= char <= "\u9fff" for char in token):
            cjk = "".join(char for char in token if "\u4e00" <= char <= "\u9fff")
            found.update(cjk[index:index + 2] for index in range(max(0, len(cjk) - 1)))
    expanded = set(found)
    for group in BILINGUAL_GROUPS:
        if found.intersection(group):
            expanded.update(group)
    return sorted(expanded)


def load_json(path: Path) -> tuple[dict[str, Any], str | None]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        if not isinstance(data, dict):
            return {}, "JSON root is not an object"
        return data, None
    except Exception as exc:
        return {}, f"{type(exc).__name__}: {exc}"


def load_old(index_path: Path) -> dict[str, Any]:
    if not index_path.exists():
        return {}
    data, error = load_json(index_path)
    if error or data.get("schema_version") != 1:
        return {}
    return data


def pack_metadata(pack_dir: Path) -> dict[str, Any]:
    manifest_path = pack_dir / "pack.json"
    manifest: dict[str, Any] = {}
    manifest_error = None
    if manifest_path.exists():
        manifest, manifest_error = load_json(manifest_path)
    identity = manifest.get("id") if isinstance(manifest.get("id"), str) else pack_dir.name
    text_parts = [pack_dir.name]
    for key in ("title", "description"):
        if isinstance(manifest.get(key), str):
            text_parts.append(manifest[key])
    domains = manifest.get("domains", [])
    if isinstance(domains, list):
        text_parts.extend(str(item) for item in domains)
    return {
        "folder": pack_dir.name,
        "id": identity,
        "manifest": "present" if manifest_path.exists() else "absent",
        "manifest_error": manifest_error,
        "topics": terms(" ".join(text_parts)),
    }


def candidate_score(record: dict[str, Any], query_terms: set[str]) -> int:
    if not query_terms:
        return 0
    haystack = set(record.get("topics", []))
    path_text = record.get("relative_path", "").casefold()
    score = 0
    for query in query_terms:
        if query in haystack:
            score += 4
        elif query in path_text:
            score += 2
        elif any(query in topic or topic in query for topic in haystack if len(topic) >= 3):
            score += 1
    return score


def scan(root: Path, index_path: Path, query: str, hash_max_mb: int, rebuild: bool) -> tuple[dict[str, Any], dict[str, Any]]:
    old = {} if rebuild else load_old(index_path)
    old_files = {item["relative_path"]: item for item in old.get("files", []) if "relative_path" in item}
    packs: list[dict[str, Any]] = []
    files: list[dict[str, Any]] = []
    summary: dict[str, list[Any]] = {
        "new": [], "modified": [], "deleted": [], "unchanged": [],
        "unsupported": [], "errors": [],
    }
    max_bytes = hash_max_mb * 1024 * 1024
    root.mkdir(parents=True, exist_ok=True)
    pack_dirs = sorted(
        (path for path in root.iterdir() if path.is_dir() and not path.name.startswith(".")),
        key=lambda path: path.name.casefold(),
    )
    for pack_dir in pack_dirs:
        meta = pack_metadata(pack_dir)
        packs.append(meta)
        if meta["manifest_error"]:
            summary["errors"].append({"path": f"{pack_dir.name}/pack.json", "error": meta["manifest_error"]})
        for path in sorted(pack_dir.rglob("*"), key=lambda item: str(item).casefold()):
            if not path.is_file() or path.name.startswith(".") or path.name in CONTROL_FILES:
                continue
            relative = path.relative_to(root).as_posix()
            try:
                stat = path.stat()
                suffix = path.suffix.casefold()
                kind = SUPPORTED.get(suffix, "unsupported")
                previous = old_files.get(relative)
                unchanged = bool(
                    previous
                    and previous.get("size") == stat.st_size
                    and previous.get("mtime_ns") == stat.st_mtime_ns
                )
                record: dict[str, Any] = {
                    "relative_path": relative,
                    "pack": pack_dir.name,
                    "file_type": kind,
                    "extension": suffix,
                    "size": stat.st_size,
                    "mtime_ns": stat.st_mtime_ns,
                    "modified_utc": utc_iso(stat.st_mtime),
                    "supported": kind != "unsupported",
                    "topics": sorted(set(meta["topics"] + terms(relative))),
                    "parse_status": "metadata_only" if kind != "unsupported" else "unsupported",
                    "error": None,
                }
                if unchanged:
                    record["sha256"] = previous.get("sha256")
                    record["hash_status"] = previous.get("hash_status", "unavailable")
                    summary["unchanged"].append(relative)
                else:
                    summary["modified" if previous else "new"].append(relative)
                    if kind == "unsupported":
                        record["sha256"] = None
                        record["hash_status"] = "not_applicable"
                    elif stat.st_size <= max_bytes:
                        record["sha256"] = sha256(path)
                        record["hash_status"] = "computed"
                    else:
                        record["sha256"] = None
                        record["hash_status"] = "skipped_size_limit"
                if kind == "unsupported":
                    summary["unsupported"].append(relative)
                files.append(record)
            except Exception as exc:
                error = f"{type(exc).__name__}: {exc}"
                summary["errors"].append({"path": relative, "error": error})
                files.append({
                    "relative_path": relative, "pack": pack_dir.name,
                    "parse_status": "error", "error": error,
                })

    current = {item["relative_path"] for item in files}
    summary["deleted"] = sorted(set(old_files) - current)
    query_terms = set(terms(query))
    candidates = []
    for record in files:
        if not record.get("supported"):
            continue
        score = candidate_score(record, query_terms)
        if score > 0:
            candidates.append({
                "relative_path": record["relative_path"], "pack": record["pack"],
                "score": score, "status": record["parse_status"],
            })
    candidates.sort(key=lambda item: (-item["score"], item["relative_path"].casefold()))
    index = {
        "schema_version": 1,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "root": str(root.resolve()),
        "hash_max_mb": hash_max_mb,
        "packs": packs,
        "files": files,
    }
    report = {
        "index_path": str(index_path.resolve()),
        "pack_count": len(packs),
        "file_count": len(files),
        "query": query,
        "candidates": candidates,
        "summary": summary,
        "note": "Index and candidate scores are discovery metadata, not technical evidence; selected files still require direct inspection.",
    }
    return index, report


def atomic_write(path: Path, data: dict[str, Any]) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("scan", "rebuild"))
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1] / "resource-packs")
    parser.add_argument("--index", type=Path)
    parser.add_argument("--query", default="")
    parser.add_argument("--hash-max-mb", type=int, default=64)
    args = parser.parse_args()
    if args.hash_max_mb < 0:
        parser.error("--hash-max-mb must be zero or greater")
    root = args.root.resolve()
    index_path = args.index.resolve() if args.index else root / INDEX_NAME
    try:
        index, report = scan(root, index_path, args.query, args.hash_max_mb, args.command == "rebuild")
        atomic_write(index_path, index)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({"status": "error", "error": f"{type(exc).__name__}: {exc}"}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
