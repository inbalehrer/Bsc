from fpdf import FPDF
from Discovery import Types
from Report import Report_analysis as report

width = 210
height = 297

if __name__ == "__main__":
    '''
    Add the summary of each project mining section to a pdf 
    '''
    pdf = FPDF()
    pdf.set_font('Arial', "", 9)
    analysis = report.get_analysis()

    for a in analysis.keys():
        pdf.add_page()
        pdf.cell(0, 10, a, ln=True, border=True, align='C')  # Single line
        pdf.set_font('Arial', "B", 9)
        for att in analysis[a]:
            pdf.cell(0, 10, att, ln=True)
            pdf.set_font('Arial', "", 9)
            text = f"{analysis[a][att]}"
            pdf.multi_cell(0, 10, text)  # Multi line

    pdf.output("../Report/Report_final.pdf")