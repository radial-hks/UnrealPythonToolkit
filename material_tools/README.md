# 材质工具集合

本文件夹包含用于处理和管理Unreal Engine材质的Python脚本。

## 📁 文件列表

- **`remove_unused_material_slots.py`** - 主版本：智能清理未使用材质槽
- **`remove_unused_material_slots_1.py`** - 早期版本
- **`remove_unused_material_slots_latest.py`** - 最新版本
- **`remove_unused_material_slots copy.py`** - 备份版本
- **`StaticTexture.py`** - 静态纹理处理工具

## 🎯 主要功能

### 材质槽清理工具
智能识别并清理StaticMesh中未被几何体实际使用的材质槽：

#### ✨ 核心特性
- **精确分析**: 基于几何体实际使用情况，而非简单的空槽检查
- **LOD支持**: 支持多LOD级别的材质槽映射分析
- **索引重映射**: 删除后自动重建材质索引，确保引用正确
- **UE5兼容**: 完全兼容Unreal Engine 5
- **安全操作**: 只删除真正未使用的材质槽

#### 🔍 工作原理
1. 遍历StaticMesh的所有LOD和section
2. 分析每个section实际使用的材质槽索引
3. 识别未被任何section引用的材质槽
4. 安全删除未使用的材质槽
5. 重建材质索引并更新所有section引用

## 🚀 使用方法

### 智能材质清理（推荐）
```python
# 清理选中的StaticMesh
exec(open("material_tools/remove_unused_material_slots.py").read())
```

### 脚本配置
```python
# 只处理选中的资产（默认）
remove_unused_material_slots(selected_only=True)

# 处理项目中所有StaticMesh
remove_unused_material_slots(selected_only=False)
```

## 📊 版本说明

| 版本 | 说明 | 推荐度 |
|------|------|--------|
| `remove_unused_material_slots.py` | 主版本，功能最完整 | ⭐⭐⭐⭐⭐ |
| `remove_unused_material_slots_latest.py` | 最新实验功能 | ⭐⭐⭐⭐ |
| `remove_unused_material_slots_1.py` | 早期稳定版本 | ⭐⭐⭐ |
| `remove_unused_material_slots copy.py` | 备份版本 | ⭐⭐ |

## ⚠️ 重要注意事项

### 🔴 安全警告
- **不可逆操作**: 材质槽删除后无法撤销
- **备份项目**: 使用前务必创建项目备份
- **测试验证**: 先在测试环境中验证效果

### ✅ 最佳实践
1. 备份项目文件
2. 在测试环境中验证
3. 选中少量资产进行测试
4. 确认效果后再批量处理

## 🔧 技术细节

### 材质槽分析算法
- **GeometryScript方法**: 优先使用UE5的GeometryScript API
- **渲染数据回退**: 当GeometryScript不可用时使用渲染数据分析
- **简单检查回退**: 最后的安全检查方案

### 性能优化
- **批量处理**: 支持多资产同时处理
- **内存管理**: 优化大项目的内存使用
- **日志控制**: 可调节日志详细程度

## 📋 适用场景

- **项目优化**: 减少不必要的材质槽数量
- **性能提升**: 降低材质加载和渲染开销
- **资源整理**: 清理冗余材质引用
- **版本控制**: 减少项目文件差异

## 🐛 故障排除

### 常见问题
1. **权限错误**: 确保资产没有被其他程序占用
2. **内存不足**: 分批处理大量资产
3. **引用错误**: 检查材质实例是否正确

### 调试选项
- 设置 `VERBOSE_SECTION_UPDATE_LOG = True` 查看详细日志
- 检查UE编辑器输出窗口的错误信息

---

**使用前请务必备份项目！** 💾