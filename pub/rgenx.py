#! /usr/local/lib/python3.10
import pathlib

import sys
import mysql.connector
import db_variables 
import pymysql.cursors
import pymysql

from tabulate import tabulate
from db_variables import *
from datetime import datetime
from fpdf import FPDF  #pip install fpdf2 ... note !  TWO
from random import random
from env_rule import *

from db_connection_utils import get_head_data
from db_connection_utils import get_line_data

westnum = sys.argv[1]

# Get Data from DB
ehead_data = get_head_data(westnum)
eline_data = get_line_data(westnum)

# rows_in_elemnts_list = 5  # Put the quantity of rows, that we'll receive in our report

rows_in_elemnts_list = len(eline_data)

class Customizer(FPDF):
    def header(self):
        if self.page_no() != 1:
            self.set_font('helvetica', size=7)
            self.set_xy(2, 2)
            self.cell(15, 6, 'ESTIMATE. #')

            self.set_font('helvetica', 'B', 12)
            self.cell(20, 6, f'{ehead_data["estnum"]}')

            self.set_font('helvetica', size=7)
            self.cell(8, 6, 'NAME:')

            self.set_font('helvetica', 'B', 12)
            self.cell(
                20, 6, f'{ehead_data["fname"]}, {ehead_data["lname"]}')

            self.ln(10)

current_date = datetime.now()
dateFormat = current_date.strftime('%d-%m-%Y-d%H-%M')
custom_header = f'ESTIMATE..  # {ehead_data["estnum"]} Name: {ehead_data["fname"]}, {ehead_data["lname"]}'

pdf = Customizer()

# Initializing
pdf.alias_nb_pages()
pdf.add_page()

pdf.set_margins(5, 10, 5)
pdf.set_auto_page_break(auto=True, margin=5)

# LOGO
# pdf.image('/Users/vladimirkuzin/StuProj/Vlad3ServREST/pub/images/tesla_logo.png', 95, 5, 20) #MB_Air path
# pdf.image('/Users/vladimir/StuTeslaProj/StuSecretEstimate/pub/images/tesla_logo.png', 95, 5, 20) # MB_Pro path
pdf.image(f'{path_to_logo}/tesla_logo.png', 95, 5, 20) # Docker path


pdf.set_xy(55, 25)

# Company Name
pdf.set_font('helvetica', 'B', 22)
pdf.multi_cell(100, 10, align='C', txt='TESLA')
pdf.set_xy(55, 35)
pdf.set_font('helvetica', size=10)
pdf.multi_cell(100, 5, align='C',
            txt='4321 Blast Off Way\nElectric City, TX 98765\nPh: 800-fix-tesla\nEmail: fixtesla@tesla.com')

# Order No, Client Name, Car Model
pdf.set_font('helvetica', 'B', size=12)
pdf.set_xy(10, 68)
pdf.multi_cell(
    50, 5, f'Estimate... # {ehead_data["estnum"]}\n{ehead_data["fname"]}, {ehead_data["lname"]}')
pdf.set_xy(100, 68)
pdf.cell(50, 6, f'{ehead_data["model"]}')


# Client Info
pdf.set_xy(10, 80)
pdf.set_font('helvetica', size=8)
pdf.multi_cell(30, 5, f'Last\nFirst\nCell Ph.\nOther Ph\nEmail\nCNOTES')
pdf.set_xy(70, 80)
pdf.multi_cell(30, 5, f'Model\nVIN #\nLicense\nColor\nYear\nStyle')
pdf.set_xy(140, 80)
pdf.multi_cell(30, 5, f'Insurance\nClaim\nPolicy\nAdjuster\nPhone\nEmail')

# Client Data (Info Part)
pdf.set_xy(26, 80)
pdf.set_font('helvetica', 'B', size=8)
pdf.multi_cell(
    50, 5, f'{ehead_data["lname"]}\n{ehead_data["fname"]}\n{ehead_data["cellph"]}\n{ehead_data["oth"]}\n{ehead_data["cemail"]}\n{ehead_data["cnotes"]}')  # 7 values
pdf.set_xy(90, 80)
pdf.multi_cell(
    50, 5, f'{ehead_data["model"]}\n{ehead_data["vin"]} #\n{ehead_data["lic"]}\n{ehead_data["color"]}\n{ehead_data["year"]}\n{ehead_data["style"]}')  # 9 values
pdf.set_xy(160, 80)
pdf.multi_cell(
    50, 5, f'{ehead_data["insco"]}\n{ehead_data["claimnum"]}\n{ehead_data["policynum"]}\n{ehead_data["adjuster"]}\n{ehead_data["aphone"]}\n{ehead_data["aemail"]}')  # 9 values


