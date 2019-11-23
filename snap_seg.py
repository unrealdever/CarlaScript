import carla
import random
import time
from tqdm import tqdm

client = carla.Client('localhost', 2000)
client.set_timeout(2.0)

for mid, map_name in enumerate(client.get_available_maps()):
    world = client.load_world(map_name)
    blueprint_library = world.get_blueprint_library()
    print('load map', map_name)

    bp_rgb = blueprint_library.find('sensor.camera.rgb')
    bp_rgb.set_attribute('sensor_tick', '0.1')
    bp_rgb.set_attribute('image_size_x', '1024')
    bp_rgb.set_attribute('image_size_y', '1024')
    bp_seg = blueprint_library.find('sensor.camera.semantic_segmentation')
    bp_seg.set_attribute('sensor_tick', '0.1')
    bp_seg.set_attribute('image_size_x', '1024')
    bp_seg.set_attribute('image_size_y', '1024')
    cc_rgb = carla.ColorConverter.Raw
    cc_seg = carla.ColorConverter.CityScapesPalette
    actors = []

    for i, transform in tqdm(enumerate(world.get_map().get_spawn_points())):
        transform.location.z += 3.0
        transform.rotation.pitch = -45.0

        camera_rgb = world.spawn_actor(bp_rgb, transform)
        actors.append(camera_rgb)
        camera_rgb.listen(lambda image: image.save_to_disk('_out/%02d_%05d_rgb_%06d.png' % (mid, i, image.frame), cc_rgb))
        time.sleep(0.15)
        for actor in actors:
            actor.destroy()
        # 通过存取list的方式让destory方法可调用，直接调用可能报错
        actors = []

        camera_seg = world.spawn_actor(bp_seg, transform)
        actors.append(camera_seg)
        camera_seg.listen(lambda image: image.save_to_disk('_out/%02d_%05d_seg_%06d.png' % (mid, i, image.frame), cc_seg))
        time.sleep(0.15)
        for actor in actors:
            actor.destroy()
        actors = []
    
    time.sleep(1)
    print('all %d point done.' % len(world.get_map().get_spawn_points()))