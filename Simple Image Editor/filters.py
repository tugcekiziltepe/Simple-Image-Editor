from PIL import Image, ImageOps, ImageEnhance, ImageFilter
from scipy.stats.mstats import mquantiles
from skimage.util import random_noise
import numpy as np
import cv2


def openImage(image_path):
    image = Image.open(image_path)

    if (IsGrayScale(image)):
        image = image.convert("L")

    return image


def saveImage(image, path):
    """It saves images given path

    Args:
        image (PIL.Image)
        path (str): path of the image
    """
    
    image.save(path + ".jpg")


def NumberOfChannels(sourceImage):
    if(len(np.asarray(sourceImage).shape) < 3):
        return 1
    return np.asarray(sourceImage).shape[2]


def IsTransparent(sourceImage):
    if(sourceImage.mode == "RGBA" or "transparency" in sourceImage.info):
        return True
    return False


def IsGrayScale(sourceImage):
    if(len(np.asarray(sourceImage).shape) < 3):
        return True
    if(NumberOfChannels(sourceImage) == 1):
        return True

    width, height = sourceImage.size
    for i in range(width):
        for j in range(height):
            if(IsTransparent(sourceImage)):
                r, g, b, a = sourceImage.getpixel((i, j))
            else:
                r, g, b = sourceImage.getpixel((i, j))
            if r != g != b:
                return False
    return True


def ConvertToGrayScale(image):
    if(IsGrayScale(image)):
        print("ConvertToGrayScale: The source image is already grayscale! Please be sure to give a proper colorful image.")
        return image

    print("ConvertToGrayScale: The source image is converted to grayscale successfully.")
    return image.convert("L")


def InvertImage(image):
    if(IsTransparent(image)):
        sourceImage = image.convert("RGB")
        print("InvertImage: The transparent source image is inverted successfully.")
        return ImageOps.invert(sourceImage).convert("RGBA")

    print("InvertImage: The source image is inverted successfully.")
    return ImageOps.invert(image)


def MirrorImage(image):
    print("MirrorImage: The source image is mirrored successfully.")
    return ImageOps.mirror(image)


def AddNoise(image, mode="gaussian", var=0.0025, amount=0.05):
    """
    https://scikit-image.org/docs/stable/api/skimage.util.html#random-noise
    One of the following strings, selecting the type of noise to add:
        "gaussian" Gaussian-distributed additive noise.
        "poisson" Poisson-distributed noise generated from the data.
        "salt" Replaces random pixels with 1.
        "pepper" Replaces random pixels with 0 (for unsigned images) or -1 (for signed images).
        "s&p" Replaces random pixels with either 1 or low_val, where low_val is 0 for unsigned images or -1 for signed images.
        "speckle" Multiplicative noise using out = image + n*image, where n is Gaussian noise with specified mean & variance.
    """

    if(var < 0 or 0.0):
        print("AddNoise: Negative \"var\" value is invalid! No noise added.")
        return image

    if(amount < 0 or 0.0):
        print("AddNoise: Negative \"amount\" value is invalid! No noise added.")
        return image

    sourceImage = image

    if(IsGrayScale(sourceImage) and NumberOfChannels(sourceImage) > 1):
        sourceImage = sourceImage.convert("L")

    # random_noise() method will convert image in [0, 255] to [0, 1.0]
    # inherently it uses np.random.normal() to create normal distribution and adds the generated noised back to image
    if(mode == "gaussian"):
        noiseImage = random_noise(np.asarray(sourceImage), mode=mode, var=var)
    elif(mode == "poisson"):
        noiseImage = random_noise(np.asarray(sourceImage), mode=mode)
    elif(mode == "salt"):
        noiseImage = random_noise(np.asarray(sourceImage), mode=mode, amount=amount)
    elif(mode == "pepper"):
        noiseImage = random_noise(np.asarray(sourceImage), mode=mode, amount=amount)
    elif(mode == "s&p"):
        noiseImage = random_noise(np.asarray(sourceImage), mode=mode, amount=amount)
    elif(mode == "speckle"):
        noiseImage = random_noise(np.asarray(sourceImage), mode=mode, var=var)
    else:
        print("AddNoise: Noise mode does not exist! No noise added.")
        return sourceImage

    print("AddNoise: The", mode, "noise is added to the source image successfully.")
    noiseImage = (255 * noiseImage).astype(np.uint8)
    return Image.fromarray(noiseImage)


# factor = 1 -> original image
# 0 < factor < 1 -> darkened image
# factor > 1 -> brightened image
def AdjustBrightness(image, factor=1.5):
    if(factor < 0 or 0.0):
        print("AdjustBrightness: Negative \"factor\" value is invalid! Brightness is not modified.")
        return image

    enhancer = ImageEnhance.Brightness(image)
    print("AdjustBrightness: The brightness of the source image is adjusted by a factor of {} successfully.".format(factor))
    return enhancer.enhance(factor)