# Separartor line
pdf.set_line_width(0.4)
pdf.line(0, 126, 210, 126)
# $, Hours, Labor, Paint
pdf.set_xy(145, 120)
pdf.multi_cell(46, 5, '$              Labor              Paint')

# ROWS LIST
pdf.set_xy(0, 126)
pdf.set_font('Courier', size=10)


def list_of_works(rows_quantity):
    for i in range(1, rows_quantity+1):
        pdf.set_x(5)
        pdf.cell(8, 6, f'{i}')  # Number
        pdf.cell(10, 6, 'RPS')  # CODE
        pdf.cell(130, 6, 'SOME TEXT THAT DESCRIBES THE ELEMENT AND IT\'S COST')
        pdf.cell(14, 6, str(round(random()*100, 2)))  # Hours
        pdf.cell(14, 6, str(round(random()*100, 2)))  # Labor
        pdf.cell(20, 6, str(round(random()*100, 2)))  # Paint
        pdf.ln(6)

def list_of_elines():

    conn = mysql.connector.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DB)
    c = conn.cursor()
    c.execute("SELECT lboper,description,partno,price,hrs,pnthrs FROM elines WHERE elnum="+westnum)
#    conn.commit()
    
#    print(f'test 1 ' + westnum + '<<<')

    linenum=0
    for erow in c:
        linenum=linenum+1
        pdf.set_x(5)
        pdf.cell(4, 6, str(linenum))  # $$$
        pdf.cell(10, 6, erow[0])  # Labor
        pdf.cell(70, 6, erow[1])  # Paint
        pdf.cell(50, 6, str(erow[2]))  # Paint
        pdf.cell(20, 6, str(erow[3]))  # Paint
        pdf.cell(20, 6, str(erow[4]))  # Paint
        pdf.cell(20, 6, str(erow[5]))  # Paint

#        print(f'test 2 ')

#        pdf.cell(20, 10, erow[0])  # $$$
#        pdf.cell(20, 136, erow[1])  # Labor
#        pdf.cell(20, 40, erow[2])  # Paint
#        pdf.cell(20, 12, str(erow[3]))  # Paint
#        pdf.cell(20, 12, str(erow[4]))  # Paint
#        pdf.cell(20, 12, str(erow[5]))  # Paint

        pdf.ln(6)

    conn.close()


def totalBlock(rows):
    if rows <= 10:
        pdf.set_xy(5, 185)
    elif rows >= 10 and rows <= 27:
        pdf.set_xy(5, 300)
    elif rows > 27 and rows <= 56:
        pdf.set_xy(5, pdf.get_y())
    elif rows > 56 and rows < 75:
        pdf.set_xy(5, 300)
    elif rows >= 75 and rows < 90:
        pdf.set_xy(5, pdf.get_y())

    # Labor, Units, Rate, Labor $, Item $, Totals
    pdf.set_xy(4, pdf.get_y()+10)
    pdf.set_font('Courier', size=8)
    pdf.cell(25, 5, ' LABOR')
    pdf.cell(20, 5, 'Units')
    pdf.cell(20, 5, '  Rate')
    pdf.cell(40, 5, '  Labor $')
    pdf.cell(60, 5, '  Item $')
    pdf.cell(30, 5, 'Totals')
    pdf.ln(6)

    # -------
    # Columns
    # Totals Table
    pdf.set_font('Courier', size=10)
    pdf.multi_cell(
        20, 5, 'Paint\nBody\nMech\nFrame\nStruct\nGlass\nDetail\nOther')

    pdf.set_xy(pdf.get_x() + 3, pdf.get_y() - 5 * 8)
    # Units
    pdf.multi_cell(
        30, 5, f'{ehead_data["etpnthrs"]}@\n{ehead_data["etbodhrs"]}@\n{ehead_data["etmechrs"]}@\n{ehead_data["etfrahrs"]}@\n{ehead_data["etstrhrs"]}@\n{ehead_data["etglahrs"]}@\n{ehead_data["etdethrs"]}@\n{ehead_data["etothhrs"]}@')
