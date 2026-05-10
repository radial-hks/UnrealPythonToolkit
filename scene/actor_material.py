import unreal

# 获取编辑器世界
editor_world = unreal.EditorLevelLibrary.get_editor_world()

# 获取所有具有特定 Tag 的 Actor
tag_to_find = "Layer=terrain"  # 替换为你要查找的 Tag
# actors_with_tag = unreal.GameplayStatics.get_all_actors_with_tag(editor_world,tag_to_find)


actors_with_tag = unreal.EditorLevelLibrary.get_selected_level_actors()


def get_info(actor):
    for i in actor.tags:
        if("EID=" in str(i)):
            eid = str(i).replace("EID=","")
        if("XXY" in str(i)):
            type = str(i)
    return eid,type

# 遍历所有找到的 Actor
for actor in actors_with_tag:
    # 检查 Actor 是否是静态网格物体
    if isinstance(actor, unreal.StaticMeshActor):
        static_mesh_actor = unreal.StaticMeshActor.cast(actor)
        static_mesh_component = static_mesh_actor.static_mesh_component
        eid,type = get_info(actor)
        # print eid,
        # 获取材质
        materials = static_mesh_component.get_materials()
        # 输出材质名称
        for material in materials:
            if material:
                # print(f"Actor: {actor.get_name()}, Material: {material.get_name()}")
                # print(f"Actor: {actor.get_name()}, Material: {material.get_name()}")
                color = str(material.get_name()).replace("M_","#")
            else:
                # print(f"Actor: {actor.get_name()}, Material: None")
                pass
        print(f"{actor.get_name()},{eid},{type},{color}")
        # print(f"{eid},{type},{color}")