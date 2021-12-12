from PIL import Image

class BuildImage:
    def __init__(self,imageLocations:list,imageSize:tuple=(100,100)):
        self.imageLocations = imageLocations
        self.build = Image.new("RGBA",imageSize,(0,0,0,0))

    
    def mergeAllImages(self):
        for imageLocation in self.imageLocations:
            self.build.paste(Image.open(imageLocation),(0,0),Image.open(imageLocation))

    def SaveImage(self,filePath):
        self.build.save(filePath)
    
    
    