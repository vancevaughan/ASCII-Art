from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import numpy as np

gs_reverse = '@%#*+=-:. '
gs = " .:-=+*#%@"

# returns average level of image tile
def getAverageL(tile):
    img = np.array(tile)
    width, height = img.shape

    return np.average(img.reshape(width * height))


# returns full-scale contrast stretched image as numpy array
def contrastStretch(unstretched_image):
    us_img_array = np.array(unstretched_image)
    minL = us_img_array.min()
    maxL = us_img_array.max()
    stretch = 255 / (maxL - minL)

    stretched_image = np.multiply(np.add(us_img_array, -1 * minL), stretch)

    return stretched_image


# returns string array of ASCII art
def getASCIIArt(image, cols, scale):
    w, h = image.size[0], image.size[1]

    m = cols
    x = w / m
    y = x / scale
    n = int(h / y)

    converted_image = []

    for j in range(n):
        y1 = int(j * y)
        y2 = int((j + 1) * y)

        # correct last tile
        if j == n - 1:
            y2 = h

        # append an empty string
        converted_image.append("")

        for i in range(cols):
            # crop image to tile
            x1 = int(i * x)
            x2 = int((i + 1) * x)

            # correct last tile
            if i == cols - 1:
                x2 = w

            # crop image to extract tile
            img = image.crop((x1, y1, x2, y2))

            # get average luminance
            avg = int(getAverageL(img))

            # look up ascii char
            gsval = gs[int((avg * 9) / 255)]

            # append ascii char to string
            converted_image[j] += gsval

    # return txt image
    return converted_image


filename = "selfie.png"
image = Image.open(filename).convert("L")

numCols = 155
scale = 0.5
width, height = image.size[0], image.size[1]

ASCII_array = getASCIIArt(image, numCols, scale)

# write to text file
outputTXTFile = filename.partition(".")[0] + ".txt"
f = open(outputTXTFile, 'w')
for row in ASCII_array:
    f.write(row + '\n')
f.close()

# create ASCII image
k = 8
ASCII_image = Image.new('RGB', (k * width, k * height), '#000000')
draw = ImageDraw.Draw(ASCII_image)
font = ImageFont.truetype("cour.ttf", int(k * 1.625 * width / numCols))
font_color = '#afff14'

y_pos = 0
for row in ASCII_array:
    draw.text((0, y_pos), (row + '\n'), font_color, font)
    y_pos = y_pos + (k * 2 * width / numCols)

ASCII_image.show()

outputPNGFile = filename.partition(".")[0] + "_ASCII.png"
ASCII_image.save(outputPNGFile)
