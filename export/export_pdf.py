from tkinter import filedialog, messagebox
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table,
    TableStyle, PageBreak
)
from reportlab.lib.units import inch
import io
from PIL import Image as PilImage

def export_pdf(cur):
    #  Get employee data
    cur.execute("SELECT photo, name, age, dob, sex, education_background, "
                "marital_status, blood_type, phone, email, address FROM employees")
    rows = cur.fetchall()

    filepath = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not filepath:
        return

    doc = SimpleDocTemplate(filepath, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    story = []

    # Custom styles
    title_style = ParagraphStyle('Title', fontSize=16, leading=20, spaceAfter=12, spaceBefore=12,
                                 textColor=colors.darkblue, alignment=1)
    label_style = ParagraphStyle('Label', fontSize=10, textColor=colors.HexColor('#333333'), leftIndent=6)
    value_style = ParagraphStyle('Value', fontSize=10, textColor=colors.HexColor('#000000'), leftIndent=12)
    header_style = ParagraphStyle('Header', fontSize=12, spaceAfter=6, textColor=colors.black, leading=15)

    for i, row in enumerate(rows):
        photo_data, name, age, dob, sex, edu, marital, blood, phone, email, address = row

        story.append(Paragraph("Employee Information", title_style))
        story.append(Spacer(1, 10))

        # Process photo
        if photo_data:
            try:
                img = PilImage.open(io.BytesIO(photo_data))
                img.thumbnail((120, 120))
                byte_arr = io.BytesIO()
                img.save(byte_arr, format='PNG')
                byte_arr.seek(0)
                rl_img = RLImage(byte_arr, width=1.5*inch, height=1.5*inch)
            except:
                rl_img = Paragraph("No photo", header_style)
        else:
            rl_img = Paragraph("No photo", header_style)

        # Info table including Education
        info_data = [
            [Paragraph("<b>Name:</b>", label_style), Paragraph(name, value_style)],
            [Paragraph("<b>Age:</b>", label_style), Paragraph(str(age), value_style)],
            [Paragraph("<b>Date of Birth:</b>", label_style), Paragraph(str(dob), value_style)],
            [Paragraph("<b>Sex:</b>", label_style), Paragraph(sex, value_style)],
            [Paragraph("<b>Marital Status:</b>", label_style), Paragraph(marital, value_style)],
            [Paragraph("<b>Blood Type:</b>", label_style), Paragraph(blood, value_style)],
            [Paragraph("<b>Phone:</b>", label_style), Paragraph(phone, value_style)],
            [Paragraph("<b>Email:</b>", label_style), Paragraph(email, value_style)],
            [Paragraph("<b>Address:</b>", label_style), Paragraph(address, value_style)],
            [Paragraph("<b>Education:</b>", label_style), Paragraph(edu if edu else "N/A", value_style)],
        ]

        info_table = Table(info_data, colWidths=[120, 360])
        info_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))

        # Combine Info + Photo (photo on the right side)
        combined_table = Table([[info_table, rl_img]], colWidths=[420, 120])
        combined_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))

        story.append(combined_table)
        story.append(Spacer(1, 24))

        if i < len(rows) - 1:
            story.append(PageBreak())

    doc.build(story)
    messagebox.showinfo("Success", "Information exported as PDF successfully!")
