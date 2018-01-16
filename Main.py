from PIL import Image
from ClearImg import ReadImage
from ImgToString import ImgTostring
import os,requests,time
class TheMain:
    img_src = "http://59.69.173.117/jwweb/sys/ValidateCode.aspx"
    img_save_path = "split_img\\"
    train_path = "train\\"
    model_data = "data\\model.txt"
    split_list = []
    img_name_list = []
    file_name_list = []
    def __init__(self):
        self.Tostring_obj = ImgTostring()
        self.CImg_obj = ReadImage()

    def split_img(self):
        self.file_name_list =  os.listdir(self.img_save_path)
        for file in self.file_name_list:
            split_img_list = []
            self.CImg_obj.set_img(Image.open(self.img_save_path + file))
            self.CImg_obj.main_remove_novce()
            x_min, x_max, y_min, y_max = 0, 0, 0, 0
            b_left = True
            for index in range(4):
                x_min, x_max, y_min, y_max,b_left = self.CImg_obj.edge_check(x_max + 1,b_left=b_left)
                split_img_list.append(self.CImg_obj.img.crop((x_min, y_min, x_max, y_max)).
                                           resize((self.CImg_obj.resize_x,self.CImg_obj.resize_y)))
            self.split_list.append(split_img_list.copy())
        return self
            
    def manual_check(self):
        """
        手动识别
        :return:
        """
        for img_list in self.split_list:
            for img in img_list:
                img.show()
                result = input()
                if result is "":
                    return
                img.save(self.train_path + result + "\\" + str(time.time()) + ".jpg")
        return self
        
    def auto_check(self):
        
        for img_list in self.split_list:
            the_name = ""
            for img in img_list:
                feature_list = self.CImg_obj.set_feature(img)
                result = self.Tostring_obj.load_model().predict([feature_list])#读取固定模型,惊醒预测
                result = chr(result) if result > 9 else str(result[0])
                the_name+=result
            self.img_name_list.append(the_name)
        return self
        
    def img_rename(self):
        for index,val in enumerate(self.file_name_list):
            os.rename(self.img_save_path + val, self.img_save_path + self.img_name_list[index] + '.jpg')
        return self
        
    def save_img(self):
        result = requests.get(self.img_src)
        with open(self.img_save_path  + str(time.time()) + '.jpg','ab+') as file:
            file.write(result.content)
        return self
    def all_img_to_feature(self,src = None):
        """
        把素材转化为特征文件
        :param src: 传过来一个地址
        :return: 无返回值
        """
        if src is None:src = self.train_path
        for dir in os.listdir(src):
            for file_name in os.listdir(src + dir):
                label = dir if dir.isdigit() else str(ord(dir))
                self.CImg_obj.set_img(Image.open(src + dir + "\\"+file_name))
                with open(self.model_data,'a+') as file:
                    file.write(self.CImg_obj.get_feature_str(label))
                self.CImg_obj.img.close()
                os.remove(src + str(dir) + "\\"+file_name)
        return self
if __name__=="__main__":
    
    the_main = TheMain()
    # for i in range(1):
    #     the_main.save_img()
        
    the_main.split_img().auto_check().img_rename()
    
    # the_main.all_img_to_feature()
    pass
