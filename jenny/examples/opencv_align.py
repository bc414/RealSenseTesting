import pyrealsense2 as rs
import numpy as np
import cv2

pipeline=rs.pipeline()
config=rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
profile=pipeline.start(config)

depth_sensor=profile.get_device().first_depth_sensor()
depth_scale=depth_sensor.get_depth_scale()
print("depth scale: {0}".format(depth_scale))

align_to=rs.stream.color
align=rs.align(align_to)

def click_point(event, x, y, flags, params):
	if event==cv2.EVENT_LBUTTONUP:
		params[1].append((x, y))
		color=(int(params[0][y, x, 0]), int(params[0][y, x, 1]), int(params[0][y, x, 2]))
		print(color)
		cv2.circle(params[0], (x, y), 5, color, -1)

try:
	for i in range(0, 10):
		frames=pipeline.wait_for_frames()
		aligned_frames=align.process(frames)
		depth_frame=aligned_frames.get_depth_frame()
		color_frame=aligned_frames.get_color_frame()
		if not depth_frame or not color_frame:
			continue
	depth_image=np.asanyarray(depth_frame.get_data())
	color_image=np.asanyarray(color_frame.get_data())
	
	depth_colormap=cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

	images=np.hstack((color_image, depth_colormap))
	params=[color_image, []]
	cv2.namedWindow("Realsense", cv2.WINDOW_AUTOSIZE)
	cv2.setMouseCallback("Realsense", click_point, params)
	while True:
		cv2.imshow("Realsense", color_image)
		k=cv2.waitKey(1)
		if k==ord('q'):
			break
	colorImage=np.zeros((100, 0, 3), dtype=np.uint8)
	for p in params[1]:
		hsv_value=cv2.cvtColor(np.uint8([[color_image[p]]]), cv2.COLOR_BGR2HSV).squeeze()
		print(hsv_value[0], hsv_value[1], hsv_value[2])
		subimage=np.stack((np.ones((100, 20), dtype=np.uint8)*hsv_value[0], np.ones((100, 20), dtype=np.uint8)*hsv_value[1], np.ones((100, 20), dtype=np.uint8)*hsv_value[2]), axis=2)
		colorImage=np.hstack((colorImage, subimage))
	bgrImage=cv2.cvtColor(colorImage, cv2.COLOR_HSV2BGR)
	cv2.namedWindow("colors", cv2.WINDOW_AUTOSIZE)
	cv2.imshow("colors", bgrImage)
	cv2.waitKey()
	

finally:
	pipeline.stop()


