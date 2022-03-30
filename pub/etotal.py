
import sys

import mysql.connector
import db_variables

from tabulate import tabulate
from db_variables import *

westnum = sys.argv[1]

conn = mysql.connector.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DB)
c = conn.cursor()
c.execute("DELETE FROM elines WHERE elnum="+westnum+" AND lboper='OVL'")
conn.commit()
c.execute("SELECT hrstype,hrs,pnthrs,pricetype,price,lxnum FROM elines WHERE elnum="+westnum)

olap = mysql.connector.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DB)
o = olap.cursor()

o.execute("UPDATE m3overlap SET ox1b = 0, ox1p = 0, ox1c = 0, ox2b = 0, ox2p = 0, ox2c = 0")

xdols = 0
xhrs = 0

pnthrstotal = 0
bodyhrstotal = 0 ## B or blank
mechhrstotal = 0 ## M
framehrstotal = 0 ## F
structhrstotal = 0 ## S
glasshrstotal = 0 ## G
detailhrstotal = 0 ## D
otherhrstotal = 0 ## O

partitemtotal=0 ## N or blank
pmatitemtotal=0 ## P 
bmatitemtotal=0 ## B
hazitemtotal=0 ## H
subletitemtotal=0 ## U
afteritemtotal=0 ## A
towingitemtotal=0 ## T
storageitemtotal=0 ## R
misc1itemtotal=0 ## 1
misc2itemtotal=0 ## 2
misc3itemtotal=0 ## 3

for row in c:
    
## 13 is tuple position for hrstype
    pnthrstotal = pnthrstotal+float(row[2])
    bodyoverlaptag = False

    match row[0]:
        case "B": bodyhrstotal=bodyhrstotal+float(row[1]);bodyoverlaptag = True
        case "M": mechhrstotal=mechhrstotal+float(row[1])
        case "F": framehrstotal=framehrstotal+float(row[1])
        case "S": structhrstotal=structhrstotal+float(row[1])
        case "G": glasshrstotal=glasshrstotal+float(row[1])
        case "D": detailhrstotal=detailhrstotal+float(row[1])
        case "O": otherhrstotal=detailhrstotal+float(row[1])
        case _: bodyhrstotal=bodyhrstotal+float(row[1]);bodyoverlaptag = True

    match row[3]:
        case "N": partitemtotal=partitemtotal+row[4] ## N or blank
        case "P": pmatitemtotal=pmatitemtotal+row[4] ## P 
        case "B": bmatitemtotal=bmatitemtotal+row[4] ## B
        case "H": hazitemtotal=hazitemtotal+row[4] ## H
        case "U": subletitemtotal=subletitemtotal+row[4] ## U
        case "A": afteritemtotal=afteritemtotal+row[4] ## A
        case "T": towingitemtotal=towingitemtotal+row[4] ## T
        case "R": storageitemtotal=storageitemtotal+row[4] ## R
        case "1": misc1itemtotal=misc1itemtotal+row[4] ## 1
        case "2": misc2itemtotal=misc2itemtotal+row[4] ## 2
        case "3": misc3itemtotal=misc3itemtotal+row[4] ## 3
        case _: partitemtotal=partitemtotal+row[4] ## N or blank

    overlapcheck=str(row[5])
    
    if float(row[1])>0 and  bodyoverlaptag :
        o.execute("UPDATE m3overlap SET ox1b = 'X' WHERE oxnum1 ="+overlapcheck+" ")
        o.execute("UPDATE m3overlap SET ox2b = 'X' WHERE oxnum2 ="+overlapcheck+"")

    if float(row[2])>0 :
        o.execute("UPDATE m3overlap SET ox1p = 'X' WHERE oxnum1 ="+overlapcheck+"")
        o.execute("UPDATE m3overlap SET ox2p = 'X' WHERE oxnum2 ="+overlapcheck+"")

    olap.commit()

ovoperation="OVL"

o.execute("SELECT odescription, obodolap, opntolap, occolap FROM m3overlap WHERE ox1b='X' and ox2b='X' and ox1p='X' and ox2p='X'")
for row in o:
    ovdescrip=row[0]
    ovbodytime=str(-row[1])
    ovpnttime=str(-row[2])
    c.execute("INSERT INTO elines(description, hrs, pnthrs, lboper, elnum) VALUE ('"+ovdescrip+"','"+ovbodytime+"','"+ovpnttime+"','"+ovoperation+"','"+westnum+"')")
    conn.commit()

o.execute("SELECT odescription, obodolap, opntolap, occolap FROM m3overlap WHERE ox1b='X' and ox2b='X' and ox1p=' ' and ox2p=' '")
for row in o:
    ovdescrip=row[0]
    ovbodytime=str(-row[1])
    c.execute("INSERT INTO elines(description, hrs, lboper, elnum) VALUE ('"+ovdescrip+"','"+ovbodytime+"','"+ovoperation+"','"+westnum+"')")
    conn.commit()
