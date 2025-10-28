# https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/EditorLevelLibrary?application_version=5.5#unreal.EditorLevelLibrary.clear_actor_selection_set

import unreal

def get_actor_folder_name(actor):
    # 获取 Actor 的路径
    # actor_path = actor.get_path_name()
    actor_path = actor.get_folder_path()
    # 分割路径以获取文件夹名称
    path_parts = str(actor_path).split('/')
    
    # 如果路径中包含文件夹，返回文件夹名称
    if len(path_parts) > 0:
        return path_parts  # 倒数第二部分是文件夹名称
    else:
        return None  # 如果没有文件夹，返回 None

def main():
    # 获取编辑器世界
    editor_world = unreal.EditorLevelLibrary.get_editor_world()
    
    # 获取世界中的所有 Actor
    all_actors = unreal.EditorLevelLibrary.get_all_level_actors()
    
    # 遍历所有 Actor 并打印其文件夹名称
    for actor in all_actors:
        # 获取 Actor 的文件夹名称
        folder_name = get_actor_folder_name(actor)
        if folder_name:
            print(f"Actor: {actor.get_name()} is in folder: {folder_name}")
        else:
            print(f"Actor: {actor.get_name()} is not in any folder")

if __name__ == "__main__":
    main()