class basicCOCOMOModel :
    def __init__(self,loc: int):
        self.loc = loc
        self.kloc = loc/1000.0
        
        if self.kloc<=50:
            self.a,self.b,self.c,self.d = (2.4,1.05,2.5,0.38)
            self.type = "Organic"
        elif self.kloc <=300:
            self.a,self.b,self.c,self.d = (3.0,1.12,2.5,0.35)
            self.type = "Semi_detached"
        else:
            self.type = "Embedded"
            self.a,self.b,self.c,self.d = (3.6,1.20,2.5,0.32)
        self.effort = round(self.a*(self.kloc**self.b), 2)
        self.time = round(self.c*(self.effort**self.d), 2)
        self.people = self.effort//self.time
    def getEffort(self):
        return self.effort
    def getTime(self):
        return self.time
    def getPeople(self):
        return self.people
    def getType(self):
        return self.type
    def getClass(self):
        return "BASIC"
class intermediateCOCOMOModel:
    def __init__(self,loc: int):
            self.loc = loc
            self.kloc = loc/1000.0
            if self.kloc<=50:
                self.a,self.b,self.c,self.d = (2.4,1.05,2.5,0.38)
                self.type = "Organic"
            elif self.kloc <=300:
                self.a,self.b,self.c,self.d = (3.0,1.12,2.5,0.35)
                self.type = ""
            else:
                self.type = "Semi_detached"
                self.a,self.b,self.c,self.d = (3.6,1.20,2.5,0.32)
            self.eaf = self.a*self.b*self.c*self.d
            self.effort = self.a*(self.kloc**self.b)*self.eaf
            self.time = self.c*(self.effort**self.d)
            self.people = self.effort//self.time
    def getEffort(self):
        return self.effort
    def getTime(self):
        return self.time
    def getPeople(self):
        return self.people
    def getType(self):
        return self.type
    def getClass(self):
        return "INTERMEDIATE"
    
class COCOMOapp:
    def __init__(self):
        self.model = None
    def enter_data(self):
        while True:
            loc = int(input("Enter lines of code: "))
            ch = int(input("choose model type: 1: basic: 2: intermediate: "))
            if ch == 1:
                self.model = basicCOCOMOModel(loc)
            elif ch == 2:
                self.model = intermediateCOCOMOModel(loc)
            
            if loc<=0 or ch not in {1,2}:
                print("ENTER VALID LOC OR CHOICE")
                continue
            
            print("DATA ENTER SUCCESS")
            
            break
        
    def showINFO(self):
        print("\n=============COCOMO RESULTS=============")
        print("MODEL USED: ", self.model.getClass())
        print("Project Type: ",self.model.getType())
        print("Effort: ",self.model.getEffort())
        print("Time: ",self.model.getTime())
        print("People: ",self.model.getPeople())

if __name__ == "__main__":
    app = COCOMOapp()
    app.enter_data()
    app.showINFO()