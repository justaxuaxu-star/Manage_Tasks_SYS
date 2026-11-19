import json
import os
import struct
from pathlib import Path

DIR = Path(__file__).resolve().parents[1] / "public" / "models"

for path in sorted(DIR.glob("*.glb")):
    with path.open("rb") as f:
        f.read(12)
        clen = struct.unpack("<I", f.read(4))[0]
        f.read(4)
        data = json.loads(f.read(clen))
    nodes = data.get("nodes", [])
    meshes = data.get("meshes", [])
    tris = 0
    for mesh in meshes:
        for prim in mesh.get("primitives", []):
            idx = prim.get("indices")
            if idx is not None:
                tris += data["accessors"][idx]["count"] // 3
    names = [n.get("name", "") for n in nodes[:6]]
    print(
        f"{path.name:22} {path.stat().st_size // 1024:4}KB "
        f"meshes={len(meshes):3} nodes={len(nodes):3} tris≈{tris:6} {names}"
    )