o.execute("SELECT odescription, obodolap, opntolap, occolap FROM m3overlap WHERE ox1b=' ' and ox2b=' ' and ox1p='X' and ox2p='X'")
for row in o:
    ovdescrip=row[0]
    ovpnttime=str(-row[2])
    c.execute("INSERT INTO elines(description, pnthrs, lboper, elnum) VALUE ('"+ovdescrip+"','"+ovpnttime+"','"+ovoperation+"','"+westnum+"')")
    conn.commit()

olap.close()    
conn.close()

eh1 = mysql.connector.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DB)
eh = eh1.cursor()
eh.execute("SELECT epntrate, emecrate, ebodrate, efrarate , estrrate , eglarate , edetrate, eothrate, etaxrate FROM ehead WHERE estnum=" + westnum)
   # Fetch all the rows in a list of lists.
results = eh.fetchall()
for row in results:
    epntrate = row[0]
    if epntrate is None :
	    epntrate = 0
emecrate = row[1]
if emecrate is None :
	    emecrate = 0
ebodrate = row[2]
if ebodrate is None :
	    ebodrate = 0
efrarate = row[3]
if efrarate is None :
	    efrarate = 0
estrrate = row[4]
if estrrate is None :
	    estrrate = 0
eglarate = row[5]
if eglarate is None :
	    eglarate = 0
edetrate = row[6]
if edetrate is None :
	    edetrate = 0
eothrate = row[7]
if eothrate is None :
	    eothrate = 0
etaxrate = row[8]
if etaxrate is None :
	    etaxrate = 0

eh1.close()    
#print  (epntrate, emecrate, ebodrate, efrarate , estrrate , eglarate , edetrate, eothrate)

eetlpnt = pnthrstotal*float(epntrate)
eetlbod = bodyhrstotal*float(ebodrate)
eetlmec = mechhrstotal*float(emecrate)
eetlfra = framehrstotal*float(efrarate)
eetlstr = structhrstotal*float(estrrate)
eetlgla = glasshrstotal*float(eglarate)
eetldet = detailhrstotal*float(edetrate)
eetloth = otherhrstotal*float(eothrate)

#print  (eetlpnt, eetlbod, eetlmec, eetlfra, eetlstr, eetlgla,eetldet,eetloth )
tetitems=partitemtotal+pmatitemtotal+bmatitemtotal+hazitemtotal+subletitemtotal+afteritemtotal+towingitemtotal+storageitemtotal+misc1itemtotal+misc2itemtotal+misc3itemtotal
tetlabor=eetlpnt+eetlbod+eetlmec+eetlfra+eetlstr+eetlgla+eetldet+eetloth

tethrslabor=pnthrstotal+bodyhrstotal+mechhrstotal+framehrstotal+structhrstotal+glasshrstotal+detailhrstotal+otherhrstotal

tetsubtotal=float(tetitems)+tetlabor
tetax = float(tetitems)*float(etaxrate/100)
tetgtotal = float(tetitems)+tetlabor+float(tetax)

conn = mysql.connector.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DB)
c = conn.cursor()

c.execute("UPDATE ehead SET \
    etpnthrs = " + str(pnthrstotal) + ", \
    etbodhrs = " + str(bodyhrstotal) + ", \
    etmechrs = " + str(mechhrstotal) + ", \
    etfrahrs = " + str(framehrstotal) + ", \
    etstrhrs = " + str(structhrstotal) + ", \
    etglahrs = " + str(glasshrstotal) + ", \
    etdethrs = " + str(detailhrstotal) + ", \
    etothhrs = " + str(otherhrstotal) + ", \
    etlpnt = " + str(eetlpnt) + ", \
    etlbod = " + str(eetlbod) + ", \
    etlmec = " + str(eetlmec) + ", \
    etlfra = " + str(eetlfra) + ", \
    etlstr = " + str(eetlstr) + ", \
    etlgla = " + str(eetlgla) + ", \
    etldet = " + str(eetldet) + ", \
    etloth = " + str(eetloth) + ", \
    etparts = " + str(partitemtotal) + ", \
    etpmat = " + str(pmatitemtotal) + ", \
    etbmat = " + str(bmatitemtotal) + ", \
    ethaz = " + str(hazitemtotal) + ", \
    etsublet = " + str(subletitemtotal) + ", \
    etafter = " + str(afteritemtotal) + ", \
    ettowing = " + str(towingitemtotal) + ", \
    etstorage = " + str(storageitemtotal) + ", \
    etmisc1 = " + str(misc1itemtotal) + ", \
    etmisc2 = " + str(misc2itemtotal) + ", \
    etmisc3 = " + str(misc3itemtotal) + ", \
    etlabor = " + str(tetlabor) + ", \
    etitems = " + str(tetitems) + ", \
    etlsubtotal = " + str(tetsubtotal) + ", \
    etax = " + str(tetax) + ", \
    etgtotal = " + str(tetgtotal) + " \
    WHERE estnum=" + westnum)

conn.commit()
conn.close()

