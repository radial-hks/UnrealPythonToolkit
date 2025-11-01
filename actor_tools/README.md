# Actor工具集合

本文件夹包含用于操作和管理Unreal Engine Actor的Python脚本。

## 📁 文件列表

- **`get_actor_name.py`** - 获取场景中所有Actor信息并导出为CSV
- **`get_actor_material.py`** - 获取Actor的材质信息
- **`get_folder_path.py`** - 获取Actor的文件夹路径
- **`remove_tag.py`** - 移除Actor的标签
- **`generate_approx_boxes.py`** - 近似盒体自动生成（聚类 + BoxComponent）

## 🚀 使用方法

在UE编辑器的Python控制台中运行：
```python
exec(open("actor_tools/get_actor_name.py").read())
```

### 近似盒体生成（聚类 + BoxComponent）

从选中的 `StaticMeshActor` 生成多个近似盒体：
```python
import actor_tools.generate_approx_boxes as g
g.generate_approx_boxes_from_selected_actor(cluster_count=3, lod_index=0)
```

从资产路径生成（可在场景中新建空Actor并附加BoxComponent）：
```python
import actor_tools.generate_approx_boxes as g
g.generate_approx_boxes_from_asset_path('/Game/Path/To/YourStaticMesh', cluster_count=4, lod_index=0, spawn_new_actor=True)
```

## 📋 主要功能

- **批量Actor信息提取** - 一次性获取所有Actor的详细属性
- **材质分析** - 分析Actor使用的材质
- **场景组织** - 管理Actor的文件夹结构和标签
- **数据处理** - 导出为CSV格式便于分析

## ⚠️ 注意事项

- 确保在编辑器模式下运行
- 大型场景可能需要较长处理时间
- 导出的CSV文件会保存在指定路径
- 不同 Unreal 版本的 Python API 可能有所差异，如遇接口不可用请反馈具体版本号
- 生成的 BoxComponent 默认使用 `BlockAll` 碰撞，可按需在脚本内调整