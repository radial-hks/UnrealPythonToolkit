import unreal
import math

# ------------ 配置区（按需修改） ------------
use_existing_actor = False
existing_actor_name = "DG3M_Camera_01"    # 若use_existing_actor=True，会尝试找到此名字的 actor
location_cm = unreal.Vector(0.0, 0.0, 0.0) # 若要创建新 actor，请替换为你的 cm 单位位置
pitch = 35.29101115172902
yaw   = 134.3707467663964
roll  = -151.25654334242077

focal_length_mm = 45.0
sensor_w_mm = 36.0
sensor_h_mm = 24.0

res_w = 6868
res_h = 4588
# --------------------------------------------

# Helper to degrees <-> radians
def rad2deg(r): return r * 180.0 / math.pi
def deg2rad(d): return d * math.pi / 180.0

# 1) Find or spawn a CineCameraActor
camera_actor = None
if use_existing_actor:
    all_actors = unreal.EditorLevelLibrary.get_all_level_actors()
    for a in all_actors:
        if a.get_name() == existing_actor_name:
            camera_actor = a
            break

if camera_actor is None:
    camera_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.CineCameraActor, location_cm)
    camera_actor.set_actor_label("DG3M_Camera_01")

# 2) Set rotation
camera_actor.set_actor_rotation(unreal.Rotator(pitch, yaw, roll), teleport_physics=False)

# 3) Get CineCameraComponent
cine = camera_actor.get_cine_camera_component()

# 4) Set Filmback and Focal Length
filmback = cine.get_editor_property("filmback")
filmback.sensor_width = sensor_w_mm
filmback.sensor_height = sensor_h_mm
cine.set_editor_property("filmback", filmback)
cine.set_editor_property("current_focal_length", focal_length_mm)

# 5) Ensure sensor fit is horizontal (so focal length & sensor width control horizontal FOV)
# CineCameraComponent has FilmbackSettings -> but "sensor fit" may be in LensSettings, so try both if present
try:
    lenssettings = cine.get_editor_property("lens_settings")
    # lenssettings does not always expose sensor fit; try to set filmback crop or offset if available
except Exception:
    pass

# 6) Compute theoretical FOVs
fov_h = 2.0 * math.atan(sensor_w_mm / (2.0 * focal_length_mm))  # radians
fov_v = 2.0 * math.atan(sensor_h_mm / (2.0 * focal_length_mm))
print("理论水平 FOV (deg):", rad2deg(fov_h))
print("理论垂直 FOV (deg):", rad2deg(fov_v))

# 7) Read actual FOV from component (if methods exist)
try:
    actual_h = cine.get_horizontal_field_of_view()
    actual_v = cine.get_vertical_field_of_view()
    print("CineCameraComponent 报告水平 FOV:", actual_h, "垂直 FOV:", actual_v)
except Exception:
    # Fallback: compute from CameraComponent.field_of_view (which is horizontal FOV)
    cc = camera_actor.get_component_by_class(unreal.CameraComponent)
    if cc:
        fov_from_cc = cc.get_editor_property("field_of_view")
        print("CameraComponent FieldOfView (deg):", fov_from_cc)

# 8) Debug: draw frustum lines from camera (visualization)
world = unreal.EditorLevelLibrary.get_editor_world()
rot = camera_actor.get_actor_rotation()
forward = unreal.MathLibrary.rotator_to_vector(rot)
right = unreal.MathLibrary.rotator_to_direction(rot, unreal.Vector(1,0,0)) if hasattr(unreal.MathLibrary, 'rotator_to_direction') else unreal.Vector(1,0,0)

start = camera_actor.get_actor_location()
# compute forward vector in cm
forward_vec = unreal.Vector(forward.x, forward.y, forward.z)
far = 20000.0 * 100.0  # 20km in cm (very long)
end = start + forward_vec * far
unreal.DrawDebugHelpers.draw_debug_line(world, start, end, unreal.LinearColor.GREEN, True, -1.0, 0, 10.0)

print("Camera setup complete. 请确保 Editor Viewport 输出分辨率设置为 {}x{} 并锁定相机视图以检验画面。".format(res_w, res_h))
