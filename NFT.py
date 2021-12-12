from SpriteCollections import Sprite
from SpriteCollections import SpriteCollection

def CreateSprites(BoilerPlateName,amount,FolderPath):
    for i in range(amount):
        Sprite(f"{BoilerPlateName}_{i+1}","Attributes",(640,640)).output(FolderPath,"png")
        print(f"created new '{BoilerPlateName}' #{i+1} in '{FolderPath}'")


def Update(MasterAttributesFolder):
    x = SpriteCollection(MasterAttributesFolder)
    x.loadAll_NewAttributes()
    x.updateAll_TotalWeights()

#Update("Attributes")

#SpriteCollection("Attributes").createWeightsJson()
CreateSprites("SpriteMan",50,"Dump/")



