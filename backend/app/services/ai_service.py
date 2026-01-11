import json
import google.generativeai as genai
from backend.app.core.config import settings

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
            model_name="gemini-1.5-flash", 
            generation_config=generation_config,
            system_instruction="""
            You are an expert academic editor and formatter. 
            Your task is to analyze research paper drafts and provide structured feedback and formatting data.
            Do NOT rewrite the content effectively, but structure it.
            Output valid JSON.
            """
        )

    def analyze_document(self, text_content: str):
        prompt = f"""
        Analyze the following academic paper text. 
        Return a JSON object with the following structure:
        {{
            "title": "Suggested Title",
            "keywords": ["keyword1", "keyword2", "keyword3"],
            "sections": [
                {{ "original_header": "intro", "standardized_header": "Introduction", "content_snippet": "start of content..." }}
            ],
            "issues": [
                {{ "type": "reference", "description": "Citation [3] is missing in references list." }}
            ]
        }}

        Text content:
        {text_content[:30000]} 
        """ 

        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except Exception as e:
            print(f"AI Analysis failed: {e}")
            return {
                "title": "Error analyzing title",
                "keywords": [],
                "sections": [],
                "issues": [{"type": "error", "description": f"AI analysis failed: {str(e)}"}]
            }

ai_service = AIService()
