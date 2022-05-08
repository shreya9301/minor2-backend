from PIL import Image, ImageFilter

#Open existing image
OriImage = Image.open('pic1.jpeg')
#Applying GaussianBlur filter
gaussImage = OriImage.filter(ImageFilter.GaussianBlur(5))
#Save Gaussian Blur Image
gaussImage.save('gaussian_blur.jpg')

from wand.image import Image
with Image(filename ="gaussian_blur.jpg") as img:

	# Generate noise image using spread() function
	img.noise("laplacian", attenuate = 10.0)
	img.save(filename ="noisekoala2.jpeg")

from PIL import Image
# Open Paddington
img = Image.open("noisekoala2.jpeg")

# Resize smoothly down to 16x16 pixels
imgSmall = img.resize((64,64),resample=Image.Resampling.BILINEAR)

# Scale back up using NEAREST to original size
result = imgSmall.resize(img.size,Image.Resampling.NEAREST)

# Save
result.save('result.jpg')