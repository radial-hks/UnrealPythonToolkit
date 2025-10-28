# 框架工具集合

本文件夹包含Unreal Engine Python开发的核心框架和处理器工具，为其他脚本提供基础设施支持。

## 📁 文件列表

- **`unreal_python_processor.py`** - Python代码综合处理器
- **`demo_processor_usage.py`** - 处理器使用演示
- **`remote_execution.py`** - 远程执行框架
- **`syntax_check.py`** - 语法检查工具
- **`README_UnrealPythonProcessor.md`** - 处理器详细文档

## 🎯 核心框架

### UnrealPythonProcessor (`unreal_python_processor.py`)

#### ✨ 功能特性
- **代码分析**: 深度分析Python代码结构和Unreal API使用
- **代码验证**: 检查语法错误、安全问题和最佳实践
- **性能优化**: 提供代码优化建议和重构方案
- **模板生成**: 自动生成常用代码模板
- **批量处理**: 支持目录级别的批量代码处理

#### 🔍 分析能力
- **导入分析**: 识别标准库、第三方库和本地导入
- **API使用**: 分析Unreal Engine API的使用模式
- **复杂度评估**: 计算代码复杂度和质量评分
- **安全检查**: 识别潜在的安全风险和问题

#### 🚀 使用方法
```python
# 基本分析
from unreal_python_processor import UnrealPythonProcessor
processor = UnrealPythonProcessor()
result = processor.analyze_code(python_code)

# 代码验证
validation = processor.validate_code(python_code)

# 批量处理
results = processor.process_directory("/path/to/scripts", "analyze")
```

### 远程执行框架 (`remote_execution.py`)

#### ✨ 功能特性
- **节点发现**: 自动发现网络中的Unreal Engine实例
- **远程命令**: 在远程UE实例中执行Python命令
- **多实例协调**: 支持多个UE实例间的协调工作
- **安全连接**: 基于TCP/UDP的安全通信协议

#### 🔧 应用场景
- **渲染农场**: 多台机器协同渲染
- **自动化测试**: 跨实例的自动化测试
- **批量处理**: 分布式资源处理
- **远程调试**: 远程诊断和调试

#### 🚀 使用方法
```python
# 启动远程执行会话
from remote_execution import RemoteExecution
remote_exec = RemoteExecution()
remote_exec.start()

# 连接到远程节点
remote_exec.open_command_connection(node_id)
remote_exec.run_command("your_python_command")
```

## 📊 工具矩阵

| 工具 | 主要功能 | 适用场景 | 复杂度 |
|------|----------|----------|--------|
| UnrealPythonProcessor | 代码分析和优化 | 开发阶段、代码审查 | ⭐⭐⭐⭐⭐ |
| RemoteExecution | 远程控制和协调 | 分布式工作、自动化 | ⭐⭐⭐⭐ |
| SyntaxCheck | 语法验证 | 开发调试、质量保证 | ⭐⭐⭐ |
| DemoUsage | 学习和演示 | 入门学习、参考 | ⭐⭐ |

## 🔧 开发工作流

### 1. 代码开发阶段
```python
# 使用语法检查
exec(open("framework/syntax_check.py").read())

# 使用代码分析优化
exec(open("framework/unreal_python_processor.py").read())
```

### 2. 代码质量保证
```python
# 批量验证代码质量
processor = UnrealPythonProcessor()
results = processor.process_directory(".", "validate")
```

### 3. 分布式执行
```python
# 设置远程执行环境
exec(open("framework/remote_execution.py").read())
```

## 📋 高级特性

### 代码模板生成
UnrealPythonProcessor支持多种代码模板：

- **ActorManager**: Actor操作管理模板
- **MaterialProcessor**: 材质处理模板
- **CameraSetup**: 相机设置模板
- **AssetBatchProcessor**: 资产批量处理模板
- **SceneAnalyzer**: 场景分析模板

### 性能优化
- **缓存机制**: 智能缓存分析结果
- **并行处理**: 支持多线程批量处理
- **内存优化**: 大文件处理的内存管理

### 安全特性
- **路径验证**: 防止路径遍历攻击
- **代码审计**: 识别潜在安全风险
- **权限检查**: 确保操作权限合法

## 🔌 扩展开发

### 自定义分析器
```python
class CustomAnalyzer(UnrealPythonProcessor):
    def custom_analysis(self, tree):
        # 自定义分析逻辑
        pass
```

### 自定义验证规则
```python
def custom_validation_rule(tree):
    # 自定义验证逻辑
    return {"issues": issues, "suggestions": suggestions}
```

## 📚 文档资源

- **详细文档**: `README_UnrealPythonProcessor.md`
- **使用示例**: `demo_processor_usage.py`
- **API参考**: 源码中的详细注释

## ⚠️ 系统要求

### 最低要求
- **Python**: 3.7+
- **Unreal Engine**: 4.27+ / 5.0+
- **内存**: 512MB+

### 推荐配置
- **Python**: 3.9+
- **Unreal Engine**: 5.1+
- **内存**: 2GB+
- **网络**: 千兆以太网（远程执行）

## 🐛 故障排除

### 常见问题
1. **导入错误**: 检查Python路径和环境
2. **权限问题**: 确保UE编辑器权限
3. **网络连接**: 检查防火墙和网络配置
4. **内存不足**: 优化批处理大小

### 调试技巧
- 启用详细日志输出
- 使用小文件测试
- 检查UE编辑器控制台
- 验证网络连通性

## 🚀 最佳实践

### 开发建议
1. **模块化设计**: 保持工具的独立性
2. **错误处理**: 添加完善的异常处理
3. **日志记录**: 使用结构化日志
4. **文档完善**: 维护详细的代码文档

### 性能优化
1. **批量处理**: 减少单次处理开销
2. **缓存结果**: 避免重复计算
3. **内存管理**: 及时释放不需要的对象
4. **异步操作**: 使用异步处理提高响应性

---

**这些框架工具为Unreal Python开发提供了强大的基础设施支持！** 🏗️