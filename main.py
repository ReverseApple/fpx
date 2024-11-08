from pathlib import Path
import plistlib
import shutil

PF_DIR = Path("/System/Library/PrivateFrameworks/")
OUTPUT = Path("./binaries")

backup = {
    "FairPlay": {
        "base": PF_DIR / "CoreFP.framework" / "Versions" / "A",
        "files": [
            ("CoreFP",),
            ("fairplayd",),
            ("Resources", "CoreFP.icxs"),
            ("XPCServices", "com.apple.fpsd.arcadeservice.xpc", "Contents", "MacOS", "com.apple.fpsd.arcadeservice")
        ]
    },
    "CoreADI": {
        "base": PF_DIR / "CoreADI.framework" / "Versions" / "A",
        "files": [
            ("CoreADI",),
            ("adid",)
        ]
    },
    "CoreLSKD": {
        "base": PF_DIR / "CoreLSKD.framework" / "Versions" / "A",
        "files": [
            ("CoreLSKD",),
            ("lskdd",)
        ]
    },
    "CoreKE": {
        "base": PF_DIR / "CoreKE.framework" / "Versions" / "A",
        "files": [
            ("CoreKE",),
        ]
    },
}

def create_directories():
    OUTPUT.mkdir(exist_ok=True)
    for directory in backup.keys():
        (OUTPUT / directory).mkdir(exist_ok=True)


def get_version(path: Path):
    plist = path / "Resources" / "Info.plist"

    if not plist.exists():
        plist = path / "Info.plist"
        assert plist.exists()

    content = plist.read_bytes()
    content = content.replace(b"\"-\//", b"\"-//")

    return plistlib.loads(content)["CFBundleShortVersionString"]


def main():
    create_directories()

    for name, item in backup.items():
        location_base = item['base']
        bundle_version = get_version(location_base)
        print(f"{name} {bundle_version}")

        copy_path = OUTPUT / name / bundle_version
        copy_path.mkdir(exist_ok=True, parents=True)

        for path in item['files']:
            print(f"  -> Copying {path[-1]}")
            binary_path = location_base.joinpath("/".join(path))
            shutil.copyfile(binary_path, copy_path / path[-1])

    pass



if __name__ == '__main__':
    main()
