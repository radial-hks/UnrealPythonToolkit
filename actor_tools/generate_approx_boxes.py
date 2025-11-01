import unreal
import random


def log(msg):
    unreal.log(f"[ApproxBoxes] {msg}")


def kmeans(points, k, max_iters=25):
    """
    纯 Python K-Means，对点列表进行聚类。
    points: List[unreal.Vector]
    返回: List[List[unreal.Vector]] 聚类结果（去除空簇）
    """
    if not points or k <= 0:
        return []
    k = min(k, len(points))
    # 初始化质心（随机采样）
    centroids = random.sample(points, k)

    assignments = [0] * len(points)
    for _ in range(max_iters):
        # 归类到最近质心
        for i, p in enumerate(points):
            min_d = float("inf")
            min_j = 0
            for j, c in enumerate(centroids):
                dx = p.x - c.x
                dy = p.y - c.y
                dz = p.z - c.z
                d = dx * dx + dy * dy + dz * dz
                if d < min_d:
                    min_d = d
                    min_j = j
            assignments[i] = min_j

        # 更新质心
        sums = [unreal.Vector(0.0, 0.0, 0.0) for _ in range(k)]
        counts = [0] * k
        for i, p in enumerate(points):
            j = assignments[i]
            v = sums[j]
            sums[j] = unreal.Vector(v.x + p.x, v.y + p.y, v.z + p.z)
            counts[j] += 1

        new_centroids = []
        for j in range(k):
            if counts[j] > 0:
                v = sums[j]
                new_centroids.append(
                    unreal.Vector(v.x / counts[j], v.y / counts[j], v.z / counts[j])
                )
            else:
                # 保持原质心以避免空簇抖动
                new_centroids.append(centroids[j])

        # 简单收敛检测（质心变化很小）
        converged = True
        for j in range(k):
            dx = centroids[j].x - new_centroids[j].x
            dy = centroids[j].y - new_centroids[j].y
            dz = centroids[j].z - new_centroids[j].z
            if (dx * dx + dy * dy + dz * dz) > 1e-6:
                converged = False
                break
        centroids = new_centroids
        if converged:
            break

    # 组装簇
    clusters = [[] for _ in range(k)]
    for i, p in enumerate(points):
        clusters[assignments[i]].append(p)
    # 去除空簇
    clusters = [c for c in clusters if len(c) > 0]
    return clusters


def compute_aabb(points):
    """基于点列表计算AABB中心与半径（extent）。"""
    if not points:
        return unreal.Vector(0, 0, 0), unreal.Vector(0, 0, 0)
    min_x = min(p.x for p in points)
    min_y = min(p.y for p in points)
    min_z = min(p.z for p in points)
    max_x = max(p.x for p in points)
    max_y = max(p.y for p in points)
    max_z = max(p.z for p in points)
    center = unreal.Vector((min_x + max_x) * 0.5, (min_y + max_y) * 0.5, (min_z + max_z) * 0.5)
    extent = unreal.Vector((max_x - min_x) * 0.5, (max_y - min_y) * 0.5, (max_z - min_z) * 0.5)
    return center, extent

