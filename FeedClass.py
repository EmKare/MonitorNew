class Feed:
    def __init__(self):
        self.__feedName, self.__feedLink, self.__feedAddress, self.__feedParish = "", "", "", ""
        self.__feedLong, self.__feedLat = 0, 0
        self.__feedContact = None
    
    def set__feedName(self, feedName):
        self.__feedName = feedName
        
    def get__feedName(self):
        return self.__feedName
    
    def set__feedLink(self, feedLink):
        self.__feedLink = feedLink
    
    def get__feedLink(self):
        return self.__feedLink
    
    def set__feedLong(self, feedLon):
        self.__feedLong = feedLon
    
    def get__feedLong(self):
        return self.__feedLong
    
    def set__feedLat(self, feedLat):
        self.__feedLat = feedLat
    
    def get__feedLat(self):
        return self.__feedLat
    
    def set__feedAddress(self, feedAddress):
        self.__feedAddress = feedAddress
    
    def get__feedAddress(self):
        return self.__feedAddress
    
    def set__feedParish(self, feedParish):
        self.__feedParish = feedParish
    
    def get__feedParish(self):
        return self.__feedParish
    
    def set__feedContact(self, feedContact):
        self.__feedContact = feedContact
    
    def get__feedContact(self):
        return self.__feedContact
    
class Contact:
    def __init__(self):
        self.__contactTitle, self.__contactFname, self.__contactLname = "", "", ""
        self.__contactAddress, self.__contactParish = "", ""
        self.__contactTele = 0
        self.__contactEmail = None
        
    def set__contactTitle(self, contactTitle):
        self.__contactTitle = contactTitle
        
    def get__contactTitle(self):
        return self.__contactTitle
    
    def set__contactFname(self, contactFname):
        self.__contactFname = contactFname
    
    def get__contactFname(self):
        return self.__contactFname
    
    def set__contactLname(self, contactLname):
        self.__contactLname = contactLname
    
    def get__contactLname(self):
        return self.__contactLname
        
    def set__contactAddress(self, contactAddress):
        self.__contactAddress = contactAddress
    
    def get__contactAddress(self):
        return self.__contactAddress
    
    def set__contactParish(self, contactParish):
        self.__contactParish = contactParish
    
    def get__contactParish(self):
        return self.__contactParish

    def set__contactTele(self, contactTele):
        self.__contactTele = contactTele
    
    def get__contactTele(self):
        return self.__contactTele 
    
    def set__contactEmail(self, contactEmail):
        self.__contactEmail = contactEmail
    
    def get__contactEmail(self):
        return self.__contactEmail
    

c = Contact()
c.set__contactTitle("Mr.")
c.set__contactFname("Paul")
c.set__contactLname("Walker")
c.set__contactAddress("13 Dam Road")
c.set__contactParish("Manchester")
c.set__contactTele(8765555555)
c.set__contactEmail("paulwalks@mail.com")
f = Feed()
f.set__feedContact(c)
f.set__feedName("Megamart Parking Lot")
f.set__feedAddress("10 OldHam Blvd.")
f.set__feedParish("Trelawny")
print(f" {f.get__feedContact().get__contactTitle()} {f.get__feedContact().get__contactFname()} {f.get__feedContact().get__contactLname()} is the contact for the {f.get__feedName()}, located at {f.get__feedAddress()}, {f.get__feedParish()}")