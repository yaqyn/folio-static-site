"""Build Markdown into a staged site before replacing generated output."""

import argparse
import os
from pathlib import Path
import shutil
import tempfile
from urllib.parse import urlsplit

from markdown_to_html import generate_page, normalize_basepath

ROOT = Path(__file__).resolve().parent.parent


def copy_directory(source, destination):
    shutil.copytree(source, destination, dirs_exist_ok=True)


def generate_pages_recursive(
    dir_path,
    template_path,
    dest_dir_path,
    basepath="/",
    *,
    site_url="https://yaqyn.github.io/folio",
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
            if route.endswith("index.html"):
                route = route[: -len("index.html")]
            generate_page(
                source,
                template_path,
                destination.with_suffix(".html"),
                basepath,
                route=route,
                site_url=site_url,
            )


def build_site(basepath="/", output=None, site_url="https://yaqyn.github.io/folio"):
    basepath = normalize_basepath(basepath)
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
    parser.add_argument("--site-url", default="https://yaqyn.github.io/folio")
    args = parser.parse_args(argv)
    if (
        urlsplit(args.site_url).scheme not in {"https", "http"}
        or not urlsplit(args.site_url).netloc
    ):
        parser.error("Site URL must be an absolute HTTP(S) URL")
    try:
        output = build_site(args.basepath, args.output, args.site_url)
        print(f"Built site: {output}")
        return 0
    except (OSError, ValueError) as error:
        parser.exit(1, f"Build failed: {error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
