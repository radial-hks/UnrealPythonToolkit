# 系统工具集合

本文件夹包含用于系统诊断和环境检查的Python工具。

## 📁 文件列表

- **`sys_verison.py`** - Python系统版本检查工具

## 🎯 主要功能

### 系统版本检查 (`sys_verison.py`)
用于诊断Unreal Engine内置Python环境的基本信息：

#### ✨ 检查内容
- **Python版本**: 显示当前Python解释器版本
- **执行路径**: 显示Python可执行文件路径
- **环境信息**: 提供环境诊断基础信息

#### 🔧 用途
- **环境诊断**: 确认Python环境是否正常
- **兼容性检查**: 验证Python版本兼容性
- **问题排查**: 提供基础的环境信息

## 🚀 使用方法

### 基本使用
```python
# 在UE Python控制台中运行
exec(open("system_utils/sys_verison.py").read())
```

### 输出示例
```
Python Version: 3.9.7 (default, Sep 16 2021, 16:59:28) [MSC v.1929 64 bit (AMD64)]
Python Executable Path: C:/Program Files/Epic Games/UE_5.1/Engine/Binaries/ThirdParty/Python3/Win64/python.exe
```

## 📋 应用场景

### 🐛 问题诊断
当遇到以下问题时，首先运行版本检查：
- Python脚本无法执行
- 导入模块失败
- 兼容性错误
- 性能问题

### 🔧 环境配置
- **版本确认**: 确认Python版本符合要求
- **路径验证**: 验证Python安装路径
- **升级规划**: 为Python版本升级提供参考

### 📚 开发参考
- **代码兼容**: 确保代码与当前Python版本兼容
- **功能支持**: 确认特定功能是否支持
- **调试基础**: 为其他工具提供环境信息

## 🔍 技术细节

### 检查原理
脚本使用Python内置的`sys`模块获取系统信息：
```python
import sys
print("Python Version:", sys.version)
print("Python Executable Path:", sys.executable)
```

### 信息解读
- **版本号格式**: 主版本.次版本.修订版本
- **编译信息**: 包含编译器和平台信息
- **路径重要性**: 用于验证Python环境配置

## ⚠️ 注意事项

### 🔍 版本兼容性
- **UE4**: 通常使用Python 2.7（已弃用）
- **UE5**: 使用Python 3.7+，推荐3.9+
- **模块支持**: 确认所需模块与当前版本兼容

### 🚨 常见问题
1. **版本过低**: 某些现代Python功能不支持
2. **路径异常**: Python环境配置可能有问题
3. **权限问题**: 可能无法访问某些系统信息

## 🔧 扩展功能

可以基于现有脚本添加更多系统检查功能：

### 系统信息扩展
```python
import platform
import sys
import os

def comprehensive_system_check():
    print("=== 系统信息 ===")
    print("操作系统:", platform.system())
    print("系统版本:", platform.version())
    print("处理器:", platform.processor())
    print("Python版本:", sys.version)
    print("Python路径:", sys.executable)
    print("当前工作目录:", os.getcwd())
```

### 模块检查
```python
def check_modules():
    modules = ['unreal', 'math', 'csv', 'json']
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module}: 已安装")
        except ImportError:
            print(f"❌ {module}: 未安装")
```

## 📊 性能基准

基于系统信息，可以建立性能基准：
- **Python版本性能**: 不同版本的性能差异
- **平台兼容性**: 不同平台的特性支持
- **资源占用**: 基础环境的资源使用情况

## 🔗 相关工具

这个工具是其他所有工具的基础，建议在遇到问题时首先运行：
- **诊断流程**: 版本检查 → 错误分析 → 解决方案
- **兼容性验证**: 在安装新工具前确认环境
- **性能优化**: 基于系统信息优化脚本性能

## 📝 使用建议

### 🎯 最佳实践
1. **定期检查**: 在重要操作前检查环境
2. **记录基线**: 保存正常的系统信息作为参考
3. **问题文档**: 记录遇到的问题和解决方案
4. **版本追踪**: 跟踪Python版本变化的影响

### 📋 检查清单
- [ ] Python版本是否符合要求
- [ ] 所有必需模块是否可用
- [ ] 系统路径是否正确
- [ ] 权限设置是否合适

---

**系统环境检查是确保Python脚本正常运行的第一步！** 🔧