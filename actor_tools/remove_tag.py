import unreal

# 获取编辑器世界
editor_world = unreal.EditorLevelLibrary.get_editor_world()

# 获取所有具有特定 Tag 的 Actor
tag_to_find = "BT"  # 替换为你要查找的 Tag
actors_with_tag = unreal.GameplayStatics.get_all_actors_with_tag(editor_world,tag_to_find)


rm_tag = "BXS"

def get_info(actor):
    for i in actor.tags:
        if("EID=" in str(i)):
            eid = str(i).replace("EID=","")
        if("XXY" in str(i)):
            type = str(i)
    return eid,type


for actor in actors_with_tag:
    # if rm_tag in actor.tags:
        # 检查 Actor 是否是静态网格物体
    if isinstance(actor, unreal.StaticMeshActor):
        static_mesh_actor = unreal.StaticMeshActor.cast(actor)
        static_mesh_component = static_mesh_actor.static_mesh_component
        materials = static_mesh_component.get_materials()
        if "MI_" not in str(materials[0].get_name()):
            actor.tags.append(rm_tag)
        print(actor.get_actor_label(),str(materials[0].get_name()))
            # 输出材质名称
        # print(actor)
        # materials = static_mesh_component.get_materials()
        # actor.tags.remove(rm_tag)
        # # print(get_info(actor))
        # print(str(actor.tags[0]))
        # print(actor.get_actor_label())