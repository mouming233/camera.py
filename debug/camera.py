import cv2
import numpy as np
import socket
import struct
import threading



# 创建TCP/IP套接字
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#绑定(主机,端口号)到套接字
s.bind(('10.236.112.215', 8888))


#开始TCP监听
s.listen(1)

# 建立客户端连接,阻塞
# 等待客户端连接
print("等待客户端连接...")
conn, addr = s.accept()
print("已连接：", addr)


while True:
    # 接收TCP数据
    data=conn.recv(4)

    if not data:
        break

    img_size = struct.unpack('!i', data)[0]

    img_data=b''

    while len(img_data)<img_size:

        data=conn.recv(img_size-len(img_data))

        if not data:
            break

        img_data+=data


    img = cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_COLOR)

    cv2.imshow("img",img)

    cv2.waitKey(0)




conn.close()
s.close()
cv2.destroyAllWindows()

