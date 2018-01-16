import pytesseract,time
class ReadImage(object):

    threshold = 230
    radius = 1
    resize_x = 22
    resize_y = 22
    one_size = 30
    edge_list_x = []
    edge_list_y = []
    edge_list_xy = []
    def __init__(self, img = None):
        if img is not None: self.img = img
        
    def set_radius(self,radius):
        self.radius = radius
    
    def set_img(self,img):
        self.img = img
        return self

    def get_bin_table(self):
        
        table  =  []
        for  i  in  range( 256 ):
            if  i  <  self.threshold:
                table.append(0)
            else:
                table.append(255)
        return table#获得二值化 数组 用于初始化 黑白图

    def left_zone(self,img, x, y, r = 1):
        # sum = img.getpixel((x + r, y)) + \
        #       img.getpixel((x + r, y + r)) + \
        #       img.getpixel((x + r, y - r)) + \
        #       img.getpixel((x, y + r)) + \
        #       img.getpixel((x, y - r))

        code_sum = 0
        for i in range(0, r + 1):
            for j in range(-r, r + 1):
                code_sum += img.getpixel((x + i, y + j))
        
        if code_sum >= ((255 * (r*2+1) * (r*2+1)) * 0.6):#60%以上都是白色的区域，则此块为白色
            return 255
        else:
            return 0#左边界

    def right_zone(self,img, x, y, r = 1):
        # sum = img.getpixel((x - r, y)) + \
        #       img.getpixel((x - r, y + r)) + \
        #       img.getpixel((x - r, y - r)) + \
        #       img.getpixel((x, y + r)) + \
        #       img.getpixel((x, y - r))

        code_sum = 0
        for i in range(-r, 0):
            for j in range(-r, r + 1):
                code_sum += img.getpixel((x + i, y + j))
        
        if code_sum >= ((255 *(r*2+1)*(r*2+1)) * 0.6):
            return 255
        else:
            return 0#右边界

    def up_zone(self,img, x, y, r = 1):
        # sum = img.getpixel((x - r, y)) + \
        #       img.getpixel((x + r, y)) + \
        #       img.getpixel((x - r, y + r)) + \
        #       img.getpixel((x, y + r)) + \
        #       img.getpixel((x + r, y + r))
        
        code_sum = 0
        for i in range(-r, r + 1):
            for j in range(0, r + 1):
                code_sum += img.getpixel((x + i, y + j))
                
        if code_sum >= ((255 *(r*2+1)*(r*2+1)) * 0.6):
            return 255
        else:
            return 0#上方边界

    def down_zone(self,img, x, y, r = 1):#下方边界
        # sum = img.getpixel((x - r, y)) + \
        #       img.getpixel((x + r, y)) + \
        #       img.getpixel((x - r, y - r)) + \
        #       img.getpixel((x, y - r)) + \
        #       img.getpixel((x + r, y - r))
        code_sum = 0
        for i in range(-r,r + 1):
            for j in range(-r, 0):
                code_sum += img.getpixel((x + i, y + j))
        if code_sum >= ((255 *(r*2+1)*(r*2+1)) * 0.6):
            return 255
        else:
            return 0

    def min_zone(self,img, x, y, r = 1):
        
        # sum = img.getpixel((x - r, y + r)) + \
        #       img.getpixel((x - r, y)) + \
        #       img.getpixel((x - r, y - r)) + \
        #       img.getpixel((x, y + r)) + \
        #       img.getpixel((x, y - r)) + \
        #       img.getpixel((x + r, y + r)) + \
        #       img.getpixel((x + r, y)) + \
        #       img.getpixel((x + r, y - r))
        code_sum = 0
        for i in range(-r,r + 1):
            for j in range(-r, r + 1):
                code_sum += img.getpixel((x + i, y + j))
        if code_sum >= ((255 *(r*2+1)*(r*2+1)) * 0.6):
            return 255
        else:
            return 0#中间区域

    def remove_noise(self,img, x, y, r = 1):
        cur_pixel = img.getpixel((x, y))
        width = img.width - r
        height = img.height - r
        min_x,min_y = r - 1 ,r - 1
        if x < r or y < r or x > width or y > height:
            return 255
        if cur_pixel == 255:
            return 255
        else:
            if x <= min_x:
                if y <= min_y or y >= height:#z左上的下场，都是白色
                    return 255
                else:
                    return self.left_zone(img, x, y, r)
            if x >= width:#右
                if y <= min_y or y >= height:
                    return 255
                else:
                    return self.right_zone(img, x, y, r)
            if y  <= min_y:#上
                if x <= min_x or x >= width:
                    return 255
                else:
                    return self.up_zone(img, x, y, r)
            if y >= height:#下
                if x <= min_x or x >= width:
                    return 255
                else:
                    return self.down_zone(img, x, y, r)

            return self.min_zone(img, x, y, r)#移除噪点

    def list_set_img(self,list_img, img = None):
        if img is None: img = self.img
        w, h = img.size
        i = 0
        for x in range(w):
            for y in range(h):
                if list_img[i] == None:
                    list_img[i] = 0
                img.putpixel((x, y), list_img[i])
                i = i + 1
        self.img = img
        return self

    def clear_img(self,img = None):
        if img is None: img = self.img
        w,h = img.size
        list_img = []
        for x in range(w):
            for y in range(h):
                list_img.append(self.remove_noise(img, x, y, self.radius))
        return list_img

    def read_img(self,img_):
        # img_ = img_.resize((120,60),Image.ANTIALIAS)
        # return img_
        code = pytesseract.image_to_string(img_,config = "/usr/share/tesseract-ocr/tessdata/configs/digits")
        return code

    def erase_border(self,img = None):
        if img is None:img = self.img
        w, h = img.size
        box = (1,1,w-1,h-1)
        self.img = img.crop(box)
        return self
        pass

    def to_black(self,img = None):
        if img is None: img = self.img
        img = img.convert('L')
        table = self.get_bin_table()
        self.img = img.point(table, '1')
        
        return self
    
    def show(self):
        self.img.show()

    def no_novce(self):
        '''
        移除噪点
        '''
        self.to_black()
        list_img = self.clear_img()
        self.list_set_img(list_img)
        return self
    
    def main_remove_novce(self):
        self.no_novce()
        self.erase_border()
        self.radius = 2
        self.no_novce()
        self.radius = 1
        # self.show()
        return self
    
    def get_code(self):
        '''
        外部获取验证码
        '''
        return pytesseract.image_to_string(self.img,config="-l chi_sim -psm 7").replace(' ', '')
        # return self.return_code()

    # def getCode(self):

                
    def edge_find(self,x,y,z,img = None,b_left = True):
        if img is None:img = self.img
        w, h = self.img.size
        the_pix = img.getpixel((x,y))
        if the_pix == 0:
            #左，上，右，下
            if x not in self.edge_list_x:
                self.edge_list_x.append(x)
            if y not in self.edge_list_y:
                self.edge_list_y.append(y)
            if (x,y) not in self.edge_list_xy:
                self.edge_list_xy.append((x,y))
            if x>0 and z is not  0 and (x-1,y) not in self.edge_list_xy and b_left:
                self.edge_find(x-1,y,z=2,b_left = b_left)
            if y>0 and z is not 1 and (x,y-1) not in self.edge_list_xy:
                self.edge_find(x,y-1,z=3,b_left = b_left)
            if x<w and z is not 2 and (x+1,y) not in self.edge_list_xy:
                self.edge_find(x+1,y,z=0,b_left = b_left)
            if y<h and z is not 3 and (x,y+1) not in self.edge_list_xy:
                self.edge_find(x,y+1,z=1,b_left = b_left)
        return
    def edge_check(self,x_min = None,b_left = True):
        w, h = self.img.size
        # b_left = True
        if x_min is None:
            x_min = 0
        for x in range(x_min,w):
            for y in range(h):
                if self.img.getpixel((x,y)) == 0:
                    self.edge_find(x , y, -1,b_left=b_left)
                    x_min = min(self.edge_list_x)
                    x_max = max(self.edge_list_x)
                    y_min = min(self.edge_list_y)
                    y_max = max(self.edge_list_y)
                    self.edge_list_x = []
                    self.edge_list_y = []
                    self.edge_list_xy = []
                    if x_max - x_min >= self.one_size:
                        x_max = x_min + self.one_size
                        b_left = False
                    else:
                        b_left = True
                    return x_min,x_max,y_min,y_max,b_left
                
                
    def split_save(self,index = 4):
        x_min, x_max, y_min, y_max = 0, 0, 0, 0
        for i in range(index):
            x_min, x_max, y_min, y_max = self.edge_check(x_max + 1)
            print(x_min, x_max, y_min, y_max)
            the_img = self.img.crop((x_min, y_min, x_max, y_max))
            the_img.resize((self.resize_x, self.resize_y))
            
    def set_feature(self,img = None):#特征化
        if img is None:img = self.img
        h,w = img.size
        pix_cnt_x = 0
        pix_cnt_y = 0
        pixel_cnt_list = []
        for x in range(w):
            for y in range(h):
                if img.getpixel((x, y)) == 0:  # 黑色点
                    pix_cnt_x += 1
            pixel_cnt_list.append(pix_cnt_x)
            pix_cnt_x = 0
        for y in range(h):
            for x in range(w):
                if img.getpixel((x, y)) == 0:
                    pix_cnt_y += 1
            pixel_cnt_list.append(pix_cnt_y)
            pix_cnt_y = 0
        return pixel_cnt_list
    
    def get_feature_str(self,label):
        #特征保存
        feature_list = self.set_feature()
        feature_str = label + " "
        for index in range(len(feature_list)):
            feature_str += str(index) + ":" + str(feature_list[index]) + " "
        feature_str += '\n'
        return feature_str

if __name__ == '__main__':
    from PIL import Image

    img = Image.open("Img/4DK3.png")
    the_obj = ReadImage(img)
    # the_obj.split_save()
    x_min,x_max,y_min,y_max = 0,0,0,0

    for index in range(4):
        x_min, x_max, y_min, y_max = the_obj.edge_check(x_max+1)
        print(x_min, x_max, y_min, y_max)
        the_img = the_obj.img.crop((x_min,y_min ,x_max, y_max))
    # # the_obj.splitImg()
    # the_obj.no_novce().img.save("Img/4DK3.png","PNG")

    # the_obj = ReadImage(Image.open("Img/4DK3.tif"))
    