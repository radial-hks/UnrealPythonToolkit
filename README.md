# UnrealPythonToolkit

一个全面的Unreal Engine Python自动化脚本工具集，包含Actor操作、材质处理、相机系统、导出工具等多个模块的实用脚本。

## 📁 文件夹结构

```
UnrealPythonToolkit/
├── actor_tools/           # Actor相关工具
├── camera_tools/          # 相机系统工具
├── material_tools/        # 材质处理工具
├── export_tools/          # 导出工具
├── framework/             # 框架和处理器
├── system_utils/          # 系统工具
└── README.md             # 本文档
```

## 🚀 工具分类

### 🎭 Actor工具 (`actor_tools/`)

#### `get_actor_name.py`
- **功能**: 获取场景中所有Actor信息并导出为CSV文件
- **用途**: 批量获取Actor名称、EID标签和路径信息
- **输出**: `actor_info_2.csv` - 包含EID、类型、Actor路径

#### `get_actor_material.py`
- **功能**: 获取指定Actor的材质信息
- **用途**: 分析和管理Actor材质分配

#### `get_folder_path.py`
- **功能**: 获取Actor所在的文件夹路径
- **用途**: 场景组织和管理

#### `remove_tag.py`
- **功能**: 移除Actor的标签
- **用途**: 清理和管理Actor标签

### 📷 相机工具 (`camera_tools/`)

#### `add_dji_camera.py` / `add_dji_camera_1.py`
- **功能**: 创建DJI相机的CineCameraActor
- **特性**:
  - 支持精确的传感器尺寸设置（36mm x 24mm）
  - 可配置焦距（45mm）
  - 高分辨率输出支持（6868 x 4588）
  - FOV计算和调试可视化
- **用途**: 影视级相机设置，无人机镜头模拟

#### `preview_png.py`
- **功能**: 快速预览功能
- **用途**: 场景预览和截图

### 🎨 材质工具 (`material_tools/`)

#### `remove_unused_material_slots.py` (主版本)
- **功能**: 智能清理StaticMesh中未使用的材质槽
- **特性**:
  - 基于几何体实际使用情况的精确分析
  - 支持LOD级别的材质槽映射
  - 自动重建材质索引
  - 兼容UE5
- **版本**:
  - `remove_unused_material_slots.py` - 主版本
  - `remove_unused_material_slots_1.py` - 早期版本
  - `remove_unused_material_slots_latest.py` - 最新版本
  - `remove_unused_material_slots copy.py` - 备份版本

#### `StaticTexture.py`
- **功能**: 静态纹理处理工具
- **用途**: 纹理创建和编辑

### 📤 导出工具 (`export_tools/`)

#### `export_to_image.py`
- **功能**: 将渲染目标导出为图像文件
- **特性**:
  - 支持HDR格式导出
  - 自定义导出路径
  - 纹理数据处理
- **用途**: 高质量图像导出和渲染结果保存

#### `sequence.py`
- **功能**: 序列相关工具
- **用途**: Level Sequence操作和管理

### ⚙️ 框架工具 (`framework/`)

#### `unreal_python_processor.py`
- **功能**: Unreal Engine Python代码综合处理器
- **特性**:
  - 代码分析和验证
  - 优化建议
  - 代码模板生成
  - 批量处理目录
  - 安全检查
- **用途**: Python脚本质量保证和开发效率提升

#### `demo_processor_usage.py`
- **功能**: Python处理器的使用演示
- **用途**: 学习和参考

#### `remote_execution.py`
- **功能**: 远程执行框架
- **特性**:
  - UDP多播节点发现
  - TCP命令通道
  - 跨实例脚本执行
- **用途**: 多UE实例间的协调和自动化

#### `syntax_check.py`
- **功能**: Python脚本语法检查工具
- **用途**: 代码质量保证

#### `README_UnrealPythonProcessor.md`
- **内容**: UnrealPythonProcessor的详细文档

### 🔧 系统工具 (`system_utils/`)

#### `sys_verison.py`
- **功能**: Python系统版本检查
- **用途**: 环境诊断和兼容性检查

## 📋 使用要求

- **Unreal Engine**: 5.0+
- **Python**: UE内置Python环境
- **权限**: 需要编辑器级别权限

## 🚀 快速开始

### 1. Actor信息导出
```python
# 在UE Python控制台中运行
exec(open("actor_tools/get_actor_name.py").read())
```

### 2. 材质槽清理
```python
# 选中要处理的StaticMesh，然后运行
exec(open("material_tools/remove_unused_material_slots.py").read())
```

### 3. DJI相机创建
```python
# 创建专业的DJI相机设置
exec(open("camera_tools/add_dji_camera.py").read())
```

## 📚 最佳实践

### 💡 使用建议
1. **备份项目**: 在运行清理脚本前务必备份项目
2. **测试环境**: 先在测试环境中验证脚本效果
3. **版本控制**: 使用Git等工具跟踪脚本变更
4. **文档阅读**: 详细阅读每个脚本的注释和配置选项

### ⚠️ 注意事项
- 材质清理操作不可逆，请谨慎使用
- 远程执行功能需要网络配置
- 高分辨率渲染可能消耗大量内存
- 部分脚本需要特定的Unreal Engine版本

## 🛠️ 扩展开发

### 添加新工具
1. 在对应分类文件夹中创建新脚本
2. 遵循现有的命名规范和文档格式
3. 添加适当的错误处理和日志记录
4. 更新本README文档

### 代码规范
- 使用清晰的函数和变量命名
- 添加详细的中文注释
- 包含必要的错误处理
- 提供使用示例

## 📝 更新日志

### v1.0.0 (2025-10-28)
- 🎉 初始版本发布
- 📁 文件夹结构重组和分类
- 📚 完整的文档编写
- 🛠️ 工具标准化和优化

## 🤝 贡献

欢迎提交问题报告、功能请求和代码贡献。请确保：
- 代码符合项目规范
- 包含必要的测试
- 更新相关文档

## 📄 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 🔗 相关链接

- [Unreal Engine Python文档](https://docs.unrealengine.com/en-US/PythonAPI/)
- [Unreal Engine Python脚本指南](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-scripting)

---

**Happy Coding with Unreal Python! 🎮✨**