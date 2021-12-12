import json
import random

if __name__ == "__main__":
    print("This file acts only as a holder for class 'WeightedJson' and associated methods.")
    print("See top of file comments for all use cases.")

    """
    ***JSON FILE MANIPULATION***
    loadJson() - 0 args, loads sjson object into self.jsonObj from specified filepath
    saveJson() - 0 args, saves self.jsonObj object to specified filepath, will overwrite

    ***JSON OBJECT MANIPULATION***
    addAttribute(title,weight,payload) - 3 args, adds new attribute with specified paramaters, will not add attribute if attribute exists with passed 'attributeName' already.
    editAttributeValues(attributeName,weight*,payload*) - 3 args 1 manditory, replaces values for params that are passed to relative 'attributeName'. Both 'weight' and 'payload' are optional params.
    removeAttribute(attributeName) - 1 args, removes specified Attribute
    _updateTotalWeight() - 0 args, updates 'totalWeight' for entire self.jsonObj - totalling each attributes individual weight


    ***GETTERS***
    getJsonObj() - 0 args, returns entirety of self.jsonObj
    getPercentage(attributeName) - 1 args, returns percentage float of chance of recieving said attribute based on its 'weight' relative to 'totalWeight'
    getAttributeWeight(attributeName) - 1 args, returns weight of specified attribute.
    getAttributePayload(attributeName) - 1 args, returns payload of specified attribute.
    
    
    ***UTILITY***
    _findMatch(titlename,titledata) - 2 args, searches self.JsonObj[0]["attributes"] for specified titlename, if found: queries if associated value matches titledata, if so - returns entirety of Lowest level Json Object local to where the match was found

    ***APPLICATIONS***
    genAttribute() - 0 args, randomly picks an attribute relative to its weight.


    ***AUTH KALANZ***
    """

class WeightedJson:
    def __init__(self,filepath:str=None):
        self.jsonObj = None
        
        if filepath != None: #loads json file specified within filepath, if  filepath is not left blank.
            self.loadJson(filepath)
            
            if self.jsonObj == None: #sets defaul value of jsonObj, if jsonObj is unable to be loaded from specified filepath
                self.jsonObj = json.loads('[{"totalWeight":0,"attributes":[]}]')
    
        else: #instantiates default json obj if filepath is not left blank
            self.jsonObj = json.loads('[{"totalWeight":0,"attributes":[]}]')


    def loadJson(self,filePath:str): #loads json from specified file
        try:
            self.jsonObj = json.loads(open(filePath,"r").read())
        except:
            print(f"Error - couldnt load data from {filePath} into Json Object.\n")


    def saveJson(self,filePath:str): #saves json to specified filepath, will overwrite
        try:
            open(filePath,"w+").write(json.dumps(self.jsonObj))
        except:
            print(f"Error - couldn't save Json Object into {filePath}\n")


    def addAttribute(self,title:str,weight:int=0,payload:list=[]): #adds new attribute with specified paramaters, STRING title, weight INT, load LIST
        title = title.lower()
        if self._findMatch("attributeName",title)["found"]: #if attribute by passed title already exists
            print(f"Error - Attribute by name {title} already exists. Attribute was not added.\n")
            return #prematurely ends function
        else:
            self.jsonObj[0]["attributes"].append({"attributeName":title,"weight":weight,"payload":payload})
            print(f"Successfully added new attribute.\nattributeName:'{title}' , weight:{weight} , payload{payload}\n")
            self._updateTotalWeight()


    def editAttributeValues(self,attributeName:str,weight:int=None,payload:list=None): #replaces values for params that are passed of mentioned attributeName
        
        if weight != None or payload != None: #runs method content only if a value has been passed for atleat 1 optional param: 'weight' or 'payload'
            result = self._findMatch("attributeName",attributeName)
            if result["found"]:
                attribute = self.jsonObj[0]["attributes"][self.jsonObj[0]["attributes"].index(result["data"])] #replace with 'WITH , AS' in future
                
                if weight != None: #if value is passed into 'weight' param, edit attribute 'weight' value
                    attribute["weight"] = weight

                if type(payload) is list: #if value is passed into 'payload' param, edit attribute 'payload' value
                    attribute["payload"] = payload #if payload data tpye is list, replace entire payload
                else:
                    print("Error - Cannot replace payload with datatype that is not List - it was not edited\n")
            else:
                print(f"Error - Failed to locate attribute by attributeName '{attributeName}' - it was not edited.\n")

        else: #if no values were passed for either optional params 'weight' or 'payload'
            print(f"Error - no values were passed for editing, no value of attribute '{attributeName}' were edited.\n")


    def removeAttribute(self,title:str): #removes specified Attribute
        result = self._findMatch("attributeName",title) #replace with 'WITH , AS' in future
        if result["found"]:
            self.jsonObj[0]["attributes"].remove(result["data"])
            print(f"Successfully removed attribute:\nattributeName:'{title}' , weight:{result['data']['weight']} , payload{result['data']['payload']}\n")
            self._updateTotalWeight()
            return
        print(f"Failed to locate attribute by attributeName '{title}' - it was not removed.\n")


    def getdJsonObj(self): #returns entirety of self.jsonObj
        return self.jsonObj

    def getPercentage(self,attributeName:str): #returns percantage chance of selection of passed attributeName
        result = self._findMatch("attributeName",attributeName) #replace with 'WITH , AS' in future
        if result["found"]:
            return (result["data"]["weight"] / self.jsonObj[0]["totalWeight"]) * 100
        else:
            print(f"Error - No such attribute was found to match attributeName: '{attributeName}'\n")
            return 0
            

    def genAttribute(self): #gets random attribute based on all attributes weights
        if self.jsonObj[0]["totalWeight"] != 0:
            RandomWeight = random.randrange(0,self.jsonObj[0]["totalWeight"] +1)
            if not len(self.jsonObj[0]["attributes"]) == 0: #if there are attributes that exist
                for attribute in self.jsonObj[0]["attributes"]:
                    RandomWeight -= attribute["weight"]
                    if RandomWeight <= 0:
                        return attribute
            else: #if no attributes exist
                print("Error, no attributes available to itterate through.\n")
        else:
            print("Error - cannot generate attribute of 0 'totalWeight'.")
    

    def getAttributeWeight(self,attributeName:str):
        result = self._findMatch("attributeName",attributeName)
        if result["found"]:
            return result["data"]["weight"]
        else:
            print(f"Error - No such attribute was found to match attributeName: '{attributeName}'\n")
            return None
    

    def getAttributePayload(self,attributeName:str):
        result = self._findMatch("attributeName",attributeName)
        if result["found"]:
            return result["data"]["payload"]
        else:
            print(f"Error - No such attribute was found to match attributeName: '{attributeName}'\n")
            return None
    
    def _updateTotalWeight(self):
        total = 0
        for attribute in self.jsonObj[0]["attributes"]: #itterate weights within attributes
            total += attribute["weight"] #append to newly created 'total'

        self.jsonObj[0]["totalWeight"] = total #set 'totalWeight' within local jsonObj to 'total'

    def _findMatch(self,titleName,titleData): #if titledata and titlename are found in a matching pair, return rest of json object.
        for index in self.jsonObj[0]["attributes"]:
            for title in index:
                if title == titleName:
                    if index[title] == titleData:
                        return { #when match is found
                        "found":True,
                        "data":index
                        }
                    break #if title name is found, but associated date does not match - break loop and stop searching this index of the JsonObject

        return { #if searched for match is not found
        "found":False,
        }
