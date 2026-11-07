"""Build Markdown into a staged site before replacing generated output."""

import argparse
import os
from pathlib import Path
import shutil
import tempfile
from urllib.parse import urlsplit

from markdown_to_html import generate_page, normalize_basepath
from seo import write_crawl_files

ROOT = Path(__file__).resolve().parent.parent


def validate_site_url(value):
    """Return a canonical origin/base path without query or fragment state."""
    parsed = urlsplit(value)
    if (
        parsed.scheme not in {"https", "http"}
        or not parsed.netloc
        or parsed.hostname is None
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
        or any(ord(char) < 32 or ord(char) == 127 for char in value)
    ):
        raise ValueError(
            "Site URL must be an absolute HTTP(S) URL without credentials, query, or fragment"
        )
    return value.rstrip("/")


def copy_directory(source, destination):
    shutil.copytree(source, destination, dirs_exist_ok=True)


def generate_pages_recursive(
    dir_path,
    template_path,
    dest_dir_path,
    basepath="/",
    *,
    site_url="https://yaqyn.dev",
    _root=None,
):
    source_root = Path(_root or dir_path)
    for source in sorted(Path(dir_path).iterdir()):
        destination = Path(dest_dir_path) / source.name
        if source.is_dir():
            generate_pages_recursive(
                source,
                template_path,
                destination,
                basepath,
                site_url=site_url,
                _root=source_root,
            )
        elif source.suffix == ".md":
            relative = source.relative_to(source_root).with_suffix(".html")
            route = "/" + relative.as_posix()
            if source.stem == "index":
                route = route[: -len("index.html")]
            generate_page(
                source,
                template_path,
                destination.with_suffix(".html"),
                basepath,
                route=route,
                site_url=site_url,
            )


def build_site(basepath="/", output=None, site_url="https://yaqyn.dev"):
    basepath = normalize_basepath(basepath)
    site_url = validate_site_url(site_url)
    output = Path(output or ROOT / "docs").resolve()
    for protected in [
        ROOT,
        ROOT / "content",
        ROOT / "static",
        ROOT / "src",
        ROOT / ".git",
        ROOT / "readme-assets",
    ]:
        if (
            output == protected
            or protected.is_relative_to(output)
            or output.is_relative_to(protected)
            and protected != ROOT
        ):
            raise ValueError(
                "Output must not replace the project or its source directories"
            )
    if output.exists() and not output.is_dir():
        raise ValueError("Output must be a directory")
    if (
        output.exists()
        and output != ROOT / "docs"
        and not (output / ".nojekyll").exists()
    ):
        raise ValueError(
            "Existing custom output must contain the generated-site .nojekyll marker"
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=".site-build-", dir=output.parent
    ) as temporary:
        stage = Path(temporary) / "site"
        copy_directory(ROOT / "static", stage)
        generate_pages_recursive(
            ROOT / "content", ROOT / "template.html", stage, basepath, site_url=site_url
        )
        write_crawl_files(stage, site_url)
        (stage / ".nojekyll").touch()
        backup = Path(temporary) / "previous"
        if output.exists():
            os.replace(output, backup)
        try:
            os.replace(stage, output)
        except OSError:
            if backup.exists():
                os.replace(backup, output)
            raise
    return output


def main(argv=None):
    parser = argparse.ArgumentParser(description="Build yaqyn's Markdown site")
    parser.add_argument("basepath", nargs="?", default="/")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--site-url", default="https://yaqyn.dev")
    args = parser.parse_args(argv)
    try:
        site_url = validate_site_url(args.site_url)
    except ValueError as error:
        parser.error(str(error))
    try:
        output = build_site(args.basepath, args.output, site_url)
        print(f"Built site: {output}")
        return 0
    except (OSError, ValueError) as error:
        parser.exit(1, f"Build failed: {error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
