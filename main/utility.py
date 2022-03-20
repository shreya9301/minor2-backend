from PIL import Image
import numpy as np
import random
def Random_places(n,recons):
        # random_places = np.empty(recons)
        random_places = []
        for i in range(0,recons):
                
                while(True):
                        rand_int  = np.random.randint(0,n-1)
                        #print(rand_int)
                        if(rand_int not in random_places):
                                random_places.append(rand_int)
                                break
        return random_places

# def encrypt(width,height,img):

def Get_RGB(argb_int:int):
        blue =  argb_int & 255
        green = (argb_int >> 8) & 255
        red =   (argb_int >> 16) & 255
        alpha = (argb_int >> 24) & 255
        return (red, green, blue, alpha)


def create_image(raw_list: list, width: int, height: int,image_number: int):
        """
        For Creating the image 
        """
        pixel = []
        k = 0
        for i in range(height):
                int_pixel= []
                for j in range(width):
                        red, green, blue, alpha = Get_RGB(int(raw_list[k]))
                        k += 1
                        int_pixel.append((red, green, blue, alpha))
                
                pixel.append(int_pixel)
                
        
        array = np.array(pixel, dtype=np.uint8)
        new_image = Image.fromarray(array)
        new_image.save(f"{image_number}.png")
        # new_image.save('new.png')


img = Image.open("./pic1.jpg")

width, height  = img.size
# input n=number of divisions, k = min no of divisons
print("Enter the value of N: ")
n = int(input())
print("Enter the Value of K: ")
k = int(input())

# recons  = number of images to be reconstructed
recons = (n-k) + 1

# img_share = 3d array to store the value of each pixel of n shares 
img_share = np.empty((n,width*height,32))

#converting image to Red, Green, Blue, Alpha (Brightness)
rgb_im = img.convert('RGBA')

# Pixel values of the Main RGBA Image in the form list([255,255,255,255])
PIX = []
for i in range(0,width):
    for j in range (0,height):
        t = list(rgb_im.getpixel((i,j)))
        PIX.append(t)

# To convert each pixel value into a 32 bit binary number
img_bin = []
for i in range(0,len(PIX)):
        a,red,green,blue = format(PIX[i][3],'b'),format(PIX[i][0],'b'),format(PIX[i][1],'b'),format(PIX[i][2],'b')
        if(len(a) < 8):
                a = '0'*(8-len(a)) + a
        if(len(red) < 8):
                red = '0'*(8-len(red)) + red
        if(len(green) < 8):
                green = '0'*(8-len(green)) + green
        if(len(blue) < 8):
                blue = '0'*(8-len(blue)) + blue
        color = a + red + green + blue
        img_bin.append(color)

#print(img_bin)

# random_arr = Random_places(n,recons)
# print("This is random 1 ",random_arr)

for i in range(0, len(img_bin)):
    for j in range (0,32):
            if(img_bin[i][j] == '1'):
                random_arr = Random_places(n,recons)
                #print("random 2: ",random_arr)
                for k in range(0,recons):
                    img_share[random_arr[k]][i][j]=int(1)


img_cons = []

# imgage construction from shares 

#print(img_share)
for i in range(0,n):
        in_between_image = []
        for j in range(0,width*height):
                val = ""
                for k in range(0,32):
                        val = val + str(int(img_share[i][j][k]))
                in_between_image.append(val)

        img_cons.append(in_between_image)
        

for i in range(len(img_cons)):
        create_image(img_cons[i],width,height,i)