import cv2

width = 28
height = 28
dim = (width, height)

def resize(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    cv2.imwrite(img_path,resized)

#resize("C:\\Users\\idris\\OneDrive\\IMAGES\\dola.png")

def invert_color(img_path):

    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #TODO : black and white image

invert_color("C:\\Users\\idris\\OneDrive\\IMAGES\\dola.png")