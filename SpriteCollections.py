from WeightedJson import WeightedJson
from os import listdir
from BuildImage import BuildImage





class SpriteCollection():
    def __init__(self,attributesMasterFolder_Path:str):
        if attributesMasterFolder_Path[len(attributesMasterFolder_Path) - 1] == "/": #if last char of passed folderpath is '/' remove it.
            attributesMasterFolder_Path = attributesMasterFolder_Path[0:len(attributesMasterFolder_Path) - 1]
        
        self.MasterFolderPath = attributesMasterFolder_Path



    def createWeightsJson(self): #creates 'weights.json' files for all folders within master folder and populates it, if one does not exist already.
        for folder in listdir(self.MasterFolderPath):
            if not "." in str(folder):
                if "weights.json" not in listdir(f"{self.MasterFolderPath}/{folder}/"):
                    jsonObj = WeightedJson()
                    for file in listdir(f"{self.MasterFolderPath}/{folder}/"):
                        if ".png" in str(file) and "template" not in str(file):
                            jsonObj.addAttribute(str(file).replace(".png","").replace(f"{str(folder)}_","").lower(),0,[{"ImageLocation":f"{self.MasterFolderPath}/{folder}/{str(file)}"}])
                    jsonObj.saveJson(f"{self.MasterFolderPath}/{folder}/weights.json")
                else:
                    print(f"Error - 'weights.json' already exists in directory '{self.MasterFolderPath}/{folder}/' - it was not replaced.")
            else:
                print(f"Error - '{folder}' is a file, not a folder - it was skipped.")


    def updateAll_TotalWeights(self): #Updates The Total Weight for all attribute Folders within the Master Folder
        for folder in listdir(self.MasterFolderPath):
            if not "." in str(folder):
                if "weights.json" in listdir(f"{self.MasterFolderPath}/{folder}/"):
                    jsonObj = WeightedJson(f"{self.MasterFolderPath}/{folder}/weights.json")
                    jsonObj._updateTotalWeight()
                    jsonObj.saveJson(f"{self.MasterFolderPath}/{folder}/weights.json")
                    print(f"Successfully Updated 'TotalWeight' for '{self.MasterFolderPath}/{folder}/weights.json'")
                else:
                    print(f"Error - could not locate 'weights.json' within '{self.MasterFolderPath}/{folder}/' - 'TotalWeight' was not updated.")
            else:
                print(f"Error - '{folder}' is a file, not a folder - it was skipped.")
        else:
            print(f"Error - No folders found in '{self.MasterFolderPath}' - No 'totalWeight's were updated..")
            return
        print("\nSuccessfully Updated all 'TotalWeights'.")


    # def getRandomAttributes_FileLocations(self): #Generate random Attributes, using WeightedJson.genAttribute() - then compile a list of all 'ImageLocation's present within associated Payloads - returns said list
    #     filepaths = []
    #     for folder in listdir(self.MasterFolderPath):
    #         if not "." in str(folder):
    #             jsonObj = WeightedJson(f"{self.MasterFolderPath}/{folder}/weights.json")
    #             filepaths.append(jsonObj.genAttribute()["payload"][0]["ImageLocation"])
    #     return(filepaths)


    def getRandomAttributes(self): #Generate random Attributes, using WeightedJson.genAttribute() - then compile a list of all 'ImageLocation's present within associated Payloads - returns said list
        attributes = []
        for folder in listdir(self.MasterFolderPath):
            if not "." in str(folder):
                jsonObj = WeightedJson(f"{self.MasterFolderPath}/{folder}/weights.json")
                attributes.append(jsonObj.genAttribute())
        return(attributes)

    def loadAll_NewAttributes(self): #loads all attributes into 'weights.json' if it does not already exist there.
        for folder in listdir(self.MasterFolderPath):
            if not "." in str(folder):
                jsonObj = WeightedJson(f"{self.MasterFolderPath}/{folder}/weights.json")
                folderPath = f"{self.MasterFolderPath}/{folder}/"
                
                for file in listdir(folderPath):
                    if ".png" in str(file) and "template" not in str(file): #if file is a png, and does not contain keword template
                        NewAttributeName = str(file).replace(".png","").replace(f"{str(folder)}_","").lower()
                        if not jsonObj._findMatch("attributeName",NewAttributeName)["found"]:
                            jsonObj.addAttribute(NewAttributeName,0,[{"ImageLocation":f"{folderPath}/{str(file)}"}])
                            print(f"\nNew attribute '{NewAttributeName}' added to  '{folderPath}/weights.json'\n")
                jsonObj.saveJson(f"{folderPath}/weights.json")
                print(f"Success - Updated '{folderPath}'")
            else:
                print(f"Error - '{folder}' is a file, not a folder - it was skipped.")
        print(f"\nSuccess - All New attributes within '{self.MasterFolderPath}' loaded. ") #upon method completion






class Sprite(SpriteCollection):
    def __init__(self,name,attributesMasterFolder_Path:str,imageSize:tuple=(640,640)):
        super().__init__(attributesMasterFolder_Path)
        self.sprite = None
        self.name = name
        self.imageSize = imageSize
        self.reloadSprite()
        
    def reloadSprite(self): #Replaces all current attributes, generating New character
        self.attributes = super().getRandomAttributes()
        def constructFileLocations():
            self.fileLocations = []
            for attribute in self.attributes:
                self.fileLocations.append(attribute["payload"][0]["ImageLocation"])
        
        def constructAttributeTitles():
            self.attributeTitles = []
            for attribute in self.attributes:
                self.attributeTitles.append(attribute["attributeName"])

        constructFileLocations()
        constructAttributeTitles()

        self.sprite = BuildImage(self.fileLocations,self.imageSize)
        self.sprite.mergeAllImages()


    def displayAttributes(self):
        for AttributeTitle in self.attributeTitles:
            print(AttributeTitle)


    def output(self,OutPutFolder:str = "./",FileExtension:str="png"): #outputs image of sprite to specified location, with specified file extension
        if not OutPutFolder[len(OutPutFolder) - 1] == "/": #if last char of passed folderpath is '/' remove it.
            OutPutFolder += "/"
        self.sprite.SaveImage(f"{OutPutFolder}{self.name}.{FileExtension}")