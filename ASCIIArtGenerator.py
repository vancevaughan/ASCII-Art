from PIL import Image
import numpy as np

gs = ' .:-=+*#%@'

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

    M = cols
    x = w / M
    y = x / scale
    N = int(h / y)

    converted_image = []

    for j in range(N):
        y1 = int(j * y)
        y2 = int((j + 1) * y)

        # correct last tile
        if j == N - 1:
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
img_array = contrastStretch(image)
image = Image.fromarray(img_array)

ASCIIArt = getASCIIArt(image, 150, 0.45)

outputFile = filename.partition(".")[0] + ".txt"
f = open(outputFile, 'w')
for row in (ASCIIArt):
    f.write(row + '\n')
f.close()
