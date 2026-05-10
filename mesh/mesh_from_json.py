import unreal
import json
import os
import math

# ---------- 配置 ----------
# 确保这个路径是正确的
json_path = r"E:\Code\PythonDir\UnrealPythonToolkit\data\example.json" 

actor_name = "ProcMesh_From_JSON"
spawn_location = unreal.Vector(0.0, 0.0, 0.0)

# 网格体的材质路径
material_path = "/Engine/BasicShapes/BasicShapeMaterial.BasicShapeMaterial"
# ---------- /配置 ----------


def create_procedural_mesh_actor(name, location, vertices_data, polygons_data, material_path):
    """
    根据给定的顶点和多边形数据，在 Unreal Engine 中创建带有 Procedural Mesh Component 的 Actor。
    使用 SubobjectDataSubsystem 的方式确保组件正确创建。
    """
    
    # 1. 创建 Actor
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.Actor, location)
    if not actor:
        unreal.log_error(f"无法创建 Actor: {name}")
        return None
    
    actor.set_actor_label(name)
    actor.set_folder_path("ProceduralMeshes")
    
    # 2. 使用 SubobjectDataSubsystem 添加 ProceduralMeshComponent
    subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    root_sub_object_handles = subsystem.k2_gather_subobject_data_for_instance(actor)
    
    if not root_sub_object_handles:
        unreal.log_error(f"无法获取 Actor {actor.get_name()} 的根组件句柄。")
        return None
    
    root_handle = root_sub_object_handles[0]
    
    # 3. 配置添加新子对象的参数
    params = unreal.AddNewSubobjectParams(
        parent_handle=root_handle,
        new_class=unreal.ProceduralMeshComponent
    )
    
    # 4. 添加新组件
    new_sub_object_handle, fail_reason = subsystem.add_new_subobject(params)
    
    if not new_sub_object_handle:
        unreal.log_error(f"为 Actor {actor.get_name()} 添加 ProceduralMeshComponent 失败: {fail_reason}")
        return None
    
    # 5. 获取新添加的组件实例
    pmc_components = actor.get_components_by_class(unreal.ProceduralMeshComponent)
    if not pmc_components:
        unreal.log_error(f"无法获取 Actor {actor.get_name()} 的 ProceduralMeshComponent 组件。")
        return None
    
    proc_mesh_comp = pmc_components[-1]  # 获取最后一个（新添加的）
    
    # 6. 配置组件移动性
    proc_mesh_comp.set_mobility(unreal.ComponentMobility.STATIC)
    
    # 7. 数据转换与准备
    unreal_vertices = [unreal.Vector(v[0], v[1], v[2]) for v in vertices_data]
    
    # 8. 创建三角形索引 (三角剖分)
    triangle_indices = []
    for polygon_indices in polygons_data:
        if len(polygon_indices) < 3:
            continue
        
        v0_index = polygon_indices[0]
        for i in range(1, len(polygon_indices) - 1):
            v1_index = polygon_indices[i]
            v2_index = polygon_indices[i + 1]
            triangle_indices.extend([v0_index, v1_index, v2_index])
            # 添加反面以确保能看到网格
            triangle_indices.extend([v0_index, v2_index, v1_index])
    
    # 9. 生成法线和 UVs
    unreal_normals = [unreal.Vector(0.0, 1.0, 0.0)] * len(unreal_vertices)
    unreal_uvs = [unreal.Vector2D(v.x / 100.0, v.z / 100.0) for v in unreal_vertices]
    
    # 10. 创建网格体分段
    proc_mesh_comp.clear_all_mesh_sections()
    proc_mesh_comp.create_mesh_section(
        0, 
        unreal_vertices, 
        triangle_indices, 
        unreal_normals, 
        unreal_uvs, 
        [], # Vertex Colors
        [], # Tangents
        True # bCreateCollision
    )
    
    # 11. 应用材质
    if material_path:
        material = unreal.load_asset(material_path)
        if material:
            proc_mesh_comp.set_material(0, material)
        else:
            unreal.log_warning(f"无法加载材质: {material_path}")
    
    unreal.log(f"✅ 成功创建程序化网格体 Actor: {name}，顶点数: {len(unreal_vertices)}，三角形数: {len(triangle_indices) // 3}")
    return actor


# ---------- 主执行逻辑 ----------

try:
    # 检查 json 文件是否存在
    if not os.path.exists(json_path):
        unreal.log_error(f"❌ JSON 文件不存在: {json_path}")
    else:
        # 读取 JSON 文件
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        raw_vertices = data.get("vertices", [])
        raw_polygons = data.get("polygons", [])

        if not raw_vertices or not raw_polygons:
            unreal.log_error("❌ JSON 数据中 'vertices' 或 'polygons' 字段为空。")
        else:
            # 调用函数创建网格体
            create_procedural_mesh_actor(
                actor_name,
                spawn_location,
                raw_vertices,
                raw_polygons,
                material_path
            )

except Exception as e:
    unreal.log_error(f"❌ 脚本执行过程中发生错误: {e}")