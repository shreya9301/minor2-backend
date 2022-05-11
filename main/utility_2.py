from PIL import Image, ImageFilter
import numpy as np
from wand.image import Image as Image2
# from main import create_image
import os



# def Get_RGB(argb_int:list):
#         blue =  argb_int[0] & 255
#         green = (argb_int[1] >> 8) & 255
#         red =   (argb_int[2] >> 16) & 255
#         alpha = (argb_int[3] >> 24) & 255
#         return (red, green, blue, alpha)


def create_image(raw_list: list, width: int, height: int):
        """
        For Creating the image 
        """
        pixel = []
        k = 0
        for i in range(height):
                int_pixel= []
                for j in range(width):
                        intermediate = raw_list[k:k+4]
                        # red, green, blue, alpha = Get_RGB(intermediate)
                        # print(red,green,blue,alpha)
                        k += 4
                        int_pixel.append((intermediate[0], intermediate[1], intermediate[2], intermediate[3]))
                
                pixel.append(int_pixel)
                
        
        array = np.array(pixel, dtype=np.uint8)
        new_image = Image.fromarray(array)
        new_image.save("final.png")
        # new_image.save('new.png')
    
def decrypted(path_of_file,username,date):
        k = int(input("Enter the value of k"))
        saving_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/media/"+username+"/"+str(date)

        img = Image.open(path_of_file)
        # height = int(input())
        # width = int(input())
        width, height  = img.size
        share = np.empty((k,width*height*4))
        final = np.zeros((width*height*4))
        #intermediate = np.empty((width*height))
        intermediate = []

        for i in range(0,k):
                img = Image.open(saving_dir+"/"+str(i)+".png")
                # w, h  = img.size
                for j in range(0,width*height):
                        inter_immeidate = img.getpixel((j%width,j//width))
                        # print("intermdiate value ",inter_immeidate)
                        for temp in inter_immeidate:
                                intermediate.append(temp)
                        
                share[i] = np.asarray(intermediate)
        #     print(intermediate)
        #     print(type(intermediate))

        intermediate = []

        #print(share[0].size())
        print(final[0])
        final = final.astype(int)
        for i in range(0,k):
                # print(k)
                final = np.bitwise_or(final.astype(int),share[i].astype(int))
                # print(share[i].astype(int))
                # final[j] = final[j] | share[i]

        #for i in range(len(final)):
        final = final.tolist()
        # print(final[0::100])
        create_image(final,width,height)


def decryption_test(path_of_file,username,date):
        saving_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/media/"+username+"/"+str(date)
        file_saved = os.path.join(saving_dir,"final.png")
        print(file_saved)
        print(path_of_file)
        with Image2(filename=path_of_file) as img:

        #         # Generate noise image using spread() function
                img.noise("laplacian", attenuate = 10.0)
                img.save(filename = file_saved)

        return file_saved

        
# test("username","date")