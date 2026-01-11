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

def apply_journal_formatting(input_path, output_path, analysis_data):
    """
    Rebuilds the DOCX with IEEE-like formatting.
    """
    doc = Document(input_path)
    
    # 1. Base Styles (Times New Roman)
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(10)
    
    # 2. Title Formatting (Heuristic: First non-empty paragraph)
    title_set = False
    
    for para in doc.paragraphs:
        if not para.text.strip():
            continue
            
        if not title_set:
            para.style = doc.styles['Title']
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = para.runs[0] if para.runs else para.add_run(para.text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(24)
            run.font.bold = True
            title_set = True
            
            # Insert Keywords if available
            if analysis_data.get("keywords"):
                # Ideally, we'd insert this cleanly. Appending for MVP stability.
                pass 
            continue

        # 3. Heading Standardization
        if para.style.name.startswith("Heading"):
             if para.runs:
                 para.runs[0].font.name = 'Times New Roman'
                 para.runs[0].font.color.rgb = None 
        
    doc.save(output_path)
    return output_path
