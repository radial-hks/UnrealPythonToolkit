# 相机工具集合

本文件夹包含用于创建和配置Unreal Engine相机系统的Python脚本。

## 📁 文件列表

- **`add_dji_camera.py`** - 创建DJI相机的CineCameraActor
- **`add_dji_camera_1.py`** - DJI相机脚本的备选版本
- **`preview_png.py`** - 快速预览功能

## 🎯 主要功能

### DJI相机设置 (`add_dji_camera.py`)
- **专业级配置**: 模拟真实DJI相机参数
- **传感器设置**: 36mm x 24mm传感器尺寸
- **焦距控制**: 45mm焦距配置
- **高分辨率**: 支持6868 x 4588分辨率输出
- **FOV计算**: 自动计算水平和垂直视场角
- **调试可视化**: 显示相机视锥体

## 🚀 使用方法

```python
# 创建DJI相机
exec(open("camera_tools/add_dji_camera.py").read())

# 快速预览
exec(open("camera_tools/preview_png.py").read())
```

## ⚙️ 配置选项

脚本中的可配置参数：
- `use_existing_actor` - 是否使用现有Actor
- `location_cm` - 相机位置（厘米单位）
- `pitch/yaw/roll` - 相机旋转角度
- `focal_length_mm` - 焦距（毫米）
- `sensor_w_mm/sensor_h_mm` - 传感器尺寸
- `res_w/res_h` - 输出分辨率

## 📋 应用场景

- **影视制作**: 专业级相机设置
- **建筑可视化**: 高质量渲染
- **产品展示**: 精确视角控制
- **VR/AR开发**: 沉浸式体验

## ⚠️ 注意事项

- 确保编辑器视口分辨率设置正确
- 高分辨率输出可能消耗大量内存
- 相机参数可根据具体需求调整