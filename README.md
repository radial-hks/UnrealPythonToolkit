# UnrealPythonToolkit

Unreal Engine Python 自动化工具集，按编辑器工作流分类。

## 目录结构

| 目录 | 分类 | 工具数 |
|------|------|--------|
| asset/ | 资产管理 | 2 |
| scene/ | 场景编辑 | 4 |
| mesh/ | 网格工具 | 5 |
| camera/ | 相机系统 | 2 |
| render/ | 渲染输出 | 2 |
| dev/ | 开发调试 | 5 |

## 工具列表

### 资产管理 (`asset/`)
| 脚本 | 功能 |
|------|------|
| material_cleanup.py | 清理 StaticMesh 未使用材质槽 |
| static_texture.py | 静态纹理处理 |

### 场景编辑 (`scene/`)
| 脚本 | 功能 |
|------|------|
| actor_info.py | 获取场景 Actor 信息导出 CSV |
| actor_material.py | 获取指定 Actor 材质信息 |
| actor_folder.py | 获取 Actor 文件夹路径 |
| actor_tag.py | 移除 Actor 标签 |

### 网格工具 (`mesh/`)
| 脚本 | 功能 |
|------|------|
| procedural_mesh.py | 添加 ProceduralMeshComponent |
| mesh_from_json.py | 从 JSON 创建程序化网格 |
| mesh_export.py | 导出网格顶点数据 |
| cluster_triangles.py | 按中心法线聚类三角面 |
| approx_boxes.py | 生成近似包围盒 |

### 相机系统 (`camera/`)
| 脚本 | 功能 |
|------|------|
| dji_camera.py | 创建 DJI 相机 CineCameraActor |
| preview.py | 场景预览截图 |

### 渲染输出 (`render/`)
| 脚本 | 功能 |
|------|------|
| export_image.py | 渲染目标导出为图像 |
| sequence.py | Sequence 相关操作 |

### 开发调试 (`dev/`)
| 脚本 | 功能 |
|------|------|
| remote_execution.py | 远程执行框架 |
| processor.py | Unreal Python 处理器 |
| processor_demo.py | 处理器使用示例 |
| syntax_check.py | Python 语法检查 |
| env_check.py | Python 环境版本检查 |

## 使用方法

在 UE Python 控制台中执行：
```python
exec(open("scene/actor_info.py").read())
```

## 数据文件

`data/example.json` — 程序化网格顶点数据示例
