# coding:utf-8
import os


class BatchRename(object):

    def rename(self):
        # windows环境
        """
            os.rename() 方法用于命名文件或目录，从 src 到 dst,如果dst是一个存在的目录, 将抛出OSError。
            语法:rename()方法语法格式如下：
            os.rename(src, dst)
            参数
                src -- 要修改的目录名
                dst -- 修改后的目录名

          :return:
          """
        path = r"D:\myproject\EricWeb\bluelog\static\img\avatar"
        file_list = os.listdir(path)
        total_num = len(file_list)
        i = 1
        for item in file_list:
            src = os.path.join(os.path.abspath(path), item)
            dst = os.path.join(os.path.abspath(path), '' + str(i) + '.jpg')  # 可根据自己需求选择格式
            # dst=os.path.join(os.path.abspath(path),'00000'+format(str(i))+'.jpg') #可根据自己需求选择格式,自定义图片名字
            try:
                os.rename(src, dst)  # src:原名称  dst新名称d
                i += 1
            except:
                continue
        print('total %d to rename & converted %d png' % (total_num, i))


if __name__ == '__main__':
    demo = BatchRename()
    demo.rename()
