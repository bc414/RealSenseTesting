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

	cv2.namedWindow("Realsense", cv2.WINDOW_AUTOSIZE)

	pink_upper_bound=np.array([195, 255, 255])
	pink_lower_bound=np.array([155, 50, 150])
	hsv_image=cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)
	mask=cv2.inRange(hsv_image, pink_lower_bound, pink_upper_bound)
	ekernel=np.ones((3, 3), np.uint8)
	mask=cv2.erode(mask, ekernel, iterations=1)
	c, h=cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
	for con in c:
		cv2.drawContours(mask, [con], 0, 255, -1)
	res=cv2.bitwise_and(color_image, color_image, mask=mask)

	while True:
		cv2.imshow("Realsense", res)
		k=cv2.waitKey(1)
		if k==ord('q'):
			break
	
finally:
	pipeline.stop()


