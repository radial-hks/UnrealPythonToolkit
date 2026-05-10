import unreal
import os
import csv
import math
import random

"""
三角面聚类（使用中心点与法线作为特征）

说明：
- 通过 ProceduralMeshLibrary.get_section_from_static_mesh 提取 StaticMesh 的三角面数据：顶点、三角索引、法线等。
- 对每个三角面计算中心点（顶点平均）与面法线（顶点法线平均或几何法线）。
- 将中心点与法线组合为特征向量，使用纯 Python 实现的 KMeans 聚类，无第三方依赖。
- 导出两个 CSV：
  1) Triangles_Clustered.csv：每个三角面及其聚类编号
  2) Cluster_Summary.csv：每个聚类的数量、包围盒与平均法线

注意：
- Unreal Python 环境可能没有科学计算库，故本脚本实现了简易 KMeans。
- 通过 position_scale 与 normal_weight 控制位置与法线特征的权重与尺度。
"""

# === 默认配置（可根据需要修改）===
STATIC_MESH_PATH = '/Game/ResidentialBuildingsSet/Residential_Buildings_001.Residential_Buildings_001'
LOD_INDEX = 0
K_CLUSTERS = 6
POSITION_SCALE = 100.0   # 用于缩放位置坐标，减小量纲影响
NORMAL_WEIGHT = 1.5      # 增强法线方向在特征中的权重
MAX_ITERS = 30           # KMeans 最大迭代次数

OUTPUT_DIR = os.path.join(os.path.expanduser('~'), 'UnrealMeshExport')
OUT_TRIANGLES_FILENAME = 'Triangles_Clustered.csv'
OUT_CLUSTERS_FILENAME = 'Cluster_Summary.csv'


# === 工具函数 ===
def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def log(msg):
    unreal.log('[TriangleCluster] ' + str(msg))


def warn(msg):
    unreal.log_warning('[TriangleCluster] ' + str(msg))


def vector_to_tuple(v: unreal.Vector):
    return (float(v.x), float(v.y), float(v.z))


def vec_add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def vec_sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def vec_scale(v, s):
    return (v[0] * s, v[1] * s, v[2] * s)


def vec_length(v):
    return math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])


def vec_normalize(v):
    l = vec_length(v)
    if l <= 1e-8:
        return (0.0, 0.0, 0.0)
    return (v[0] / l, v[1] / l, v[2] / l)


def vec_avg3(a, b, c):
    return ((a[0] + b[0] + c[0]) / 3.0, (a[1] + b[1] + c[1]) / 3.0, (a[2] + b[2] + c[2]) / 3.0)


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


# === 数据提取 ===
def get_section_count(mesh: unreal.StaticMesh, lod_index: int) -> int:
    try:
        return mesh.get_num_sections(lod_index)
    except Exception:
        return 1


def compute_face_normal(v0, v1, v2, n0=None, n1=None, n2=None):
    """
    优先使用顶点法线的平均值；若不可用，则用几何法线（两条边叉乘）。
    参数 v0,v1,v2 为三角面三个顶点坐标（tuple）。n0,n1,n2 为可选的顶点法线（unreal.Vector 或 None）。
    """
    if n0 is not None and n1 is not None and n2 is not None:
        nn0 = vec_normalize(vector_to_tuple(n0))
        nn1 = vec_normalize(vector_to_tuple(n1))
        nn2 = vec_normalize(vector_to_tuple(n2))
        return vec_normalize(vec_avg3(nn0, nn1, nn2))
    # 使用几何法线
    e1 = vec_sub(v1, v0)
    e2 = vec_sub(v2, v0)
    return vec_normalize(cross(e1, e2))