def get_points_from_static_mesh(static_mesh, lod_index=0, to_world_transform=None):
    """从StaticMesh指定LOD提取所有顶点，兼容UE5.1版本。
    优先使用MeshDescription，其次尝试Geometry Script，最后回退KPL。
    """
    points = []
    log = lambda msg: unreal.log(str(msg))

    log(f"[ApproxBoxes] 开始从StaticMesh提取顶点，LOD={lod_index}")
    if not static_mesh:
        log("[ApproxBoxes] StaticMesh为空")
        return points

    # 获取LOD数量
    try:
        num_lods = static_mesh.get_num_lods()
        if lod_index >= num_lods:
            log(f"[ApproxBoxes] 请求的LOD {lod_index} 超出范围，重置为0")
            lod_index = 0
    except Exception as e:
        log(f"[ApproxBoxes] 获取LOD数量失败: {e}")
        lod_index = 0

    # 检查Allow CPU Access
    try:
        allow_cpu_access = static_mesh.get_editor_property("allow_cpu_access")
        if not allow_cpu_access:
            log("[ApproxBoxes] ⚠️ Allow CPU Access 未启用，建议在编辑器中打开，否则可能取不到顶点数据。")
    except Exception as e:
        log(f"[ApproxBoxes] 无法检查Allow CPU Access: {e}")

    # === 方式 1: 使用 MeshDescription ===
    log("[ApproxBoxes] 尝试方法1: MeshDescription")
    mesh_desc = None
    esml = getattr(unreal, "EditorStaticMeshLibrary", None)

    try:
        if esml:
            mesh_desc = esml.get_mesh_description(static_mesh, lod_index)
    except Exception as e:
        log(f"[ApproxBoxes] EditorStaticMeshLibrary.get_mesh_description失败: {e}")

    if not mesh_desc:
        try:
            mesh_desc = static_mesh.get_mesh_description(lod_index)
        except Exception as e:
            log(f"[ApproxBoxes] static_mesh.get_mesh_description失败: {e}")

    if mesh_desc:
        try:
            vertex_ids = mesh_desc.get_vertices()
            for vid in vertex_ids:
                pos = mesh_desc.get_vertex_position(vid)
                v = unreal.Vector(pos.x, pos.y, pos.z)
                if to_world_transform:
                    v = unreal.KismetMathLibrary.transform_location(to_world_transform, v)
                points.append(v)
            log(f"[ApproxBoxes] MeshDescription成功提取{len(points)}个顶点")
        except Exception as e:
            log(f"[ApproxBoxes] MeshDescription提取失败: {e}")
    else:
        log("[ApproxBoxes] MeshDescription不可用，转入GeometryScript路径")

    # === 方式 2: 使用 Geometry Script (UE5.1 有接口差异) ===
    if not points:
        try:
            if hasattr(unreal, 'GeometryScriptMeshReadLOD'):
                log("[ApproxBoxes] 使用 GeometryScriptMeshReadLOD (UE5.1兼容接口)")
                dyn_mesh = unreal.GeometryScriptDynamicMesh()
                result = unreal.GeometryScriptMeshReadLOD.copy_mesh_from_static_mesh_lod(
                    static_mesh, dyn_mesh, lod_index
                )
                vert_count = unreal.GeometryScriptMeshQueryFunctions.get_vertex_count(dyn_mesh)
                log(f"[ApproxBoxes] 获取到 {vert_count} 个顶点")
                for i in range(vert_count):
                    pos = unreal.GeometryScriptMeshQueryFunctions.get_vertex_position(dyn_mesh, i)
                    if to_world_transform:
                        pos = to_world_transform.transform_position(pos)
                    points.append(pos)
            elif hasattr(unreal, 'GeometryScriptLibrary'):
                # 旧接口回退
                log("[ApproxBoxes] 使用 GeometryScriptLibrary (旧版接口)")
                dyn_mesh = unreal.GeometryScriptLibrary.request_and_release_dynamic_mesh_from_global_pool()
                success = unreal.GeometryScriptLibrary.copy_mesh_from_static_mesh(dyn_mesh, static_mesh)
                if success:
                    vert_count = unreal.GeometryScriptLibrary.get_vertex_count(dyn_mesh)
                    for i in range(vert_count):
                        pos = unreal.GeometryScriptLibrary.get_vertex(dyn_mesh, i)
                        if to_world_transform:
                            pos = to_world_transform.transform_position(pos)
                        points.append(pos)
                    unreal.GeometryScriptLibrary.return_dynamic_mesh_to_global_pool(dyn_mesh)
        except Exception as e:
            log(f"[ApproxBoxes] GeometryScript 提取失败: {e}")

    # === 方式 3: KismetProceduralMeshLibrary (最终回退) ===
    if not points:
        log("[ApproxBoxes] 尝试方法3: KismetProceduralMeshLibrary")
        kpl = getattr(unreal, "KismetProceduralMeshLibrary", None)
        if not kpl:
            log("[ApproxBoxes] 未找到KismetProceduralMeshLibrary，可能插件未启用")
        else:
            try:
                section_count = static_mesh.get_num_sections(lod_index)
            except Exception:
                section_count = 1
            for s in range(section_count):
                verts, tris, normals, tangents, uvs, colors = [], [], [], [], [], []
                try:
                    kpl.get_section_from_static_mesh(static_mesh, lod_index, s, verts, tris, normals, tangents, uvs, colors)
                    for v in verts:
                        vec = unreal.Vector(v.x, v.y, v.z)
                        if to_world_transform:
                            vec = unreal.KismetMathLibrary.transform_location(to_world_transform, vec)
                        points.append(vec)
                except Exception as e:
                    log(f"[ApproxBoxes] Section {s} 提取失败: {e}")

    log(f"[ApproxBoxes] 顶点提取完成，共 {len(points)} 个点。")
    return points



