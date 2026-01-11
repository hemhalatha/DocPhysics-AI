from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

def extract_text_from_docx(file_path):
    """
    Extracts full text from a DOCX file.
    """
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)


from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def keep_heading_with_content(paragraph):
    """Rule A: Keep with Next (no orphan headings)"""
    p = paragraph._p
    pPr = p.get_or_add_pPr()
    keepNext = pPr.find(qn('w:keepNext'))
    if keepNext is None:
        keepNext = OxmlElement('w:keepNext')
        pPr.append(keepNext)

def prevent_widow(paragraph):
    """Rule C: Prevent single-line section endings"""
    p = paragraph._p
    pPr = p.get_or_add_pPr()
    widow = pPr.find(qn('w:widowControl'))
    if widow is None:
        widow = OxmlElement('w:widowControl')
        pPr.append(widow)

def apply_journal_formatting(input_path, output_path, analysis_data):
    """
    Rebuilds the DOCX with IEEE-like formatting.
    """
    doc = Document(input_path)
    
    # 1. Base Styles (Times New Roman)
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    
    # Enable global settings
    doc.settings.odd_and_even_pages_header_footer = False 

    # 2. Iterate paragraphs to apply pagination rules
    keywords_inserted = False
    
    for i, para in enumerate(doc.paragraphs):
        # Apply standard pagination rules to ALL paragraphs
        prevent_widow(para)

        # A. Insert Keywords after the first paragraph (index 0)
        # We assume para[0] is the title or banner. We do NOT touch it.
        if i == 0:
            if analysis_data.get("keywords") and not keywords_inserted:
                kw_text = "Keywords: " + ", ".join(analysis_data["keywords"])
                # Add keywords after the first paragraph
                if len(doc.paragraphs) > 1:
                    p = doc.paragraphs[1].insert_paragraph_before(kw_text)
                else:
                    p = doc.add_paragraph(kw_text)
                
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.runs[0].font.italic = True
                p.runs[0].font.name = 'Times New Roman'
                p.runs[0].font.size = Pt(12)
                keywords_inserted = True
            continue

        # B. Pagination Fixes for Headers (Orphan Control only)
        # Rule A: Enforce Keep with Next on all headers
        if para.style.name.startswith("Heading"):
             keep_heading_with_content(para)
             para.paragraph_format.keep_with_next = True # Redundant specific api call just in case
             para.paragraph_format.keep_together = True

    # 3. Add Footer Verification
    section = doc.sections[0]
    footer = section.footer
    footer_para = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    footer_para.text = "Formatted by ResearchMate AI"
    footer_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for run in footer_para.runs:
        run.font.size = Pt(8)
        run.font.italic = True
        
    doc.save(output_path)
    return output_path

