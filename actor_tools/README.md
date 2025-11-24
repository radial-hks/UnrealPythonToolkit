# Actor工具集合

本文件夹包含用于操作和管理Unreal Engine Actor的Python脚本。

## 📁 文件列表

- **`get_actor_name.py`** - 获取场景中所有Actor信息并导出为CSV
- **`get_actor_material.py`** - 获取Actor的材质信息
- **`get_folder_path.py`** - 获取Actor的文件夹路径
- **`remove_tag.py`** - 移除Actor的标签
- **`generate_approx_boxes.py`** - 近似盒体自动生成（聚类 + BoxComponent/Cube降级）
- **`export_mesh_vertices.py`** - 导出StaticMesh顶点到CSV（基于 ProceduralMeshLibrary）
- **`add_ProceduralMeshComponent.py`** - 为选中的Actor添加ProceduralMeshComponent组件
- **`create_proc_mesh_from_json.py`** - 从JSON文件创建程序化网格体Actor

## 🚀 使用方法

在UE编辑器的Python控制台中运行：
```python
exec(open("actor_tools/get_actor_name.py").read())
```

### 添加ProceduralMeshComponent组件

为场景中选中的所有Actor添加ProceduralMeshComponent组件：
```python
exec(open("actor_tools/add_ProceduralMeshComponent.py").read())
```

该脚本将：
1. 获取所有选中的Actor
2. 使用SubobjectDataSubsystem添加ProceduralMeshComponent组件
3. 自动重命名组件为"MyProceduralMesh"
4. 保存Actor改动

### 从JSON创建程序化网格体

从JSON文件创建带有网格体数据的新Actor：

首先准备JSON文件（包含顶点和多边形数据）：
```json
{
  "vertices": [[x1, y1, z1], [x2, y2, z2], ...],
  "polygons": [[v0, v1, v2], [v0, v2, v3], ...]
}
```

然后在脚本中配置路径和运行：
```python
exec(open("actor_tools/create_proc_mesh_from_json.py").read())
```

配置项（在脚本顶部）：
- `json_path` - JSON文件路径
- `actor_name` - 创建的Actor名称
- `spawn_location` - Actor生成位置（unreal.Vector）
- `material_path` - 材质资产路径

### 近似盒体生成（聚类 + BoxComponent / Cube降级）

从选中的 `StaticMeshActor` 生成多个近似盒体：
```python
import actor_tools.generate_approx_boxes as g
g.generate_approx_boxes_from_selected_actor(cluster_count=3, lod_index=0)
```

从资产路径生成（可在场景中新建空Actor并附加BoxComponent；若组件不可用将降级为Cube静态网格）：
```python
import actor_tools.generate_approx_boxes as g
g.generate_approx_boxes_from_asset_path('/Game/Path/To/YourStaticMesh', cluster_count=4, lod_index=0, spawn_new_actor=True)
```

说明：
- 顶点提取优先使用 `ProceduralMeshLibrary.get_section_from_static_mesh`（与 `export_mesh_vertices.py` 一致）。
- 若插件或接口不可用，回退到 `MeshDescription` → `Geometry Script` → `KismetProceduralMeshLibrary`。
- 若仍无法提取顶点，将基于组件 Bounds 或资产 Bounds（`StaticMesh.get_bounds` / `extended_bounds` / `bounding_box`）生成世界轴对齐的近似盒体，并按最长轴切分为 `cluster_count` 个子盒。
- 在部分UE版本中 `Actor.add_component` 不可用时，会自动降级：生成基础 `Cube` 静态网格Actor并按盒体尺寸缩放；无法加载Cube资产时，会生成空Actor标记位置。

### 顶点导出（CSV）

从资产路径导出顶点到 CSV（基于 `ProceduralMeshLibrary`）：
```python
import actor_tools.export_mesh_vertices as ev
ev.export_vertices_using_proceduralmesh('/Game/Path/To/YourStaticMesh', lod_index=0, out_csv_path='C:/Temp/StaticMesh_Vertices.csv')
```
或直接运行脚本：
```python
exec(open("actor_tools/export_mesh_vertices.py").read())
```

## 📋 主要功能

- **批量Actor信息提取** - 一次性获取所有Actor的详细属性
- **材质分析** - 分析Actor使用的材质
- **场景组织** - 管理Actor的文件夹结构和标签
- **数据处理** - 导出为CSV格式便于分析
- **近似盒体生成** - 对静态网格进行聚类与AABB计算，自动生成多个近似盒体（支持无顶点API环境的降级）
- **顶点导出** - 从StaticMesh提取顶点并导出为CSV
- **ProceduralMeshComponent管理** - 为Actor添加和配置程序化网格组件
- **程序化网格体创建** - 从JSON文件数据创建带有自定义网格的Actor

## ⚠️ 注意事项

- 确保在编辑器模式下运行
- 大型场景可能需要较长处理时间
- 导出的CSV文件会保存在指定路径
- 不同 Unreal 版本的 Python API 可能有所差异，如遇接口不可用请反馈具体版本号
- 生成的 BoxComponent 默认使用 `BlockAll` 碰撞，可按需在脚本内调整
- 若需使用 `ProceduralMeshLibrary` 顶点提取，请启用“Procedural Mesh”插件（提供 `unreal.ProceduralMeshLibrary`）。
- 若需使用几何脚本路径，请启用“Geometry Scripting”插件（`unreal.GeometryScript*`）。
- 建议在 StaticMesh 资产上开启 `Allow CPU Access`，以提升顶点读取的成功率。
- 降级使用基础 `Cube` 资产依赖 Engine 内容或 StarterContent（如 `/Engine/BasicShapes/Cube`），请确保项目已包含或可访问。