def add_box_component(actor, center_world, extent):
    """在给定Actor上添加一个BoxComponent（世界空间中心 + extent）。"""
    # 创建组件
    try:
        comp = actor.add_component(unreal.BoxComponent, unreal.Transform(), False, None)
    except Exception:
        # 某些版本可能需要不同签名
        comp = actor.add_component(unreal.BoxComponent, unreal.Transform())

    # 设置外观与位置
    try:
        comp.set_box_extent(extent, False)
    except Exception:
        # 旧版本可能无set_box_extent，回退到编辑属性
        comp.set_editor_property("box_extent", extent)

    comp.set_world_location(center_world)
    # 交互与碰撞设置（可按需调整）
    try:
        comp.set_editor_property("mobility", unreal.ComponentMobility.MOVABLE)
        comp.set_editor_property("collision_enabled", unreal.CollisionEnabled.QUERY_AND_PHYSICS)
        comp.set_editor_property("collision_profile_name", "BlockAll")
    except Exception:
        pass
    comp.register_component()
    return comp


def _add_boxes_from_component_bounds(actor, component, cluster_count=1):
    """当无法提取顶点时，使用组件的世界包围 Bounds 生成世界对齐盒体。
    若 cluster_count>1，则沿最长轴均匀切分成多个盒体。
    """
    try:
        bounds = component.get_editor_property("bounds")
    except Exception:
        bounds = None
    if not bounds:
        try:
            bounds = getattr(component, "bounds", None)
        except Exception:
            bounds = None
    if not bounds:
        log("[ApproxBoxes] 无法获取组件Bounds，降级生成失败。")
        return []

    origin = getattr(bounds, "origin", None)
    box_extent = getattr(bounds, "box_extent", None)
    if not isinstance(origin, unreal.Vector) or not isinstance(box_extent, unreal.Vector):
        log("[ApproxBoxes] 组件Bounds格式不符合预期。")
        return []

    created = []
    if cluster_count <= 1:
        comp = add_box_component(actor, origin, box_extent)
        created.append(comp)
        log(f"[ApproxBoxes] 使用组件Bounds降级生成1个盒体 center={origin} extent={box_extent}")
        return created

    # 沿最长轴切分
    ex, ey, ez = box_extent.x, box_extent.y, box_extent.z
    axis = 0
    longest = ex
    if ey > longest:
        axis = 1
        longest = ey
    if ez > longest:
        axis = 2
        longest = ez

    total_len = longest * 2.0
    segment_len = total_len / float(cluster_count)
    segment_half = segment_len * 0.5

    for i in range(cluster_count):
        # 计算每个子盒的中心和extent
        cx, cy, cz = origin.x, origin.y, origin.z
        sx, sy, sz = ex, ey, ez
        if axis == 0:
            left = origin.x - ex
            center_axis = left + (i + 0.5) * segment_len
            cx = center_axis
            sx = segment_half
        elif axis == 1:
            left = origin.y - ey
            center_axis = left + (i + 0.5) * segment_len
            cy = center_axis
            sy = segment_half
        else:
            left = origin.z - ez
            center_axis = left + (i + 0.5) * segment_len
            cz = center_axis
            sz = segment_half

        center = unreal.Vector(cx, cy, cz)
        extent = unreal.Vector(sx, sy, sz)
        comp = add_box_component(actor, center, extent)
        created.append(comp)
        log(f"[ApproxBoxes] 使用组件Bounds降级生成盒体[{i}] center={center} extent={extent}")

    return created