# factor = 1 -> original image
# 0 < factor < 1-> muted or calmed image
# factor > 1 -> saturated image
def AdjustSaturation(image, factor=1.75):
    if(factor < 0 or 0.0):
        print("AdjustSaturation: Negative \"factor\" value is invalid! Saturation is not modified.")
        return image

    enhancer = ImageEnhance.Color(image)
    print("AdjustSaturation: The saturation of the source image is adjusted by a factor of {} successfully.".format(factor))
    return enhancer.enhance(factor)


# (left, top) = top left coordinates i.e (x,y)
# (right, bottom) = bottom right coordinates i.e. (x,y)
# Area to be cropped:
#       left <= x < right and top <= y < bottom
def CropImage(image, left, top, right, bottom):
    if(left >= right or top >= bottom):
        print("CropImage: Invalid positions! Can not crop image from left = {} top = {} to right = {} bottom = {}."
              "\n\t\t   Should satisfy \"right > left and bottom > top\"".format(left, top, right, bottom))
        return image

    if(left < 0):
        left = 0
    if(top < 0):
        top = 0
    if(right > image.size[0]):
        right = image.size[0]
    if(bottom > image.size[1]):
        bottom = image.size[1]

    print("CropImage: The source image is cropped from left = {} top = {} to right = {} bottom = {} successfully.".format(left, top, right, bottom))
    return image.crop((left, top, right, bottom))


def flip(image):
    """Flip the image around the x axis.

    Args:
        image (PIL.Image)

    Returns:
        PIL.Image: Flipped image
    """

    return image.transpose(Image.FLIP_TOP_BOTTOM)


def gaussianBlurImage(image):
    """Blur the image with gaussian blur with radius 1.

    Args:
        image (PIL.Image)

    Returns:
        (PIL.Image): Blurred image
    """

    return image.filter(ImageFilter.GaussianBlur(radius=1))


def deblurImage(image):
    """Deblur image using laplacian filter.

    Args:
        image (PIL.Image)

    Returns:
        PIL.Image: Deblurred image
    """

    return image.filter(ImageFilter.Kernel((3, 3), (0, -1, 0, -1, 5, -1, 0, -1, 0)))


def rotateImage(image):
    """Rotate image by angle

    Args:
        image (PIL.Image)

    Returns:
        PIL.Image: Rotated image
    """

    return image.rotate(90, expand=True)


def changeColorBalance(image, saturationLevel=0.5):
    """The color cast can be removed from an image
    by scaling the histograms of each of the R, G, and B channels
    so that they span the complete 0-255 scale.
    Resource: https://web.stanford.edu/~sujason/ColorBalancing/simplestcb.html
    Args:
        image (PIL.Image)

    Returns:
        PIL.Image: color balanced image
    """
    if IsGrayScale(image):
        return image

    image = np.asarray(image)
    # 1. Determine the histogram for each RGB channel
    # find the quantiles that correspond to our desired saturation level.

    # saturationLevel controls the saturation of a certain percentage of the pixels to black and white.
    q = np.array([saturationLevel / 2.0, 1 - saturationLevel / 2.0])

    output_image = np.zeros(image.shape)
    for dim in range(image.shape[2]):  # For R, G, B channels in image
        low, high = mquantiles(image[:, :, dim], q, alphap=0.5,
                               betap=0.5)  # alphap and betap are plotting positions parameter

        # 2. Cut off the outlying values by saturating a certain percentage of the pixels to black and white.
        # Set pixel value to low where pixel value is smaller than low,
        # Set pixel value to high where pixel value is greater than high
        output_image[:, :, dim] = np.where(image[:, :, dim] < low, low,
                                           (np.where(image[:, :, dim] > high, high, image[:, :, dim])))

        # 3. Scale the saturated histogram to span the full 0-255 range.
        min = np.amin(output_image[:, :, dim])  # Min value of the channel
        max = np.amax(output_image[:, :, dim])  # Max value of the channel
        difference = (max - min if max - min != 0 else 1)  # Difference cannot be equal to 1.
        output_image[:, :, dim] = (output_image[:, :, dim] - min) * 255 / difference

    return Image.fromarray(output_image.astype(np.uint8))


def adjustContrast(image, factor=0.5):
    """Adjust image contrast.
    An enhancement factor of 0.0 gives a solid grey image.
    A factor of 1.0 gives the original image.

    Args:
        image (PIL.Image): 
        factor (float): Image contrast will change with a factor.
        If factor is equal to 1, it gives original image.
        If factor is less than 1, image's constrast will be decreased.
        If factor is greater than 1, image's contrast will be increased.

    Returns:
        PIL.Image
    """
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(factor)
    return image


def detectEdges(image, threshold1=120, threshold2=150, L2gradient=False):
    """Detect the edges using Canny Algorithm.
    Consists of 4 steps:
        1. Noise reduction
        2. Finding intensity gradient of the image
        3. Finding intensity gradient of the image
        4. Non-maximum suppression
        5. Hystresis Thresholding

    Args:
        image (PIL.Image)

    Returns:
        PIL.Image: Blurred image
    """

    # L2gradient specifies the equation for finding gradient magnitude. Edge_Gradient(G)=|Gx|+|Gy|
    edges = cv2.Canny(np.asarray(image), threshold1=threshold1, threshold2=threshold2, L2gradient=L2gradient)
    return Image.fromarray(edges)
