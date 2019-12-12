import os

curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\2.txt'
filename = f'{curdir}\\dec8.txt'
data, w, h = open(filename, 'r').readline(), 25, 6
#data, w, h = "123456789012", 3, 2
#data, w, h = "0222112222120000", 2, 2

class Image:
    def __init__(self, width, height, data):
        self.width = width
        self.height = height
        self.data = data

    def layer_count(self):
        return len(self.data) // self.layer_len()

    def layer_len(self):
        return self.width * self.height

    def get_layer(self, layer):
        start = layer * self.layer_len()
        return self.data[start:start+self.layer_len()]

    def count_chars(self, c, layer):
        s = self.get_layer(layer)
        res = sum([1 for _ in s if _ == c])
        return res

    def effective_pixel(self, p):
        for layer in range(self.layer_count()):
            layerdata = self.get_layer(layer)
            c = layerdata[p]
            if c in "01":
                return c
        raise

    def render_picture(self):
        pic = ""
        for p in range(self.layer_len()):
            pic += self.effective_pixel(p)
        return pic

    def print_image(self):
        pixmap = {"0": " ", "1": "*"}
        pic = self.render_picture()
        for row in range(self.height):
            scanline = ""
            for line in range(self.width):
                p = pic[row*self.width + line]
                
                scanline += pixmap[p]
            print(scanline)


image = Image(w, h, data)
#image = Image(2, 2, data)

def test():
    print(image.layer_count())
    print(image.get_layer(0))
    print(image.render_picture())

def star1():
    minzero = -1
    for i in range(image.layer_count()):
        layer = image.get_layer(i)
        #print(f"{i}: {image.get_layer(i)} 1: {image.count_chars('0', i)}")
        r = image.count_chars('0', i)
        if minzero == -1 or r < minzero:
            minzero = r
            minzerolayer = i

    print(minzerolayer)
    print(image.count_chars('1', minzerolayer) * image.count_chars('2', minzerolayer))

def star2():    
    image.print_image()

star1()
star2()