def _try_get_world_transform_from_component(component):
    """兼容不同UE版本：尽可能从组件获取世界变换，失败则回退到Actor变换。"""
    # 1) 直接尝试常见方法名
    for m in ("get_component_transform", "get_component_to_world", "get_world_transform"):
        try:
            fn = getattr(component, m, None)
            if fn:
                t = fn()
                if isinstance(t, unreal.Transform):
                    return t
        except Exception:
            pass

    # 2) 尝试编辑器属性
    try:
        t = component.get_editor_property("world_transform")
        if isinstance(t, unreal.Transform):
            return t
    except Exception:
        pass

    # 3) 回退到Actor世界变换
    owner = None
    try:
        owner = component.get_owner()
    except Exception:
        owner = None

    if owner:
        try:
            fn = getattr(owner, "get_actor_transform", None)
            if fn:
                t = fn()
                if isinstance(t, unreal.Transform):
                    return t
        except Exception:
            pass

        # 构造Transform
        loc = unreal.Vector(0, 0, 0)
        rot = unreal.Rotator(0, 0, 0)
        scale = unreal.Vector(1, 1, 1)
        try:
            gl = getattr(owner, "get_actor_location", None)
            if gl:
                loc = gl()
            else:
                v = owner.get_editor_property("actor_location")
                if isinstance(v, unreal.Vector):
                    loc = v
        except Exception:
            pass
        try:
            gr = getattr(owner, "get_actor_rotation", None)
            if gr:
                rot = gr()
            else:
                r = owner.get_editor_property("actor_rotation")
                if isinstance(r, unreal.Rotator):
                    rot = r
        except Exception:
            pass
        try:
            gs = getattr(owner, "get_actor_scale3d", None)
            if gs:
                scale = gs()
            else:
                s = owner.get_editor_property("actor_scale3d")
                if isinstance(s, unreal.Vector):
                    scale = s
        except Exception:
            pass
        return unreal.Transform(location=loc, rotation=rot, scale=scale)

    # 4) 最后兜底为单位变换
    return unreal.Transform()


def generate_approx_boxes_from_selected_actor(cluster_count=3, lod_index=0):
    """
    从选中的 StaticMeshActor 读取其StaticMesh的几何点（转换到世界坐标），
    进行K-Means聚类并为每个簇添加一个近似AABB BoxComponent。
    """
    # 兼容获取选中Actor：优先使用EditorActorSubsystem，回退到EditorLevelLibrary
    actors = []
    try:
        eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
        actors = eas.get_selected_level_actors()
    except Exception:
        try:
            actors = unreal.EditorLevelLibrary.get_selected_level_actors()
        except Exception:
            actors = []
    if not actors:
        unreal.log_error("未选中任何Actor，请选择一个StaticMeshActor后再运行。")
        return
    actor = actors[0]
    try:
        smc = actor.static_mesh_component
    except Exception:
        unreal.log_error("选中的Actor不是StaticMeshActor或缺少static_mesh_component。")
        return
    # 兼容不同UE版本的获取方式
    static_mesh = None
    try:
        static_mesh = smc.get_static_mesh()
    except Exception:
        pass
    if not static_mesh:
        try:
            static_mesh = smc.get_editor_property("static_mesh")
        except Exception:
            pass
    if not static_mesh:
        try:
            static_mesh = smc.static_mesh
        except Exception:
            pass
    if not static_mesh:
        unreal.log_error("选中的Actor没有关联StaticMesh。")
        return

    to_world = _try_get_world_transform_from_component(smc)
    points = get_points_from_static_mesh(static_mesh, lod_index=lod_index, to_world_transform=to_world)
    if not points:
        unreal.log_warning("[ApproxBoxes] 未能从StaticMesh中提取顶点，改用组件Bounds降级生成世界对齐盒体。")
        _add_boxes_from_component_bounds(actor, smc, max(1, cluster_count))
        return

    log(f"提取点数量: {len(points)}，开始聚类: K={cluster_count}")
    clusters = kmeans(points, cluster_count)
    log(f"聚类完成，有效簇数量: {len(clusters)}")

    for idx, cluster in enumerate(clusters):
        center, extent = compute_aabb(cluster)
        comp = add_box_component(actor, center, extent)
        log(f"添加 BoxComponent[{idx}] center={center} extent={extent}")


