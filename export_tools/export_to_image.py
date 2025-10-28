import unreal

# 定义要导出的纹理路径
texture_path = "/Game/MyStaticTexture/RT_Capture.RT_Capture"

# 加载纹理资产
texture = unreal.load_asset(texture_path)

# 检查纹理是否加载成功
if texture is None:
    raise ValueError(f"无法加载纹理: {texture_path}")

# 定义导出路径
# export_path = "D:/UE5_Project/XXX_SJ000000/Blueprint/VehicleTools/Assets/Meshes/Textures/CLS_Dif_dark_blue_2.png"

export_path =  r"C:\\Users\\wanglinfeng\\Documents\\CodeSpace\\Unreal\\" + "111" + ".hdr"

# 确保导出目录存在
import os
os.makedirs(os.path.dirname(export_path), exist_ok=True)

# 获取世界上下文对象
world_context_object = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_world()

# 从导出路径中提取文件路径和文件名
file_path = os.path.dirname(export_path)
file_name = os.path.basename(export_path)


# 使用 Texture2D 的导出功能
# unreal.RenderingLibrary.export_texture2d(world_context_object, texture, file_path, file_name)
# unreal.RenderingLibrary.export_render_target(world_context_object, texture, file_path, file_name)


a = unreal.RenderingLibrary.read_render_target_raw(world_context_object, texture, normalize=True)
print(a)

print(f"纹理已成功导出到: {export_path}")