def extract_triangle_items(static_mesh: unreal.StaticMesh, lod_index: int):
    """
    返回列表，每项：{
        'global_tri_index': int,
        'section_index': int,
        'local_tri_index': int,   # 在该 section 内的三角面序号
        'center': (x,y,z),
        'normal': (nx,ny,nz),
        'feature': [fx,fy,fz, fnx,fny,fnz],
    }
    feature 由 center/position_scale 与 normal*normal_weight 组成。
    """
    pml = unreal.ProceduralMeshLibrary
    section_count = get_section_count(static_mesh, lod_index)

    items = []
    global_tri_index = 0

    for s in range(section_count):
        try:
            section = pml.get_section_from_static_mesh(static_mesh, lod_index, s)
            vertices = section[0] if len(section) > 0 else []
            triangles = section[1] if len(section) > 1 else []
            normals = section[2] if len(section) > 2 else []
        except Exception as e:
            warn(f'无法获取 section {s}: {e}')
            vertices, triangles, normals = [], [], []

        if not vertices or not triangles:
            continue

        has_vertex_normals = isinstance(normals, (list, tuple)) and len(normals) == len(vertices)

        local_tri_index = 0
        for i in range(0, len(triangles), 3):
            if i + 2 >= len(triangles):
                break
            idx0 = int(triangles[i])
            idx1 = int(triangles[i + 1])
            idx2 = int(triangles[i + 2])

            # 顶点坐标
            v0 = vector_to_tuple(vertices[idx0])
            v1 = vector_to_tuple(vertices[idx1])
            v2 = vector_to_tuple(vertices[idx2])

            # 三角中心
            center = vec_avg3(v0, v1, v2)

            # 面法线
            if has_vertex_normals:
                n0 = normals[idx0]
                n1 = normals[idx1]
                n2 = normals[idx2]
                normal = compute_face_normal(v0, v1, v2, n0, n1, n2)
            else:
                normal = compute_face_normal(v0, v1, v2)

            # 特征向量：位置缩放 + 法线加权
            feature = [
                center[0] / POSITION_SCALE,
                center[1] / POSITION_SCALE,
                center[2] / POSITION_SCALE,
                normal[0] * NORMAL_WEIGHT,
                normal[1] * NORMAL_WEIGHT,
                normal[2] * NORMAL_WEIGHT,
            ]

            items.append({
                'global_tri_index': global_tri_index,
                'section_index': s,
                'local_tri_index': local_tri_index,
                'center': center,
                'normal': normal,
                'feature': feature,
            })

            global_tri_index += 1
            local_tri_index += 1

    return items


# === KMeans 聚类（无依赖，简易实现）===
def sqr_dist(a, b):
    return sum((a[d] - b[d]) * (a[d] - b[d]) for d in range(len(a)))


def kmeans(feature_vectors, k, max_iters=30):
    n = len(feature_vectors)
    if n == 0:
        return [], []
    k = max(1, min(k, n))

    # 初始化中心（随机采样，固定种子保证可重复性）
    random.seed(42)
    init_indices = random.sample(range(n), k)
    centroids = [list(feature_vectors[i]) for i in init_indices]

    assignments = [-1] * n

    for _ in range(max_iters):
        changed = 0
        # 1) 分配最近中心
        for i, fv in enumerate(feature_vectors):
            best_j = 0
            best_d = sqr_dist(fv, centroids[0])
            for j in range(1, k):
                d = sqr_dist(fv, centroids[j])
                if d < best_d:
                    best_d = d
                    best_j = j
            if assignments[i] != best_j:
                assignments[i] = best_j
                changed += 1

        # 若无变化，提前结束
        if changed == 0:
            break

        # 2) 重新计算中心
        dim = len(feature_vectors[0])
        new_centroids = [[0.0] * dim for _ in range(k)]
        counts = [0] * k

        for i, fv in enumerate(feature_vectors):
            j = assignments[i]
            counts[j] += 1
            for d in range(dim):
                new_centroids[j][d] += fv[d]

        # 归一化 + 处理空簇
        for j in range(k):
            if counts[j] > 0:
                inv = 1.0 / counts[j]
                for d in range(dim):
                    new_centroids[j][d] *= inv
            else:
                # 空簇则随机重置为某个样本
                ridx = random.randrange(n)
                new_centroids[j] = list(feature_vectors[ridx])

        centroids = new_centroids

    return assignments, centroids


