from pathlib import Path
import zipfile
import struct

archive = Path("Rimva_Premium_Illustrated_Showcase_4_PNGs.zip")
expected = {
    "01-workspace-backup-illustration.png": (1672, 941),
    "02-ghl-export-summary-illustration.png": (1448, 1086),
    "03-website-capture-illustration.png": (1672, 941),
    "04-website-snapshot-result-illustration.png": (1448, 1086),
}
if not archive.exists():
    print("No pending ZIP to import")
    raise SystemExit(0)

dest = Path("assets/showcase")
dest.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(archive) as z:
    if set(z.namelist()) != set(expected):
        raise SystemExit("Unexpected ZIP members")
    for name, dimensions in expected.items():
        info = z.getinfo(name)
        if info.file_size > 9_000_000:
            raise SystemExit("Image too large: " + name)
        data = z.read(name)
        if data[:8] != b"\x89PNG\r\n\x1a\n":
            raise SystemExit("Not PNG: " + name)
        if struct.unpack(">II", data[16:24]) != dimensions:
            raise SystemExit("Unexpected dimensions: " + name)
        (dest / name).write_bytes(data)

readme = Path("README.md")
body = readme.read_text(encoding="utf-8")
anchor = "## Real extension screenshots · v11.2.5"
if anchor not in body:
    raise SystemExit("README anchor missing")
if "## Illustrated workflow showcase" not in body:
    section = """## Illustrated workflow showcase

These four **Rimva-branded promotional illustrations** visualize backup and website capture. They are not unmodified Chrome screenshots or proof of a current live GHL export. Genuine v11.2.5 extension screenshots appear below.

| GHL backup selection | Export completion |
| :---: | :---: |
| <img src="assets/showcase/01-workspace-backup-illustration.png" alt="Illustration of Rimva GHL backup selections" width="100%"> | <img src="assets/showcase/02-ghl-export-summary-illustration.png" alt="Illustration of Rimva GHL export summary" width="100%"> |

| Published website capture | Snapshot ZIP ready |
| :---: | :---: |
| <img src="assets/showcase/03-website-capture-illustration.png" alt="Illustration of Rimva website capture" width="100%"> | <img src="assets/showcase/04-website-snapshot-result-illustration.png" alt="Illustration of Rimva website capture completion" width="100%"> |

**Historical context:** Original GHL export tests occurred before the Rimva rebrand. Rebranded illustrations are visual explanations, not original live-session captures.

---

"""
    readme.write_text(body.replace(anchor, section + anchor, 1), encoding="utf-8")
archive.unlink()
print("Installed 4 full-resolution images; README updated")
