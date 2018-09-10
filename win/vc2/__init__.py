import itchat
import os
import time
import cv2

sendMsg = u"{消息精灵} 主人不在"
useMsg = u"使用方法: \n1.运行CMD命令: cmd xxx \n"\
            u"-例如: \n  cmd shutdown -s -t 0 \n"\
            u"2.获取当前电脑用户:cap \n  3.启用消息精灵(默认关闭) : ast \n"\
            u"4.关闭消息精灵: astc "

flag = 0; #消息精灵开关
nowTime = time.localtime();
filename = str(nowTime.tm_mon)+'-'+str(nowTime.tm_mday)+'_'+str(nowTime.tm_hour)+'-'+str(nowTime.tm_min)+'-'+str(nowTime.tm_sec)+".txt";
myfile = open(filename,'w'); #重写文件,没有则创建

@itchat.msg_register('Text')
def text_reply(msg):
    global flag   #全局作用
    message = msg['Text']
    fromName = msg['FromUserName']
    toName = msg['ToUserName']
    print("fromName" + fromName);
    print("toName" + toName);

    if toName == "filehelper":
        if message == "cap":
            cap = cv2.VideoCapture(0)
            ret , img = cap.read()
            cv2.imwrite("weixinTemp.jpg",img)
            itchat.send('@img@%s' %u'weixinTemp.jpg','filehelper')
            cap.release()
        if message.startswith('cmd'):
            #os.system(message.strip(message[0:4]))
            info = os.popen(message.strip(message[0:3]))
            result = info.read();
            info.close()
            itchat.send(result,'filehelper')
        if message == "ast":
            flag = 1
            itchat.send("消息精灵已启动","filehelper")
        if(message == "astc"):
            flag = 0
            itchat.send("消息精灵已关闭","filehelper")
    elif flag == 1:
        itchat.send(sendMsg,fromName)
        myfile.write(message)
        myfile.write("/n")
        myfile.flush()

if __name__ == '__main__':
    itchat.auto_login(hotReload=True)#enableCmdQR=-1
    itchat.send(useMsg,"filehelper")
    itchat.run()