# === 结果摘要（包围盒与平均法线）===
def summarize_clusters(items, assignments, k):
    clusters = []
    for _ in range(k):
        clusters.append({
            'count': 0,
            'min': [float('inf'), float('inf'), float('inf')],
            'max': [float('-inf'), float('-inf'), float('-inf')],
            'sum_normal': [0.0, 0.0, 0.0],
        })

    for item, cid in zip(items, assignments):
        if cid < 0 or cid >= k:
            continue
        c = item['center']
        n = item['normal']
        cluster = clusters[cid]
        cluster['count'] += 1
        # 包围盒更新
        cluster['min'][0] = min(cluster['min'][0], c[0])
        cluster['min'][1] = min(cluster['min'][1], c[1])
        cluster['min'][2] = min(cluster['min'][2], c[2])
        cluster['max'][0] = max(cluster['max'][0], c[0])
        cluster['max'][1] = max(cluster['max'][1], c[1])
        cluster['max'][2] = max(cluster['max'][2], c[2])
        # 平均法线累加
        cluster['sum_normal'][0] += n[0]
        cluster['sum_normal'][1] += n[1]
        cluster['sum_normal'][2] += n[2]

    summaries = []
    for cid, cluster in enumerate(clusters):
        cnt = cluster['count']
        if cnt > 0:
            avg_n = vec_scale(cluster['sum_normal'], 1.0 / cnt)
            avg_n = vec_normalize(avg_n)
        else:
            avg_n = (0.0, 0.0, 0.0)
        summaries.append({
            'cluster_id': cid,
            'count': cnt,
            'min_x': cluster['min'][0],
            'min_y': cluster['min'][1],
            'min_z': cluster['min'][2],
            'max_x': cluster['max'][0],
            'max_y': cluster['max'][1],
            'max_z': cluster['max'][2],
            'avg_nx': avg_n[0],
            'avg_ny': avg_n[1],
            'avg_nz': avg_n[2],
        })
    return summaries


# === 包围盒绘制 ===
def create_cluster_box_actors(summaries):
    """
    为每个聚类创建包围盒（使用 StaticMeshActor + Cube 作为可视化），避免使用已弃用的接口。
    返回创建的Actor列表。
    """
    created_actors = []

    # 预定义颜色列表（用于区分不同聚类）
    colors = [
        (1.0, 0.0, 0.0, 0.3),  # 红色
        (0.0, 1.0, 0.0, 0.3),  # 绿色
        (0.0, 0.0, 1.0, 0.3),  # 蓝色
        (1.0, 1.0, 0.0, 0.3),  # 黄色
        (1.0, 0.0, 1.0, 0.3),  # 洋红
        (0.0, 1.0, 1.0, 0.3),  # 青色
        (1.0, 0.5, 0.0, 0.3),  # 橙色
        (0.5, 0.0, 1.0, 0.3),  # 紫色
        (0.0, 0.5, 0.0, 0.3),  # 深绿
        (0.5, 0.5, 0.5, 0.3),  # 灰色
        (1.0, 0.75, 0.8, 0.3), # 粉色
        (0.6, 0.4, 0.2, 0.3),  # 棕色
    ]

    for summary in summaries:
        cluster_id = summary['cluster_id']
        count = summary['count']
        if count == 0:
            continue

        # 计算包围盒中心与extent（半尺寸）
        min_pos = (summary['min_x'], summary['min_y'], summary['min_z'])
        max_pos = (summary['max_x'], summary['max_y'], summary['max_z'])
        center = (
            (min_pos[0] + max_pos[0]) * 0.5,
            (min_pos[1] + max_pos[1]) * 0.5,
            (min_pos[2] + max_pos[2]) * 0.5
        )
        size = (
            max(abs(max_pos[0] - min_pos[0]), 1.0),
            max(abs(max_pos[1] - min_pos[1]), 1.0),
            max(abs(max_pos[2] - min_pos[2]), 1.0)
        )
        extent = unreal.Vector(size[0] * 0.5, size[1] * 0.5, size[2] * 0.5)

        color = colors[cluster_id % len(colors)]
        actor_name = f'ClusterBox_{cluster_id:02d}'

        actor = spawn_cluster_box_actor(
            center_world=unreal.Vector(center[0], center[1], center[2]),
            extent=extent,
            color=color,
            actor_name=actor_name,
        )
        if actor:
            created_actors.append(actor)
            log(f'创建聚类包围盒: {actor_name} (三角面数: {count})')
        else:
            warn(f'创建聚类 {cluster_id} 的包围盒失败')

    log(f'成功创建 {len(created_actors)} 个聚类包围盒')
    return created_actors


