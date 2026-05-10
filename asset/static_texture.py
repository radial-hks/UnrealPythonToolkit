import unreal
import os

# # 1. 创建 Render Target
# render_target_name = "MyRenderTarget"
# render_target_path = "/Game/MyRenderTarget"
# render_target = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
#     asset_name=render_target_name,
#     package_path=render_target_path,
#     asset_class=unreal.TextureRenderTarget2D,
#     factory=unreal.TextureRenderTarget2DFactoryNew()
# )

# # 设置 Render Target 的分辨率
# render_target.set_editor_property("size_x", 1024)
# render_target.set_editor_property("size_y", 1024)
# render_target.set_editor_property("clear_color", unreal.LinearColor(0, 0, 0, 1))  # 设置背景颜色

# 2. 渲染到 Render Target
# 假设你有一个场景或内容需要渲染到 Render Target
# 这里可以使用蓝图或 C++ 逻辑来渲染内容到 Render Target
# 例如，使用 Draw Material to Render Target 节点


#https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/RenderingLibrary?application_version=5.5#unreal.RenderingLibrary.export_texture2d

# 定义要导出的纹理路径
texture_path = '/Game/MyStaticTexture/RT_Capture.RT_Capture'
# texture_path = "/Game/XXX_SJ000000/Blueprint/VehicleTools/Assets/Meshes/Textures/RT_Capture.RT_Capture"

# 加载纹理资产
RT = unreal.load_asset(texture_path)


# 3. 导出 Render Target 为静态贴图
texture_name = "T_Capture_4"
texture_path = "/Game/MyStaticTexture/"
texture = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
    asset_name=texture_name,
    package_path=texture_path,
    asset_class=unreal.Texture2D,
    factory=unreal.Texture2DFactoryNew()
)


texture_path_new = texture.get_path_name()

# 获取世界上下文对象
world_context_object = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_world()


# 将 Render Target 的内容复制到静态贴图
unreal.RenderingLibrary.convert_render_target_to_texture2d_editor_only(world_context_object,RT,texture)

# 保存静态贴图
unreal.EditorAssetLibrary.save_asset(texture_path_new)

print(f"静态贴图已创建并保存到: {texture_path}")

# 定义导出路径
export_path = r"C:\\Users\\wanglinfeng\\Documents\\CodeSpace\\Unreal\\" + texture_name + ".hdr"
# 从导出路径中提取文件路径和文件名
file_path = os.path.dirname(export_path)
file_name = os.path.basename(export_path)

# 使用 Texture2D 的导出功能
unreal.RenderingLibrary.export_texture2d(world_context_object, texture, file_path, file_name)
# unreal.RenderingLibrary.export_render_target(world_context_object, texture, file_path, file_name)

print(f"纹理已成功导出到: {export_path}")


# 检查资源是否存在
if unreal.EditorAssetLibrary.does_asset_exist(texture_path_new):
    # 删除资源
    unreal.EditorAssetLibrary.delete_asset(texture_path_new)
    print(f"资源已删除: {texture_path_new}")
else:
    print(f"资源不存在: {texture_path_new}")
