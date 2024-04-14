from time import strftime
from datetime import datetime
import matplotlib.pyplot as plt
import pandas
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.pdfencrypt import StandardEncryption
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Image, Table, Paragraph, Spacer, PageBreak
from reportlab.platypus.tableofcontents import TableOfContents

PRIMARY_PALETTE = ['#0012bf', '#002ed0', '#003adb', '#1446e8', '#1b4ff3', '#4e6bf7', '#7488fa', '#9faafb', '#c7cbfc',
                   '#e9ebfe']
SECONDARY_PALETTE = ['#f26600', '#f28600', '#f29700', '#f2a900', '#f2b700', '#f3c11b', '#f5cd47', '#f8da7d', '#fbe8b0',
                     '#fdf7e0']
ACCENT = '#f31b4d'


def hex_to_rgb(hex_color) -> list:
    """Convert hexadecimal color code to 8-bit RGB values."""
    # Remove '#' if present
    hex_color = hex_color.lstrip('#')
    # Convert hexadecimal to RGB
    rgb = list(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    rgb = [x / 255 for x in rgb]
    return rgb


class ReportService:
    def __init__(self):
        self.employee_id: str = ""
        self.employee_phone: str = ""
        self.employee_email: str = ""
        self.employee_zip: str = ""
        self.employee_city: str = ""
        self.employee_street: str = ""
        self.employee_name: str = ""
        self.company_phone: str = ""
        self.company_email: str = ""
        self.company_zip: str = "None"
        self.company_city: str = ""
        self.company_street: str = ""
        self.company_name: str = ""
        self.actual_overtime: float = 0.0
        self.author: str = ""
        self.cumu = 'temp/Häufigkeitsverteilung.png'
        self.database_name = 'timecapturing.db'
        self.dataframe_holidays: pandas.DataFrame = pandas.DataFrame()
        self.dataframe_projects: pandas.DataFrame = pandas.DataFrame()
        self.dataframe_public_holidays: pandas.DataFrame = pandas.DataFrame()
        self.dataframe_sickleave: pandas.DataFrame = pandas.DataFrame()
        self.dataframe_worktimelog: pandas.DataFrame = pandas.DataFrame()
        self.holiday_contract: float = 0.0
        self.holiday_used: float = 0.0
        self.hours_daily: float = 0.0
        self.hours_weekly: float = 0.0
        self.document: ReportTemplate = None
        self.document_elements = []
        self.imagefile_project_bubbles = 'temp/ProjektzeitenBubble.png'
        self.imagefile_project_gradientbubbles = "temp/bubbles.png"
        self.imagefile_project_pie = 'temp/Projektzeiten.png'
        self.imagefile_worktime = 'temp/Arbeitszeitverlauf.png'
        self.language_code: str = "de_DE"
        self.overtime = 'temp/Überstundenverlauf.png'
        self.pdf_file = 'temp/report.pdf'
        self.sick_leave: float = 0.0
        self.table_styles = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(PRIMARY_PALETTE[2])),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor(PRIMARY_PALETTE[1])),
        ]
        self.text_styles = {
            'Title': ParagraphStyle(
                name='Title',
                fontSize=18,
                leading=22,
                textColor=PRIMARY_PALETTE[0],
                alignment=1  # Center alignment
            ),
            'Normal': ParagraphStyle(
                name='Normal',
                fontSize=12,
                leading=14,
                textColor='black'
            ),
            'Heading1': ParagraphStyle(
                name='Heading1',
                fontSize=16,
                leading=18,
                textColor=PRIMARY_PALETTE[0],
                spaceBefore=12,
                spaceAfter=6
            ),
            'Heading4': ParagraphStyle(
                name='Heading1',
                fontSize=12,
                leading=18,
                textColor=PRIMARY_PALETTE[0],
                spaceBefore=12,
                spaceAfter=6
            ),
        }
        self.year = strftime('%Y')

    def build_document(self):
        self.generate_plots()
        self._create_document()
        self._create_title()
        self._create_intro()
        self._create_toc()
        self._create_summary()
        self._create_worktime_plot()
        self._create_overtime_plot()
        self._create_project_plot()
        self._create_worktime_probability_plot()
        self._create_details_holidays()
        self._create_details_public_holidays()
        self._create_details_sickleave()
        self._create_details_worktime()
        self._encrypt_document()
        self.document.multiBuild(self.document_elements)

    def generate_plots(self):
        self._generate_worktime_figure()

    def set_data(self, holidays: pandas.DataFrame, projects: pandas.DataFrame, public_holidays: pandas.DataFrame,
                 sick_leave: pandas.DataFrame,
                 worktimelog: pandas.DataFrame) -> None:
        self.dataframe_holidays = holidays
        self.dataframe_projects = projects
        self.dataframe_public_holidays = public_holidays
        self.dataframe_sickleave = sick_leave
        self.dataframe_worktimelog = worktimelog

    def set_parameters(self, actual_overtime: float, author: str, company_name: str, company_street: str,
                       company_city: str, company_zip: str, company_email: str, company_phone: str, employee_name: str,
                       employee_street: str, employee_city: str, employee_zip: str, employee_email: str,
                       employee_phone: str, employee_id: str, holiday_contract: float, holiday_used: float,
                       hours_daily: float, hours_weekly: float, pdf_file: str, sick_leave: float, year: str, ) -> None:
        """
        Set parameters for the report.
        :param employee_id: HR-ID of the employee.
        :param employee_phone: phone number of the employee.
        :param employee_email: email address of the employee.
        :param employee_zip: zip code of the employee.
        :param employee_city: city name of the employee.
        :param employee_street: street name of the employee.
        :param company_phone: phone number of the company.
        :param company_email: mail address of the company.
        :param company_zip: zip code of the company.
        :param company_city: city name of the company.
        :param company_street: street name and house number of the company.
        :param employee_name: name of the employee.
        :param actual_overtime: Actual overtime in hours.
        :param author: Name of the person for whom the report is created.
        :param company_name: Name of the company.
        :param holiday_contract: Number of holiday days according to the contract.
        :param holiday_used: Number of holiday days used.
        :param hours_daily: Daily working hours.
        :param hours_weekly: Weekly working hours.
        :param pdf_file: File name of the PDF report.
        :param sick_leave: Number of sick days.
        :param year: The year for which the report is created.
        :return: None
        """
        self.actual_overtime = actual_overtime
        self.author = author
        self.company_name = company_name
        self.company_street = company_street
        self.company_city = company_city
        self.company_zip = company_zip
        self.company_email = company_email
        self.company_phone = company_phone
        self.employee_name = employee_name
        self.employee_street = employee_street
        self.employee_city = employee_city
        self.employee_zip = employee_zip
        self.employee_email = employee_email
        self.employee_phone = employee_phone
        self.employee_id = employee_id
        self.holiday_contract = holiday_contract
        self.holiday_used = holiday_used
        self.hours_daily = hours_daily
        self.hours_weekly = hours_weekly
        self.pdf_file = pdf_file
        self.sick_leave = sick_leave
        self.year = year

    def _create_details_holidays(self):
        self.document_elements.append(Paragraph("Genommene Urlaubstage, Details", self.text_styles['Heading1']))
        self.document_elements.append(Spacer(A4[0], 5))
        data = ([list(row) for row in self.dataframe_holidays.values])
        data.insert(0, ['Tag', """Verrechnete\nStunden"""])
        vac = Table(data=data, colWidths=100, rowHeights=[40].append([20] * len(self.dataframe_holidays)), repeatRows=1)
        vac.setStyle(self.table_styles)
        self.document_elements.append(vac)
        self.document_elements.append(Spacer(A4[0], 20))

    def _create_details_public_holidays(self):
        self.document_elements.append(Paragraph("Berücksichtigte gesetzliche Feiertage", self.text_styles['Heading1']))
        self.document_elements.append(Spacer(A4[0], 5))
        data = ([list(row) for row in self.dataframe_public_holidays.values])
        data.insert(0, ['Tag', """Verrechnete\nStunden""", "Wochentag", "Feiertag"])
        ho = Table(data=data, colWidths=[80, 80, 80, 120],
                   rowHeights=[40].append([20] * len(self.dataframe_public_holidays)), repeatRows=1)
        ho.setStyle(self.table_styles)
        self.document_elements.append(ho)
        self.document_elements.append(Spacer(A4[0], 20))

    def _create_details_sickleave(self):
        # Show details of sick days
        self.document_elements.append(Paragraph("Krankentage, Details", self.text_styles['Heading1']))
        self.document_elements.append(Spacer(A4[0], 5))
        if self.dataframe_sickleave.shape[0] > 0:
            data = ([list(row) for row in self.dataframe_sickleave.values])
            data.insert(0, ['Tag', """Verrechnete\nStunden"""])
            si = Table(data=data, colWidths=100, rowHeights=[40].append([20] * len(self.dataframe_sickleave)),
                       repeatRows=1)
            si.setStyle(self.table_styles)
            self.document_elements.append(si)
        else:
            self.document_elements.append(Paragraph("Keine Krankentage", self.text_styles['Normal']))
        self.document_elements.append(Spacer(A4[0], 20))

    def _create_details_worktime(self):
        self.document_elements.append(Paragraph("Arbeitszeiten, Details", self.text_styles['Heading1']))
        self.document_elements.append(Spacer(A4[0], 5))
        data = ([list(row) for row in self.dataframe_worktimelog.values])
        data.insert(0, list(self.dataframe_worktimelog.columns))
        wtl = Table(data=data, colWidths=[80, 80, 80, 160, 80],
                    rowHeights=[40].append([20] * len(self.dataframe_worktimelog)), repeatRows=1)
        wtl.setStyle(self.table_styles)
        self.document_elements.append(wtl)
        self.document_elements.append(Spacer(A4[0], 20))

    def _create_document(self):
        self.document = ReportTemplate(
            self.pdf_file,
            pagesize=A4,
            title=f"Arbeitszeitbericht {strftime('%Y')} - {self.author}",
            author=self.author,
            language=self.language_code,
            tagget=1
        )

    def _create_intro(self):
        intro = Paragraph(f"""Dieses Dokument enthält den Arbeitszeitbericht für das Jahr {strftime('%Y')}\n 
                          Daten wurden auf Grundlage der Datei '{self.database_name}' erhoben.\n
                          Die Auswertung und das Erstellen dieses Dokuments erfolgt maschinell und wird daher nicht unterschrieben.\n\n
                          """, getSampleStyleSheet()['Normal'])
        self.document_elements.append(intro)
        date = Paragraph(f"Datum der Erstellung: \t {strftime('%d.%m.%Y')}""", self.text_styles['Heading4'])
        self.document_elements.append(date)
        self.document_elements.append(Spacer(A4[0], 5))

    def _create_overtime_plot(self):
        self.document_elements.append(Paragraph("Überstundenverlauf", self.text_styles['Heading1']))
        self.document_elements.append(Spacer(A4[0], 5))
        ot = Image(self.overtime, width=A4[0], height=A4[0] * 10 / 20)
        self.document_elements.append(ot)
        self.document_elements.append(PageBreak())

    def _create_project_plot(self):
        self.document_elements.append(Paragraph("Projektzeiten", self.text_styles['Heading1']))
        pr = Image(self.imagefile_project_pie, width=A4[0], height=A4[0])
        self.document_elements.append(pr)
        self.document_elements.append(Spacer(A4[0], 20))

        prb = Image(self.imagefile_project_bubbles, width=A4[0], height=A4[0] / 1.5)
        self.document_elements.append(prb)
        self.document_elements.append(Spacer(A4[0], 20))

        prb2 = Image(self.imagefile_project_gradientbubbles, width=A4[0], height=A4[0])
        self.document_elements.append(prb2)
        self.document_elements.append(Spacer(A4[0], 20))
        self.document_elements.append(Spacer(A4[0], 5))
        data = ([list(row) for row in self.dataframe_projects.values])
        data.insert(0, ['Projekt', "Projektstunden"])
        pr = Table(data=data, colWidths=[160, 100], rowHeights=[40].append([20] * len(self.dataframe_projects)),
                   repeatRows=1)
        pr.setStyle(self.table_styles)
        self.document_elements.append(pr)
        self.document_elements.append(PageBreak())

    def _create_summary(self):
        # adding summary table and break page
        self.document_elements.append(Paragraph("Zusammenfassung", self.text_styles['Heading1']))
        self.document_elements.append(Spacer(A4[0], 5))
        short = Table(data=[
            ['Firma', f""" {self.company_name}\n Hauptstraße 29\n DE 02794 Spitzkunnersdorf"""],
            ['Name', "Lennart Schink"],
            ['Soll-Arbeitszeit (wöchentlich)', str(self.hours_weekly) + 'h'],
            ['Soll-Arbeitszeit (täglich)', str(self.hours_daily) + 'h'],
            ['Aktuelle Mehrarbeit', str(self.actual_overtime) + 'h'],
            ['vertragl. Urlaubstage', str(self.holiday_contract) + 'd'],
            ['genommene Urlaubstage', str(self.holiday_used) + 'd'],
            ['freie Urlaubstage', str(self.holiday_contract - self.holiday_used) + 'd'],
            ['Krankentage', str(self.sick_leave) + 'd']],
            colWidths=[150, 250], rowHeights=[45, 20, 20, 20, 20, 20, 20, 20, 20])
        short.setStyle([
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('FONTNAME', (0, 0), (-1, 2), 'Helvetica-Bold'),
            ('FONTNAME', (0, 4), (-1, 4), 'Helvetica-Bold'),
            ('FONTNAME', (0, 7), (-1, 7), 'Helvetica-Bold'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (1, 0), (-1, -1), colors.white),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor(PRIMARY_PALETTE[-2])),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor(PRIMARY_PALETTE[1]))
        ])
        self.document_elements.append(short)
        self.document_elements.append(PageBreak())

    def _create_title(self):
        title = Paragraph(f"Arbeitszeitbericht {self.year} - Lennart Schink", self.text_styles['Title'])
        self.document_elements.append(title)
        self.document_elements.append(Spacer(A4[0], 5))

    def _create_toc(self):
        toc = TableOfContents()
        self.document_elements.append(Paragraph("Inhaltsverzeichnis", self.text_styles['Heading1']))
        self.document_elements.append(toc)
        self.document_elements.append(Spacer(A4[0], 15))

    def _create_worktime_plot(self):
        self.document_elements.append(Paragraph("Arbeitszeitverlauf", self.text_styles['Heading1']))
        self.document_elements.append(Spacer(A4[0], 5))
        wt = Image(self.imagefile_worktime, width=A4[0], height=A4[0] * 10 / 20)
        self.document_elements.append(wt)
        self.document_elements.append(Spacer(A4[0], 5))

    def _create_worktime_probability_plot(self):
        cum = Image(self.cumu, width=A4[0], height=A4[0])
        self.document_elements.append(cum)

    def _encrypt_document(self):
        self.document.encrypt = StandardEncryption(
            "1234",
            canPrint=0,
            canModify=0,
            canCopy=0,
            canAnnotate=0,
            strength=40,
            ownerPassword="12345"
        )

    def _generate_worktime_figure(self):
        if self.year == datetime.now().strftime('%Y'):
            actual_KW = datetime.now().isocalendar()[1]
        else:
            actual_KW = None
        last_week_of_year = datetime.strptime(f"{self.year}-12-31", "%Y-%m-%d").isocalendar()[1]
        weeklist = list(range(1, last_week_of_year + 1))
        weeklist = pd.DataFrame(weeklist, columns=["KW"])
        self.dataframe_worktimelog["Tag"] = pandas.to_datetime(self.dataframe_worktimelog["Tag"])
        self.dataframe_worktimelog["KW"] = self.dataframe_worktimelog["Tag"].dt.isocalendar().week


        daily = self.dataframe_worktimelog.groupby("Tag").sum()
        weeklist["Dauer"] = 0 #initialize duration column with 0
        weeklist["Urlaub"] = 0 #initialize holiday column with 0
        weeklist["Feiertag"] = 0 #initialize public holiday column with 0
        weeklist["Krank"] = 0 #initialize sick leave column with 0
        self.dataframe_holidays["Tag"] = pandas.to_datetime(self.dataframe_holidays["Tag"])
        self.dataframe_holidays["KW"] = self.dataframe_holidays["Tag"].dt.isocalendar().week
        self.dataframe_public_holidays["Tag"] = pandas.to_datetime(self.dataframe_public_holidays["Tag"])
        self.dataframe_public_holidays["KW"] = self.dataframe_public_holidays["Tag"].dt.isocalendar().week
        self.dataframe_sickleave["Tag"] = pandas.to_datetime(self.dataframe_sickleave["Tag"])
        self.dataframe_sickleave["KW"] = self.dataframe_sickleave["Tag"].dt.isocalendar().week
        for idx, row in weeklist.iterrows():
            if row["KW"] in self.dataframe_holidays["KW"].values:
                weeklist.at[idx, "Urlaub"] = self.dataframe_holidays[self.dataframe_holidays["KW"] == row["KW"]]["Angerechnete Stunden"].sum()
            if row["KW"] in self.dataframe_public_holidays["KW"].values:
                weeklist.at[idx, "Feiertag"] = self.dataframe_public_holidays[self.dataframe_public_holidays["KW"] == row["KW"]]["Angerechnete Stunden"].sum()
            if row["KW"] in self.dataframe_sickleave["KW"].values:
                weeklist.at[idx, "Krank"] = self.dataframe_sickleave[self.dataframe_sickleave["KW"] == row["KW"]]["Angerechnete Stunden"].sum()
            if row["KW"] in daily["KW"].values:
                weeklist.at[idx, "Dauer"] = daily[daily["KW"] == row["KW"]]["Dauer"].sum()
        weeklist["Gesamt"] = weeklist["Dauer"] + weeklist["Urlaub"] + weeklist["Feiertag"] + weeklist["Krank"]
        fig, ax = plt.subplots(figsize=(20, 10), )
        bar1 = ax.bar(weeklist["KW"], weeklist["Gesamt"],
                      label="Ist-Wochenstunden inkl. Urlaub, Feiertag und Krank", color=PRIMARY_PALETTE[2])
        bar2 = ax.bar(weeklist["KW"], weeklist["Dauer"], label="Ist-Wochenstunden",
                      color=SECONDARY_PALETTE[2])
        ax.axhline(y=self.hours_weekly, color=ACCENT, linestyle='--', label='Soll-Wochenstunden')
        ax.axhline(y=self.hours_weekly / 5, color=ACCENT, linestyle='--', linewidth=0.5)
        ax.axhline(y=self.hours_weekly * 2 / 5, color=ACCENT, linestyle='--', linewidth=0.5)
        ax.axhline(y=self.hours_weekly * 3 / 5, color=ACCENT, linestyle='--', linewidth=0.5)
        ax.axhline(y=self.hours_weekly * 4 / 5, color=ACCENT, linestyle='--', linewidth=0.5)
        if actual_KW is not None:
            ax.axvline(x=actual_KW, linestyle='-', linewidth=5, label='Aktuelle Kalenderwoche', color=ACCENT)
        ax.spines['top'].set_color(PRIMARY_PALETTE[0])
        ax.spines['bottom'].set_color(PRIMARY_PALETTE[0])
        ax.spines['left'].set_color(PRIMARY_PALETTE[0])
        ax.spines['right'].set_color(PRIMARY_PALETTE[0])
        ax.set_title("Arbeitszeit je Kalenderwoche", color=PRIMARY_PALETTE[0])
        ax.set_xlabel("Kalenderwoche", color=PRIMARY_PALETTE[0])
        ax.set_xticks(weeklist["KW"])
        ax.set_xticklabels(weeklist["KW"], color=PRIMARY_PALETTE[0])
        ax.set_ylabel("Arbeitszeit [h]", color=PRIMARY_PALETTE[0])
        ax.set_yticks(ax.get_yticks())
        ax.set_yticklabels(ax.get_yticks(), color=PRIMARY_PALETTE[0])
        ax.legend(labelcolor=PRIMARY_PALETTE[0])
        fig.tight_layout()
        plt.savefig(self.imagefile_worktime, transparent=True)