def generate_approx_boxes_from_asset_path(asset_path, cluster_count=3, lod_index=0, spawn_new_actor=True):
    """
    直接从资产路径加载StaticMesh并生成近似盒体。
    如果spawn_new_actor=True，会在原点生成一个空Actor并添加BoxComponents（世界坐标）。
    """
    static_mesh = unreal.EditorAssetLibrary.load_asset(asset_path)
    if not static_mesh:
        unreal.log_error(f"无法加载资产: {asset_path}")
        return

    # 使用世界坐标（Identity）
    identity = unreal.Transform()
    points = get_points_from_static_mesh(static_mesh, lod_index=lod_index, to_world_transform=identity)
    if not points:
        unreal.log_error("未能从StaticMesh中提取顶点，请检查LOD/Section或启用相关编辑器插件。")
        return

    clusters = kmeans(points, cluster_count)
    log(f"聚类完成，有效簇数量: {len(clusters)}")

    target_actor = None
    if spawn_new_actor:
        target_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.Actor, unreal.Vector(0, 0, 0))
    else:
        sel = unreal.EditorLevelLibrary.get_selected_level_actors()
        if sel:
            target_actor = sel[0]
        else:
            target_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.Actor, unreal.Vector(0, 0, 0))

    for idx, cluster in enumerate(clusters):
        center, extent = compute_aabb(cluster)
        comp = add_box_component(target_actor, center, extent)
        log(f"添加 BoxComponent[{idx}] center={center} extent={extent}")


if __name__ == "__main__":
    # 示例：默认对选中Actor执行，K=3
    # generate_approx_boxes_from_selected_actor(cluster_count=2, lod_index=0)
    # import unreal

    # 1. 加载StaticMesh资产
    asset_path = '/CoveringAPI/Effects/Meshes/Mesh_FX_Car_Black_Wheel_Rear.Mesh_FX_Car_Black_Wheel_Rear'
    static_mesh = unreal.EditorAssetLibrary.load_asset(asset_path)
    if not static_mesh:
        unreal.log_error(f"无法加载StaticMesh资产: {asset_path}")
    else:
        # 2. 请求一个UDynamicMesh对象（从GlobalPool）
        dynamic_mesh = unreal.GeometryScriptLibrary.request_and_release_dynamic_mesh_from_global_pool()
        if not dynamic_mesh:
            unreal.log_error("无法获取UDynamicMesh对象")
        else:
            # 3. 复制StaticMesh数据到UDynamicMesh
            success = unreal.GeometryScriptLibrary.copy_mesh_from_static_mesh(dynamic_mesh, static_mesh)
            if not success:
                unreal.log_error("复制StaticMesh到UDynamicMesh失败")
            else:
                # 4. 获取顶点数量
                vertex_count = unreal.GeometryScriptLibrary.get_vertex_count(dynamic_mesh)
                unreal.log(f"顶点数量: {vertex_count}")
                
                # 5. 遍历所有顶点，打印顶点位置
                for vertex_id in range(vertex_count):
                    vertex_pos = unreal.GeometryScriptLibrary.get_vertex(dynamic_mesh, vertex_id)
                    unreal.log(f"顶点ID {vertex_id} 位置: {vertex_pos}")
                    
            # 6. 释放动态网格对象
            unreal.GeometryScriptLibrary.return_dynamic_mesh_to_global_pool(dynamic_mesh)