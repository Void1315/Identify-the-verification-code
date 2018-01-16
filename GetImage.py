import requests,time,os
from PIL import Image
from ClearImg import ReadImage
class GetImage():
    the_src = "http://59.69.173.117/jwweb/sys/ValidateCode.aspx"
    the_path = "Img"
    def __init__(self):
        pass
    def get_img(self):
        result = requests.get(self.the_src)
        return result.content
        pass
    def save_img(self):

        with open(self.the_path +'/' +str(time.time()) + '.jpg','ab+') as file:
            file.write(self.get_img())
    
if __name__ == '__main__':
    the_obj = GetImage()
    name_list = []
    for i in range(2):
        the_obj.save_img()
    files = os.listdir(GetImage.the_path)
    for file in files:
        Img = ReadImage(Image.open("Img/" + file))
        Img = Img.erase_border().no_novce()
        Img.set_radius(2)
        Img.no_novce()
        Img.set_radius(1)
        Img.no_novce()
        Img.img.save('Img/' + file)
        code =  Img.get_code()
        while code in name_list:
            code = code + '_'
        name_list.append(code)
        os.rename('Img/' + file, 'Img/' + code + '.jpg')
    pass