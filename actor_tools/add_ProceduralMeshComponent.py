import unreal

# 1. 获取 SubobjectDataSubsystem 实例
subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)

# 2. 获取当前选中的所有 Actor
selected_actors = unreal.EditorLevelLibrary.get_selected_level_actors()

for actor in selected_actors:
    # 3. 获取 Actor 的根子对象数据句柄
    # 数组的第一个元素通常是根组件或 Actor 本身
    root_sub_object_handles = subsystem.k2_gather_subobject_data_for_instance(actor)
    if not root_sub_object_handles:
        unreal.log_error(f"无法获取 Actor {actor.get_name()} 的根组件句柄。")
        continue

    root_handle = root_sub_object_handles[0]

    # 4. 定义要添加的组件类
    pmc_class = unreal.ProceduralMeshComponent

    # 5. 配置添加新子对象的参数
    params = unreal.AddNewSubobjectParams(
        parent_handle=root_handle,
        new_class=pmc_class
        # new_name=unreal.Text("MyProceduralMesh") # 为新组件指定一个名称
    )

    # 6. 添加新组件
    new_sub_object_handle, fail_reason = subsystem.add_new_subobject(params)

    if new_sub_object_handle:
        unreal.log(f"成功为 Actor {actor.get_name()} 添加 ProceduralMeshComponent 组件。")
        # 可选: 获取组件实例并进行后续操作（例如生成网格体）
        # 从 Actor 获取所有 ProceduralMeshComponent 组件
        pmc_components = actor.get_components_by_class(unreal.ProceduralMeshComponent)
        if pmc_components:
            new_pmc = pmc_components[-1]  # 获取最后一个（新添加的）
            if new_pmc:
                # 修改组件名称【暂不考虑】
                # new_pmc.rename("CustomProceduralMesh")
                # unreal.log(f"组件名称已修改为: {new_pmc.get_name()}")
                # 在这里调用 create_mesh_section 等方法生成网格体
                pass
    else:
        unreal.log_error(f"为 Actor {actor.get_name()} 添加组件失败: {fail_reason}")

# 7. 确保编辑器更新显示（标记为已修改）
for actor in selected_actors:
    unreal.EditorAssetLibrary.save_loaded_asset(actor) # 这可能会根据你的具体需求（是在关卡中的实例还是蓝图资产）有所不同

