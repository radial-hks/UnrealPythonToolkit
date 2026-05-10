import unreal
import csv

# 获取当前选中的Actor
# selected_actors = unreal.EditorLevelLibrary.get_selected_level_actors()
selected_actors = unreal.EditorLevelLibrary.get_all_level_actors()

# 准备CSV文件
csv_file_path = "C:/Users/wanglinfeng/Documents/CodeSpace/Unreal/actor_info_2.csv"

# 打开CSV文件并写入数据
with open(csv_file_path, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    # 写入CSV文件的表头
    csv_writer.writerow(['EID',"type",'Actor_Path'])

    # 遍历选中的Actor
    for actor in selected_actors:
        actor_name = actor.get_actor_label()
        # print(actor_name)
        tags = actor.tags

        # 查找以"EID="开头的Tag
        eid_tag = None
        for tag in tags:
            # print(type(tag),str(tag))
            str_tag = str(tag)
            if "EID=" in str_tag:
                eid_tag = str_tag.replace("EID=","")
                break
            # if tag.startswith("EID="):
            #     eid_tag = tag
            #     break
        # 获取路径
        
        folder_Path = actor.get_folder_path()

        name_list = str(folder_Path).split("/")
        # print(name_list)
        # print(name_list[0])
        # print(name_list[1])
        # print(name_list[2])
        # print(name_list[3])

        # 写入Actor名称和EID Tag到CSV文件
        csv_writer.writerow([eid_tag,name_list[0],str(folder_Path)+"\\"+str(actor_name)])

print(f"Actor信息已保存到 {csv_file_path}")