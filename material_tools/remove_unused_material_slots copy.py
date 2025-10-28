import unreal

def get_used_material_indices(static_mesh):
    """
    尝试获取StaticMesh中实际被几何体使用的材质槽索引
    由于GeometryScript_StaticMeshFunctions在Python中不可用，使用替代方案
    """
    try:
        # 尝试使用GeometryScript方法（如果可用）
        if hasattr(unreal, 'GeometryScript_StaticMeshFunctions'):
            # 设置LOD选项（默认LOD 0）
            requested_lod = unreal.GeometryScriptMeshReadLOD()
            requested_lod.lod_index = 0
            
            # 获取Section材质列表和对应的材质索引
            material_list, material_indices, slot_names = unreal.GeometryScript_StaticMeshFunctions.get_section_material_list_from_static_mesh(
                static_mesh, requested_lod
            )
            
            if material_indices:
                # material_indices数组中的每个值就是对应Section使用的材质槽索引
                used_indices = set()
                for material_slot_index in material_indices:
                    if material_slot_index >= 0:  # 有效的材质槽索引
                        used_indices.add(material_slot_index)
                
                unreal.log(f"  📊 检测到使用的材质槽索引: {sorted(used_indices)}")
                return used_indices
        
        # 如果GeometryScript不可用，使用基于StaticMesh渲染数据的方法
        unreal.log(f"  ℹ️ GeometryScript不可用，使用渲染数据分析方法")
        return get_used_material_indices_from_render_data(static_mesh)
            
    except Exception as e:
        unreal.log_error(f"  ❌ 获取材质使用信息时出错: {str(e)}")
        return None

def get_used_material_indices_from_render_data(static_mesh):
    """
    通过分析StaticMesh的LOD section来获取真正被几何体使用的材质索引
    这个方法会检查每个section实际使用的材质槽，而不是简单检查材质槽是否为空
    """
    try:
        # 获取StaticMeshEditorSubsystem实例
        static_mesh_editor_subsystem = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
        
        # 使用StaticMeshEditorSubsystem获取材质数量
        num_materials = static_mesh_editor_subsystem.get_number_materials(static_mesh)
        
        if num_materials == 0:
            unreal.log_warning(f"  ⚠️ StaticMesh没有材质槽")
            return set()
        
        # 获取LOD 0的section数量
        lod_index = 0
        try:
            # 使用StaticMesh的get_num_sections方法获取section数量
            num_sections = static_mesh.get_num_sections(lod_index)
            unreal.log(f"  📐 LOD {lod_index} 有 {num_sections} 个sections")
        except Exception as e:
            unreal.log_error(f"  ❌ 无法获取section数量: {str(e)}")
            # 回退到简单的材质槽检查
            return get_used_material_indices_simple(static_mesh, static_mesh_editor_subsystem, num_materials)
        
        # 分析每个section使用的材质槽
        used_indices = set()
        for section_index in range(num_sections):
            try:
                # 获取这个section使用的材质槽索引
                material_slot_index = static_mesh_editor_subsystem.get_lod_material_slot(static_mesh, lod_index, section_index)
                
                if material_slot_index >= 0 and material_slot_index < num_materials:
                    used_indices.add(material_slot_index)
                    material = static_mesh.get_material(material_slot_index)
                    material_name = material.get_name() if material else "None"
                    unreal.log(f"    🔗 Section {section_index} -> 材质槽 {material_slot_index}: {material_name}")
                else:
                    unreal.log_warning(f"    ⚠️ Section {section_index} 使用无效的材质槽索引: {material_slot_index}")
                    
            except Exception as e:
                unreal.log_error(f"    ❌ 分析Section {section_index}时出错: {str(e)}")
                continue
        
        if used_indices:
            unreal.log(f"  📊 真正被几何体使用的材质槽索引: {sorted(used_indices)}")
            return used_indices
        else:
            unreal.log_warning(f"  ⚠️ 没有找到被使用的材质槽")
            # 回退到简单检查
            return get_used_material_indices_simple(static_mesh, static_mesh_editor_subsystem, num_materials)
            
    except Exception as e:
        unreal.log_error(f"  ❌ 分析section材质映射时出错: {str(e)}")
        return None

def get_used_material_indices_simple(static_mesh, static_mesh_editor_subsystem, num_materials):
    """
    简单的材质槽检查方法（回退方案）
    只检查材质槽是否有材质，不分析section映射
    """
    used_indices = set()
    unreal.log(f"  🔄 回退到简单材质槽检查模式")
    
    for i in range(num_materials):
        material = static_mesh.get_material(i)
        if material is not None:
            used_indices.add(i)
            unreal.log(f"    📌 材质槽 {i}: {material.get_name()}")
        else:
            unreal.log(f"    ⚪ 材质槽 {i}: 空")
    
    return used_indices

def remove_unused_material_slots(selected_only=True):
    """
    清理 StaticMesh 中未被几何体实际使用的材质槽（兼容 UE5）
    """
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    editor_asset_lib = unreal.EditorAssetLibrary()

    # 获取资产列表
    if selected_only:
        assets = unreal.EditorUtilityLibrary.get_selected_assets()
    else:
        assets = [a.get_asset() for a in asset_registry.get_assets_by_class('StaticMesh')]

    if not assets:
        unreal.log_warning("⚠️ 未找到要处理的 StaticMesh。")
        return

    for mesh in assets:
        if not isinstance(mesh, unreal.StaticMesh):
            continue

        unreal.log(f"🧹 正在处理: {mesh.get_name()}")

        # 获取当前材质槽
        all_materials = mesh.get_editor_property("static_materials")
        
        if not all_materials:
            unreal.log(f"  ✅ 跳过: {mesh.get_name()} (没有材质槽)")
            continue
        
        # 获取实际被使用的材质索引
        used_indices = get_used_material_indices(mesh)
        
        if used_indices is None:
            # 如果无法获取使用信息，回退到原来的逻辑（只删除空槽）
            unreal.log(f"  ⚠️ 回退到简单模式：只删除空材质槽")
            new_materials = []
            removed_count = 0
            
            for i, mat_slot in enumerate(all_materials):
                if mat_slot.material_interface is not None:
                    new_materials.append(mat_slot)
                else:
                    unreal.log(f"    ✂️ 删除空材质槽 {i}: {mat_slot.material_slot_name}")
                    removed_count += 1
        else:
            # 使用几何体分析结果来删除未使用的材质槽
            new_materials = []
            removed_count = 0
            
            for i, mat_slot in enumerate(all_materials):
                if i in used_indices:
                    # 这个材质槽被几何体实际使用
                    new_materials.append(mat_slot)
                else:
                    # 这个材质槽没有被使用，删除它
                    material_name = mat_slot.material_interface.get_name() if mat_slot.material_interface else "None"
                    unreal.log(f"    ✂️ 删除未使用的材质槽 {i}: {mat_slot.material_slot_name} (材质: {material_name})")
                    removed_count += 1

        # 更新材质槽
        if removed_count > 0:
            mesh.set_editor_property("static_materials", new_materials)
            mesh.modify()
            mesh.mark_package_dirty()
            editor_asset_lib.save_loaded_asset(mesh)
            unreal.log(f"✅ 完成: {mesh.get_name()} (移除 {removed_count} 个未使用材质槽，保留 {len(new_materials)} 个)")
        else:
            unreal.log(f"✅ 无需修改: {mesh.get_name()} (所有材质槽都在使用中)")

    unreal.log("🎯 所有 StaticMesh 清理完成。")

# 执行
remove_unused_material_slots(selected_only=True)