#        30, 5, f'{ehead_data["etpnthrs"]}@\n{ehead_data["etbodhrs"]}@\n{ehead_data["etmechrs"]}@\n{ehead_data["etfrahrs"]}@\n{ehead_data["etstrhrs"]}@\n{ehead_data["etglahrs"]}@\n{ehead_data["etdethrs"]}@\n{ehead_data["etothhrs"]}@')
    # Rate 
    pdf.set_xy(pdf.get_x() + 1, pdf.get_y() - 5 * 8)
    pdf.multi_cell(
        20, 5, f'{ehead_data["epntrate"]}\n{ehead_data["ebodrate"]}\n{ehead_data["emecrate"]}\n{ehead_data["efrarate"]}\n{ehead_data["estrrate"]}\n{ehead_data["eglarate"]}\n{ehead_data["edetrate"]}\n{ehead_data["eothrate"]}\n')
    # Labor $
    pdf.set_xy(pdf.get_x() + 1, pdf.get_y() - 5 * 8)
    pdf.multi_cell(
        20, 5, f'{ehead_data["etlpnt"]}\n{ehead_data["etlbod"]}\n{ehead_data["etlmec"]}\n{ehead_data["etlfra"]}\n{ehead_data["etlstr"]}\n{ehead_data["etlgla"]}\n{ehead_data["etldet"]}\n{ehead_data["etloth"]}')
    # Item Cost Colum Names
    pdf.set_xy(pdf.get_x() + 1, pdf.get_y() - 5 * 8)
    pdf.multi_cell(
        20, 5, 'Parts\nPaintMat\nBodyMat\nHazWaste\nSublet\nAft/Mkt\nTowing\nStorage\nMisc #1\nMisc #2\nMisc #3')
    # Item Cost $
    pdf.set_xy(pdf.get_x() + 1, pdf.get_y() - 5 * 12)
    pdf.multi_cell(
        20, 5, f'\n{ehead_data["etparts"]}\n{ehead_data["etpmat"]}\n{ehead_data["etbmat"]}\n{ehead_data["ethaz"]}\n{ehead_data["etsublet"]}\n{ehead_data["etafter"]}\n{ehead_data["ettowing"]}\n{ehead_data["etstorage"]}\n{ehead_data["etmisc1"]}\n{ehead_data["etmisc2"]}\n{ehead_data["etmisc3"]}')

    # TOTALS
    pdf.set_font('Courier', 'B', size=11)
    pdf.set_xy(pdf.get_x() + 1, pdf.get_y() + 10 - 5 * 12)
    pdf.multi_cell(
        30, 5, '  \nTotal Items\nTotal Labor\n\nSubtotal\n\nTax\n\nGrand Total')
    pdf.set_xy(pdf.get_x() + 1, pdf.get_y() + 20 - 5 * 12)
    pdf.multi_cell(
        30, 5, f'{ehead_data["etitems"]}\n{ehead_data["etlabor"]}\n\n{ehead_data["etlsubtotal"]}\n\n{ehead_data["etaxrate"]}\n\n{ehead_data["etgtotal"]}')

    pdf.set_line_width(0.6)  # Total lines
    pdf.line(170, pdf.get_y()-8, 200, pdf.get_y()-8)
    pdf.line(170, pdf.get_y()-30, 200, pdf.get_y()-30)

    pdf.set_line_width(0.8)  # Total Block Line
    pdf.line(0, pdf.get_y()+13, 200, pdf.get_y()+13)
    pdf.line(0, pdf.get_y()-56, 200, pdf.get_y()-56)
    pdf.set_line_width(0.5)
    pdf.line(0, pdf.get_y()-51, 200, pdf.get_y()-51)

    # Bottom Text Block
    # Warning Text
    pdf.set_xy(pdf.get_x(), pdf.get_y()+15)
    pdf.set_font('Courier', size=9)
    
    #pdf.multi_cell(5, 4, 'I authorize this Tesla repair facility to repair my vehicle with this estimate being the guide for said repairs.')
    #pdf.multi_cell(5, 4, 'I understand this is an estimate that and that there may be unanticipated exceptions to the estimate for additional')
    #pdf.multi_cell(5, 4, ' repair time, parts price increases, and additional parts.')

    # Sign holder
    #pdf.set_font('Courier', 'B', size=10)
    #pdf.multi_cell(20, 10, 'X')
    #pdf.set_line_width(0.4)
    #pdf.line(11, pdf.get_y()-3, 120, pdf.get_y()-3)

    # Output file
#list_of_works(rows_in_elemnts_list)
list_of_elines()
totalBlock(rows_in_elemnts_list) 
# pdf.output(f'/var/www/vhosts/teslaest.com/httpdocs/estimate_reports/EST_{ehead_data["estnum"]}.pdf') teslaestimate.com path
# pdf.output(f'/Users/vladimirkuzin/StuProj/Vlad3ServREST/pub/estimate_reports/EST_{ehead_data["estnum"]}.pdf') #MB_Air path
# pdf.output(f'/Users/vladimir/StuTeslaProj/StuSecretEstimate/pub/estimate_reports/EST_{ehead_data["estnum"]}.pdf') #MB_Pro path
pdf.output(f'{path_to_pdf}/EST_{ehead_data["estnum"]}.pdf') #MB_Pro path


print(f'Generating of the report is finished successfuly. Download it by below link on key ESTIMATE_PDF.')



