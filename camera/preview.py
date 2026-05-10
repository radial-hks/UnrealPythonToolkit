from PIL import Image
import matplotlib.pyplot as plt

# 定义要预览的 PNG 文件路径
image_path = "D:/UE5_Project/XXX_SJ000000/Blueprint/VehicleTools/Assets/Meshes/Textures/CLS_Dif_dark_blue_1.PNG"

# 使用 Pillow 打开图像
image = Image.open(image_path)

# 使用 matplotlib 显示图像
plt.imshow(image)
plt.axis('off')  # 不显示坐标轴
plt.show()