class ReportTemplate(BaseDocTemplate):
    def __init__(self, filename, **kw):
        self.allowSplitting = 0
        BaseDocTemplate.__init__(self, filename, **kw)
        template = [PageTemplate('normal', [
            Frame(x1=2.5 * cm, y1=3 * cm, width=17 * cm, height=25 * cm, id='F1', showBoundary=0)], onPage=self.footer)]
        self.addPageTemplates(template)

    def afterFlowable(self, flowable):
        "Registers TOC entries and adds hyperlinks to TOC entries."
        if flowable.__class__.__name__ == 'Paragraph':
            text = flowable.getPlainText()
            style = flowable.style.name
            if style.startswith('Heading'):
                # Add a destination (anchor) name based on the text
                anchor_name = text.replace(' ', '_')
                self.canv.bookmarkPage(anchor_name)
                # Add a hyperlink to the TOC entry
                self.notify('TOCEntry', (0, text, self.page, anchor_name))

    def footer(self, canvas: canvas, doc):
        """Add page number to footer."""
        canvas.saveState()
        pageNumber = canvas.getPageNumber()
        canvas.setFont('Helvetica', 9)
        canvas.setFillColorRGB(*hex_to_rgb(PRIMARY_PALETTE[0]))
        canvas.drawString(doc.leftMargin, 1.5 * cm, "Seite %s" % pageNumber)
        canvas.restoreState()
