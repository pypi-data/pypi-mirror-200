import cv2 as cv
from cvbot._screen import crop as _crop
import numpy as np


class Image:
    def __init__(self, img, name="snapshot"):
        self.img  = img
        self.name = name
        self.type = "grey" if len(img.shape) < 3 else "bgr"

    def __channels(self):
        """
        self -> int
        Return the number of channels/color layers
        in the current image 'self'
        """
        shp = self.img.shape
        return 1 if len(shp) < 2 else shp[2]

    @property
    def size(self):
        """
        self -> tuple(int, int)
        Return current image width and height in a tuple
        """
        return self.img.shape[:2][::-1]

    def copy(self):
        """
        self -> Image
        Return a copy of current image
        """
        return Image(self.img.copy())

    def grey(self):
        """
        self -> npimage
        Convert current image to gray and return it as a numpy image/matrix
        """
        if self.type == "grey":
            return self.img
        elif self.type == "bgr":
            return cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
        else:
            print("Conversion is not possible from type {} to {}".format(self.type, "grey"))

    def crop(self, region):
        """
        self, (int, int, int, int) -> Image 
        Crop part of current Image using 'region' (x, y, w, h)
        and return it as a new Image
        """
        img = _crop(self.img, region)
        return Image(img)

    def convert(self, tp):
        """
        self, str -> Image
        Convert current Image to a given type 'tp'
        """
        if tp == "grey" or tp == "gray":
            gimg = self.grey()
            if not (gimg is None):
                self.img = gimg
                self.type = "grey"

    def show(self, pos=None):
        """
        self, [Optional] tuple(x, y) -> None
        Display image in a window on screen
        """
        cv.namedWindow(self.name)
        if not (pos is None):
            x, y = pos
            cv.moveWindow(self.name, x, y)
        cv.imshow(self.name, self.img)
        cv.waitKey(0)
    
    def draw_img(self, im, pos):
        """
        self, Image, Point -> Image
        Draw given image 'im' into self
        and return it as a new image
        """
        ow, oh = self.size
        x, y, w, h = pos + im.size
        nw, nh = x + w, y + h
        if x < 0:
            fsx = -x
            ndx = 0
        else:
            fsx = 0
            ndx = x
        if y < 0:
            fsy = -y
            ndy = 0
        else:
            fsy = 0
            ndy = y

        nw = ow if ow > nw else nw
        nh = oh if oh > nh else nh

        nimg = np.zeros((nh + fsy, nw + fsx, self.__channels()), dtype=self.img.dtype)

        nimg[fsy:fsy + oh, fsx:fsx + ow] = self.img
        nimg[ndy:ndy + h, ndx:ndx + w] = im.img

        return Image(nimg)