def spawn_cluster_box_actor(center_world: unreal.Vector, extent: unreal.Vector, color, actor_name: str):
    """
    生成一个 StaticMeshActor，设置Cube网格、缩放与位置，并应用颜色材质。
    """
    # 尝试通过 EditorActorSubsystem 生成Actor，失败则回退到 EditorLevelLibrary
    actor = None
    try:
        editor_actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
        actor = editor_actor_sub.spawn_actor_from_class(unreal.StaticMeshActor, center_world)
    except Exception:
        try:
            actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, center_world)
        except Exception:
            actor = None

    if not actor:
        return None

    try:
        actor.set_actor_label(actor_name)
    except Exception:
        pass

    # 获取 StaticMeshComponent
    smc = None
    try:
        smc = actor.static_mesh_component
    except Exception:
        try:
            comps = actor.get_components_by_class(unreal.StaticMeshComponent)
            if comps:
                smc = comps[0]
        except Exception:
            smc = None

    # 加载Cube资产
    cube_paths = [
        '/Engine/BasicShapes/Cube',
        '/Engine/BasicShapes/Cube.Cube',
        '/Game/StarterContent/Shapes/Shape_Cube.Shape_Cube',
    ]
    cube_asset = None
    for p in cube_paths:
        try:
            cube_asset = unreal.EditorAssetLibrary.load_asset(p)
        except Exception:
            cube_asset = None
        if cube_asset:
            break

    if smc and cube_asset:
        try:
            smc.set_static_mesh(cube_asset)
        except Exception:
            try:
                smc.set_editor_property('static_mesh', cube_asset)
            except Exception:
                pass

        # 立方体默认尺寸约100uu，按extent计算缩放
        size = 100.0
        scale_vec = unreal.Vector(
            (extent.x * 2.0) / size,
            (extent.y * 2.0) / size,
            (extent.z * 2.0) / size,
        )
        try:
            smc.set_world_scale3d(scale_vec)
        except Exception:
            try:
                actor.set_actor_scale3d(scale_vec)
            except Exception:
                pass

        try:
            actor.set_actor_location(center_world, False, False)
        except Exception:
            pass

        # 应用颜色材质
        mat = create_cluster_material(0, color)
        if mat:
            try:
                smc.set_material(0, mat)
            except Exception:
                pass

        # 移动性与碰撞
        try:
            smc.set_editor_property('mobility', unreal.ComponentMobility.MOVABLE)
        except Exception:
            pass
        try:
            smc.set_editor_property('collision_enabled', unreal.CollisionEnabled.QUERY_AND_PHYSICS)
            smc.set_editor_property('collision_profile_name', 'BlockAll')
        except Exception:
            pass

    return actor


def create_cluster_material(cluster_id, color):
    """
    为聚类创建半透明彩色材质
    
    参数:
    - cluster_id: 聚类ID
    - color: RGBA颜色元组 (r, g, b, a)
    
    返回: MaterialInstanceDynamic 或 None
    """
    try:
        # 使用引擎默认的半透明材质作为基础
        base_material = unreal.EditorAssetLibrary.load_asset('/Engine/BasicShapes/BasicShapeMaterial')
        if not base_material:
            # 如果找不到基础材质，尝试创建简单的材质实例
            return None
            
        # 创建动态材质实例
        material_instance = unreal.MaterialInstanceDynamic.create(base_material, None)
        if material_instance:
            # 设置颜色参数（如果材质支持）
            try:
                material_instance.set_vector_parameter_value('Color', unreal.LinearColor(color[0], color[1], color[2], color[3]))
            except:
                # 如果不支持Color参数，尝试其他常见参数名
                try:
                    material_instance.set_vector_parameter_value('BaseColor', unreal.LinearColor(color[0], color[1], color[2], color[3]))
                except:
                    pass
        
        return material_instance
        
    except Exception as e:
        warn(f'创建聚类 {cluster_id} 材质时出错: {e}')
        return None


# === CSV 输出 ===
def write_triangles_csv(items, assignments, out_path):
    ensure_dir(os.path.dirname(out_path))
    with open(out_path, mode='w', newline='') as f:
        w = csv.writer(f)
        w.writerow([
            'GlobalTriangleIndex', 'SectionIndex', 'LocalTriangleIndex',
            'CenterX', 'CenterY', 'CenterZ',
            'NormalX', 'NormalY', 'NormalZ',
            'ClusterID'
        ])
        for item, cid in zip(items, assignments):
            c = item['center']
            n = item['normal']
            w.writerow([
                item['global_tri_index'], item['section_index'], item['local_tri_index'],
                c[0], c[1], c[2], n[0], n[1], n[2], cid
            ])


