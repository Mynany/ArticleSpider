from zheye import zheye
z = zheye()
positions = z.Recognize('image/zhihu_image/c.gif')
last_postion = []
if len(positions) == 2:
    if positions[0][1] > positions[1][1]:
        last_postion.append([positions[1][1], positions[1][0]])
        last_postion.append([positions[0][1], positions[0][0]])
    else:
        last_postion.append([positions[0][1], positions[0][0]])
        last_postion.append([positions[1][1], positions[1][0]])
else:
    last_postion.append([positions[0][1], positions[0][0]])
print(last_postion)
