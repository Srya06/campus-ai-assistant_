import io
import re
from typing import Optional
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether
)

class CampusPDFGenerator:
    """
    Industry-grade Institutional PDF Generator for Course Lecture Notes & Syllabus Materials.
    Produces high-fidelity academic documents with institutional headers, metadata boxes,
    callouts, and page number footers.
    """

    @staticmethod
    def generate_course_note_pdf(
        course_code: str,
        course_title: str,
        unit_number: int,
        unit_title: str,
        topic_description: str,
        content_text: str,
        faculty_author: str = "Department Faculty",
        academic_year: str = "2025-2026",
        department_name: str = "Computer Science & Engineering"
    ) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=45,
            leftMargin=45,
            topMargin=45,
            bottomMargin=45
        )

        styles = getSampleStyleSheet()

        # Custom Typography
        inst_title_style = ParagraphStyle(
            'InstTitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=16,
            leading=20,
            textColor=colors.HexColor('#1e1b4b'),
            alignment=1 # Center
        )

        inst_sub_style = ParagraphStyle(
            'InstSubtitle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor('#475569'),
            alignment=1
        )

        course_heading_style = ParagraphStyle(
            'CourseHeading',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=13.5,
            leading=18,
            textColor=colors.HexColor('#312e81')
        )

        unit_heading_style = ParagraphStyle(
            'UnitHeading',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=12,
            leading=16,
            textColor=colors.HexColor('#4338ca')
        )

        meta_label_style = ParagraphStyle(
            'MetaLabel',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=9,
            leading=12,
            textColor=colors.HexColor('#1e293b')
        )

        body_style = ParagraphStyle(
            'Body',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=15,
            textColor=colors.HexColor('#1e293b')
        )

        section_title_style = ParagraphStyle(
            'SectionTitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=11,
            leading=15,
            textColor=colors.HexColor('#1e1b4b'),
            spaceBefore=10,
            spaceAfter=4
        )

        callout_style = ParagraphStyle(
            'CalloutText',
            parent=styles['Normal'],
            fontName='Helvetica-Oblique',
            fontSize=9.5,
            leading=14,
            textColor=colors.HexColor('#312e81')
        )

        story = []

        # 1. Institution Header Banner
        story.append(Paragraph("APEX INSTITUTE OF TECHNOLOGY & ENGINEERING", inst_title_style))
        story.append(Spacer(1, 3))
        story.append(Paragraph(
            f"Department of {department_name} • Academic Session {academic_year}",
            inst_sub_style
        ))
        story.append(Paragraph(
            "Verified Course Study Material & Comprehensive Lecture Notes",
            inst_sub_style
        ))
        story.append(Spacer(1, 8))
        story.append(HRFlowable(
            width="100%",
            thickness=1.5,
            color=colors.HexColor('#4f46e5'),
            spaceBefore=2,
            spaceAfter=12
        ))

        # 2. Course & Module Metadata Card (Table)
        meta_data = [
            [
                Paragraph(f"<b>Course:</b> {course_code} — {course_title}", meta_label_style),
                Paragraph(f"<b>Faculty In-Charge:</b> {faculty_author}", meta_label_style)
            ],
            [
                Paragraph(f"<b>Unit {unit_number}:</b> {unit_title}", meta_label_style),
                Paragraph(f"<b>Status:</b> Official Curriculum Material", meta_label_style)
            ]
        ]
        meta_table = Table(meta_data, colWidths=[310, 210])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 14))

        # 3. Topic Overview Callout Box
        if topic_description:
            story.append(Paragraph("📌 SYLLABUS TOPICS COVERED IN THIS UNIT", section_title_style))
            overview_data = [[Paragraph(topic_description, callout_style)]]
            overview_table = Table(overview_data, colWidths=[520])
            overview_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f5f3ff')),
                ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#c7d2fe')),
                ('LEFTPADDING', (0, 0), (-1, -1), 12),
                ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(overview_table)
            story.append(Spacer(1, 14))

        # 4. Lecture Content Parser
        story.append(Paragraph("📖 COMPREHENSIVE LECTURE NOTES & ACADEMIC MATERIAL", section_title_style))
        story.append(Spacer(1, 4))

        # Split content into paragraphs and headers
        raw_lines = content_text.split('\n')
        current_p = []

        def flush_current_p():
            if current_p:
                combined = " ".join(current_p).strip()
                if combined:
                    # Escape HTML entities for reportlab
                    safe = (combined
                            .replace('&', '&amp;')
                            .replace('<', '&lt;')
                            .replace('>', '&gt;'))
                    # Bold markdown
                    safe = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', safe)
                    safe = re.sub(r'\*(.*?)\*', r'<i>\1</i>', safe)
                    story.append(Paragraph(safe, body_style))
                    story.append(Spacer(1, 6))
                current_p.clear()

        for line in raw_lines:
            line_str = line.strip()
            if not line_str:
                flush_current_p()
                continue

            if line_str.startswith('### '):
                flush_current_p()
                title_text = line_str[4:].strip().replace('&', '&amp;')
                story.append(Paragraph(f"<b>{title_text}</b>", ParagraphStyle('SubSub', parent=section_title_style, fontSize=10.5, leading=14, textColor=colors.HexColor('#4338ca'))))
                story.append(Spacer(1, 4))
            elif line_str.startswith('## '):
                flush_current_p()
                title_text = line_str[3:].strip().replace('&', '&amp;')
                story.append(Paragraph(f"<b>{title_text}</b>", section_title_style))
                story.append(Spacer(1, 4))
            elif line_str.startswith('# '):
                flush_current_p()
                title_text = line_str[2:].strip().replace('&', '&amp;')
                story.append(Paragraph(f"<b>{title_text}</b>", unit_heading_style))
                story.append(Spacer(1, 6))
            elif line_str.startswith('- ') or line_str.startswith('* '):
                flush_current_p()
                bullet_text = line_str[2:].strip().replace('&', '&amp;')
                bullet_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', bullet_text)
                story.append(Paragraph(f"• &nbsp; {bullet_text}", body_style))
                story.append(Spacer(1, 4))
            else:
                current_p.append(line_str)

        flush_current_p()

        # 5. Footer Watermark & Verification Notice
        story.append(Spacer(1, 20))
        story.append(HRFlowable(
            width="100%",
            thickness=0.8,
            color=colors.HexColor('#cbd5e1'),
            spaceBefore=10,
            spaceAfter=8
        ))
        footer_text = f"Apex Institute Academic Repository • {course_code} {unit_title} • Verified for Semester Examination Preparation"
        story.append(Paragraph(footer_text, ParagraphStyle('FooterStyle', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=8, leading=10, textColor=colors.HexColor('#94a3b8'), alignment=1)))

        doc.build(story)
        return buffer.getvalue()
