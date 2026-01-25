import json
import google.generativeai as genai
import json_repair
from app.core.config import settings

# Configure Gemini
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

generation_config = {
  "temperature": 0.2,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}

class AIService:
    def __init__(self):
        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash", 
            generation_config=generation_config,
            system_instruction="""
            You are an expert academic editor and formatter. 
            Your task is to analyze research paper drafts and provide structured feedback and formatting data.
            Do NOT rewrite the content effectively, but structure it.
            Output valid JSON.
            """
        )

    def analyze_document(self, text_content: str):
        prompt = """Analyze the following academic or technical document text.

This may be:
- Research paper
- Project / internship report
- Technical / business report

Your task is to intelligently analyze, fix and standardize the document.

You are allowed to:
- Rename section headers
- Merge or split sections
- Rewrite unclear content
- Reorder content
- Fix reference and formatting issues
- Apply pagination intelligence (no orphan headings, no broken flow)

--------------------------------------------------
RETURN JSON IN THIS EXACT FORMAT
--------------------------------------------------

{
  "title": "Improved professional title",

  "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],

  "sections": [
    {
      "original_header": "original heading from document",
      "standardized_header": "Improved professional heading",
      "content_snippet": "First 3–4 sentences of the rewritten section"
    }
  ],

  "issues": [
    {
      "type": "reference | structure | layout | grammar",
      "description": "Clear description of what was fixed or detected"
    }
  ]
}

--------------------------------------------------
RULES
--------------------------------------------------

• Do not ask the user any questions.
• Output must be professional and submission-ready.
• Rewrite weak text but preserve original meaning.
• Do NOT change content length — only report layout risks.
• Detect headings that would likely appear alone at page bottom.
• If a section has less than 2 paragraphs before a page break, flag it.
• Report in issues list with type="layout".

--------------------------------------------------
DOCUMENT CONTENT:
--------------------------------------------------
""" + text_content[:30000]

        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            # Clean markdown code blocks if present
            if response_text.startswith("```"):
                lines = response_text.splitlines()
                # Remove first line if it starts with ```
                if lines[0].startswith("```"):
                    lines = lines[1:]
                # Remove last line if it starts with ```
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                response_text = "\n".join(lines).strip()
            
            data = json_repair.loads(response_text)
            return data
        except Exception as e:
            print(f"AI Analysis failed: {e}")
            return {
                "title": "Error analyzing title",
                "keywords": [],
                "sections": [],
                "issues": [{"type": "error", "description": f"AI analysis failed: {str(e)}"}]
            }

ai_service = AIService()