def write_clusters_csv(summaries, out_path):
    ensure_dir(os.path.dirname(out_path))
    with open(out_path, mode='w', newline='') as f:
        w = csv.writer(f)
        w.writerow([
            'ClusterID', 'Count',
            'MinX', 'MinY', 'MinZ', 'MaxX', 'MaxY', 'MaxZ',
            'AvgNormalX', 'AvgNormalY', 'AvgNormalZ'
        ])
        for s in summaries:
            w.writerow([
                s['cluster_id'], s['count'],
                s['min_x'], s['min_y'], s['min_z'], s['max_x'], s['max_y'], s['max_z'],
                s['avg_nx'], s['avg_ny'], s['avg_nz']
            ])


# === 主流程 ===
def cluster_triangles_using_center_normal(
    static_mesh_path: str,
    lod_index: int = LOD_INDEX,
    k_clusters: int = K_CLUSTERS,
    position_scale: float = POSITION_SCALE,
    normal_weight: float = NORMAL_WEIGHT,
    out_dir: str = OUTPUT_DIR,
    out_triangles_filename: str = OUT_TRIANGLES_FILENAME,
    out_clusters_filename: str = OUT_CLUSTERS_FILENAME,
    draw_boxes: bool = True,
    clear_existing_boxes: bool = True,
):
    global POSITION_SCALE, NORMAL_WEIGHT
    POSITION_SCALE = position_scale
    NORMAL_WEIGHT = normal_weight

    mesh = unreal.EditorAssetLibrary.load_asset(static_mesh_path)
    if not mesh:
        unreal.log_error(f'无法加载 StaticMesh: {static_mesh_path}')
        return False

    log(f'开始提取三角面特征：{static_mesh_path} (LOD {lod_index})')
    items = extract_triangle_items(mesh, lod_index)
    if not items:
        warn('未提取到三角面数据，请检查 LOD/section 设置')
        return False

    features = [it['feature'] for it in items]
    log(f'提取完成，三角面数量：{len(items)}，开始 KMeans(k={k_clusters})')

    assignments, centroids = kmeans(features, k_clusters, MAX_ITERS)
    if not assignments:
        warn('聚类未产生有效结果')
        return False

    out_tri_path = os.path.join(out_dir, out_triangles_filename)
    write_triangles_csv(items, assignments, out_tri_path)
    log(f'三角面聚类结果已导出：{out_tri_path}')

    summaries = summarize_clusters(items, assignments, min(k_clusters, len(items)))
    out_cls_path = os.path.join(out_dir, out_clusters_filename)
    write_clusters_csv(summaries, out_cls_path)
    log(f'聚类摘要已导出：{out_cls_path}')

    # 绘制包围盒（可选）
    if draw_boxes:
        # 清理现有的聚类包围盒Actor（可选）
        if clear_existing_boxes:
            clear_cluster_box_actors()
        
        # 创建新的包围盒Actor
        created_actors = create_cluster_box_actors(summaries)
        if created_actors:
            log(f'已在场景中创建 {len(created_actors)} 个聚类包围盒')
        else:
            warn('未能创建任何包围盒Actor')

    return True


def clear_cluster_box_actors():
    """
    清理场景中现有的聚类包围盒Actor（名称以 'ClusterBox_' 开头的Actor）
    """
    try:
        # 使用 EditorActorSubsystem 获取所有 Actor（避免弃用接口）
        editor_actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
        all_actors = editor_actor_sub.get_all_level_actors()
        
        deleted_count = 0
        for actor in all_actors:
            if actor and hasattr(actor, 'get_actor_label'):
                label = actor.get_actor_label()
                if label and label.startswith('ClusterBox_'):
                    unreal.EditorLevelLibrary.destroy_actor(actor)
                    deleted_count += 1
        
        if deleted_count > 0:
            log(f'已清理 {deleted_count} 个现有的聚类包围盒Actor')
            
    except Exception as e:
        warn(f'清理现有包围盒时出错: {e}')


if __name__ == '__main__':
    cluster_triangles_using_center_normal(
        STATIC_MESH_PATH,
        LOD_INDEX,
        K_CLUSTERS,
        POSITION_SCALE,
        NORMAL_WEIGHT,
        OUTPUT_DIR,
        OUT_TRIANGLES_FILENAME,
        OUT_CLUSTERS_FILENAME,
        draw_boxes=True,
        clear_existing_boxes=True,
    )