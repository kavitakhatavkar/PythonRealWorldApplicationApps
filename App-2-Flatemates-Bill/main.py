from filestack import Client
from fpdf import FPDF
import os


class Bill:
    """
    Object that contains data about a bill, such as
    total amount and period of the bill.
    """

    def __init__(self, amount, period):
        self.amount = amount
        self.period = period


class Flatmate:
    """
    Create a flatmate person who lives in the flat
    and pays a share of the bill.
    """

    def __init__(self, name, days_in_house):
        self.name = name
        self.days_in_house = days_in_house

    def pays(self, bill, flatmate2):
        weight = self.days_in_house / (self.days_in_house + flatmate2.days_in_house)
        to_pay = bill.amount * weight
        return round(to_pay, 2)


class PdfReport:
    """
    Creates a PDF file that contains data about
    the flatmates such as their names, their due amount
    and the period of the bill.
    """

    def __init__(self, filename):
        self.filename = filename

    def generate(self, flatmate1, flatmate2, bill):
        pdf = FPDF(orientation='P', unit='pt', format='A4')
        pdf.add_page()

        # Insert and Style title
        pdf.set_font(family='Courier', size=25, style='B')
        pdf.cell(w=540, h=60, txt='Flatmates Bill Invoice', border=1, align='C', ln=1)

        # Add column names
        pdf.set_font(family='Courier', size=15, style='B')
        pdf.cell(w=135, h=48, txt='Name', border=1, align='C')
        pdf.cell(w=135, h=48, txt='Days in house', border=1, align='C')
        pdf.cell(w=135, h=48, txt='Period', border=1, align='C')
        pdf.cell(w=135, h=48, txt='Rent($)', border=1, ln=1, align='C')

        pdf.set_font(family='Courier', size=15)
        pdf.cell(w=135, h=38, txt=flatmate1.name, border=1, align='C')
        pdf.cell(w=135, h=38, txt=str(flatmate1.days_in_house), border=1, align='C')
        pdf.cell(w=135, h=38, txt=monthly_bill.period, border=1, align='C')
        pdf.cell(w=135, h=38, txt=str(flatmate1.pays(bill, flatmate2)), border=1, ln=1, align='C')

        pdf.cell(w=135, h=38, txt=flatmate2.name, border=1, align='C')
        pdf.cell(w=135, h=38, txt=str(flatmate2.days_in_house), border=1, align='C')
        pdf.cell(w=135, h=38, txt=monthly_bill.period, border=1, align='C')
        pdf.cell(w=135, h=38, txt=str(flatmate2.pays(bill, flatmate1)), border=1, align='C')

        # Change directory to "files", generate and open the PDF
        os.chdir("files")
        pdf.output(self.filename)


class FileSharer:

    def __init__(self, filepath, api_key="Ay9A51nluQ0qxiq8MdhxPz"):
        self.api_key = api_key
        self.filepath = filepath

    def share(self):
        client = Client(self.api_key)

        new_filelink = client.upload(filepath=self.filepath)
        return new_filelink.url


if __name__ == '__main__':
    # taking input from the user
    user_amount = float(input('Enter bill amount: '))
    user_period = input('Enter period: ')
    name1 = input('Enter flatmate1 name: ')
    days_in_house1 = int(input(f'How many days did {name1} stay in? '))
    name2 = input('Enter flatmate2 name: ')
    days_in_house2 = int(input(f'How many days did {name2} stay in? '))

    monthly_bill = Bill(user_amount, user_period)
    flatmate_obj1 = Flatmate(name1, days_in_house1)
    flatmate_obj2 = Flatmate(name2, days_in_house2)

    print(f'{flatmate_obj1.name} pays: ', flatmate_obj1.pays(monthly_bill, flatmate_obj2))
    print(f'{flatmate_obj2.name} pays: ', flatmate_obj2.pays(monthly_bill, flatmate_obj1))

    pdf_report = PdfReport(filename=f'{monthly_bill.period}.pdf')
    pdf_report.generate(flatmate_obj1, flatmate_obj2, monthly_bill)

    file_sharer = FileSharer(filepath=pdf_report.filename)
    print(file_sharer.share())
