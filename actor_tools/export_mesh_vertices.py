# Save as export_staticmesh_vertices_procedural.py
import unreal
import csv
import os
import math

# === 配置 ===
STATIC_MESH_PATH = '/Game/ResidentialBuildingsSet/Residential_Buildings_001.Residential_Buildings_001' # <- 替换为你的资源路径
LOD_INDEX = 0
OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "UnrealMeshExport")
OUTPUT_FILENAME = "StaticMesh_Vertices.csv"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)

# === 工具 ===
def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def log(msg):
    unreal.log("[ExportStaticMesh] " + str(msg))

# === 主函数（使用 ProceduralMeshLibrary）===
def export_vertices_using_proceduralmesh(static_mesh_path, lod_index=0, out_csv_path=None):
    mesh = unreal.EditorAssetLibrary.load_asset(static_mesh_path)
    if not mesh:
        unreal.log_error(f"无法加载 StaticMesh: {static_mesh_path}")
        return False

    # 尝试获取 section 数量（API 可能因版本不同而不同）
    try:
        section_count = mesh.get_num_sections(lod_index)
    except Exception:
        # 如果没有该方法，保守地设为 1（大多数简单网格只有一个 section）
        section_count = 1

    all_vertices = []  # 将存放 (global_index, x, y, z, section_index, vertex_local_index)
    global_index = 0

    for section_idx in range(section_count):
        try:
            # ProceduralMeshLibrary 提供的便捷函数，会返回该 section 的顶点/索引/法线/uv等
            section = unreal.ProceduralMeshLibrary.get_section_from_static_mesh(mesh, lod_index, section_idx)
            # 返回的 section 典型结构： (vertices, triangles, normals, uvs, tangents, colors) —— 不同版本可能有细微差别
            vertices = section[0] if len(section) > 0 else []
        except Exception as e:
            unreal.log_warning(f"无法通过 ProceduralMeshLibrary 获取 section {section_idx}：{e}")
            vertices = []

        # 遍历并记录
        for local_i, v in enumerate(vertices):
            # v 通常是 unreal.Vector 类型，直接读取 x,y,z
            all_vertices.append((global_index, float(v.x), float(v.y), float(v.z), section_idx, local_i))
            global_index += 1

    if not all_vertices:
        unreal.log_warning("未提取到任何顶点（检查 LOD / section 设置）")
        return False

    # 写 CSV
    if out_csv_path is None:
        ensure_dir(OUTPUT_DIR)
        out_csv_path = OUTPUT_PATH
    else:
        ensure_dir(os.path.dirname(out_csv_path))

    with open(out_csv_path, mode="w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["GlobalIndex", "X", "Y", "Z", "SectionIndex", "LocalIndex"])
        for row in all_vertices:
            writer.writerow(row)

    log(f"导出完成：{out_csv_path}   顶点数量：{len(all_vertices)}")
    return True

# === 执行 ===
if __name__ == "__main__":
    export_vertices_using_proceduralmesh(STATIC_MESH_PATH, LOD_INDEX, OUTPUT_PATH)
