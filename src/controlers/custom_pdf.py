# Author: Keveen Rodriguez Zapata <keveenrodriguez@gmail.com>
#
# License: GNU Lesser General Public License v3.0 (LGPLv3)
from fpdf import FPDF


class CustomPDF(FPDF):
    def header(self):
        # Set up a logo
        # self.image('snakehead.jpg', 10, 8, 33)
        self.set_font('Arial', 'B', 15)
        
        # Add an address
        self.cell(100)
        self.cell(0, 5, 'Nebula', ln = 1)
        self.cell(100)
        self.cell(0, 5, 'Report created by Nebula', ln = 1)
        self.cell(100)
        self.cell(0, 5, 'GRUNECO', ln = 1)
        self.cell(100)
        
        # Line break
        self.ln(20)
    
    def footer(self):
        self.set_y(-10)
        
        self.set_font('Arial', 'I', 8)
        
        # Add a page number
        page = 'Page ' + str(self.page_no()) + '/{nb}'
        self.cell(0, 10, page, 0, 0, 'C')
