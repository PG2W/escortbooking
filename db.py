import sqlite3

#Klassen der håndtager databasen
class Database():
    def __init__(self, db_name:str):
        #Opretter forbindelse med databasen
        self.db_name = db_name
        self.opencon()
        
        #Sætter databasen op hvis den ikke er det
        self.cur.execute("CREATE TABLE IF NOT EXISTS reservations (name text, date text, time text, escort text)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS escorts (escort text)")
        self.cur.execute("SELECT COUNT(*) FROM escorts")
        count = self.cur.fetchall()[0][0]
        if count == 0:
            escorts = ['Ida Kina', 'Oliver 1', 'Adamowich', 'Christian Lille Lund']
            for x in escorts:
                self.cur.execute("INSERT INTO escorts VALUES (?)", (x,))
        self.closecon()


    def opencon(self):
        self.con = sqlite3.connect(f'{self.db_name}.db')
        self.cur = self.con.cursor()

    def closecon(self):
        self.con.commit()
        self.con.close()

    #Funktionen som man kan tilføje escorts med
    def addescort(self, escort:str):
        self.opencon()
        self.cur.execute("INSERT INTO escorts VALUES (?)", (escort,))
        self.closecon()

    #Returnerer listen af alle escorts
    def fetchescortslist(self):
        self.opencon()
        self.cur.execute("SELECT * FROM escorts")
        escortsraw = self.cur.fetchall()
        escortslist = []
        for x in escortsraw:
            for y in x:
                escortslist.append(y)
        self.closecon()
        return escortslist

    #Returnerer alle reserveret tidspunkter for bestemt dato og escort
    def getreservedlist(self, date, escort):
        self.opencon()
        self.cur.execute("SELECT time FROM reservations WHERE date == (?) AND escort == (?);", (date, escort))
        reservedtimes = self.cur.fetchall()
        timeslist = []
        liststr = ""
        for x in reservedtimes:
            for y in x:
                liststr += y
            liststr += ", "
        liststr = liststr.rstrip(", ")
        timeslist = liststr.split(', ')
        self.closecon()
        return timeslist
    
    #Returnerer reserveret tider for bestemt booking nummer 
    def getreservedlistfor(self, rowid):
        self.opencon()
        self.cur.execute("SELECT time FROM reservations WHERE rowid == (?);", (rowid,))
        reservedtimes = self.cur.fetchall()
        timeslist = []
        liststr = ""
        for x in reservedtimes:
            for y in x:
                liststr += y
            liststr += ", "
        liststr = liststr.rstrip(", ")
        timeslist = liststr.split(', ')
        self.closecon()
        return timeslist
    
    #Returnerer escort for bestemt booking nummer
    def getescortfor(self, rowid):
        self.opencon()
        self.cur.execute("SELECT escort FROM reservations WHERE rowid == (?);", (rowid,))
        fetch = self.cur.fetchall()
        self.closecon()
        return fetch[0][0]

    #Returnerer dato for bestemt booking nummer
    def getdateforbooking(self, rowid):
        self.opencon()
        self.cur.execute("SELECT date FROM reservations WHERE rowid == (?);", (rowid,))
        fetch = self.cur.fetchall()
        self.closecon()
        return fetch[0][0]
    
    #Returnerer alle reservationer
    def getallreservations(self):
        self.opencon()
        self.cur.execute("SELECT rowid, * FROM reservations")
        fetch = self.cur.fetchall()
        self.closecon()
        return fetch

    #Returnerer reservationen for bestemt booking nummer og navn
    def getreservationsecure(self, name, bookingid):
        self.opencon()
        self.cur.execute("SELECT * FROM reservations WHERE name = ? AND rowid = ?", (name, bookingid))
        fetch = self.cur.fetchall()
        self.closecon()
        return fetch

    #Opret en reservation og returner bookingid
    def reservereturnid(self, name, datef, hoursf, escort):
        self.opencon()
        self.cur.execute("INSERT INTO reservations VALUES (?, ?, ?, ?)", (name, datef, hoursf, escort))
        self.cur.execute("SELECT rowid FROM reservations WHERE name == (?) AND date == (?) AND time == (?) AND escort == (?)", (name, datef, hoursf, escort))
        bookingid = self.cur.fetchall()[0][0]
        self.closecon()
        return bookingid
    
    def changereservation(self, name, datef, hoursf, escort, bookingid):
        self.opencon()
        self.cur.execute("UPDATE reservations SET name = (?), date = (?), time = (?), escort= (?) WHERE rowid = (?)", (name, datef, hoursf, escort, bookingid))
        self.closecon()
    
    def deletereservation(self, bookingid):
        self.opencon()
        self.cur.execute("DELETE FROM reservations WHERE rowid = (?) AND name = (?)", (bookingid))
        self.closecon()



    
    
