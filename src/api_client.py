import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

class ClauseAPIClient:
    def __init__(self):
        self.client = InferenceClient(
            provider="together",
            api_key=os.getenv("HF_API_KEY")
        )
    
    def extract_clauses(self, contract_text):
        prompt = """Analyze this contract and extract main clauses in JSON format with these keys: 
        parties, payment_terms, termination. Return ONLY valid JSON without markdown:

        Contract Text:
        """ + contract_text[:12000]
        
        completion = self.client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800
        )
        
        return self._parse_response(completion.choices[0].message.content)

    def _parse_response(self, text):
        try:
            start = text.index('{')
            end = text.rindex('}') + 1
            return eval(text[start:end])
        except:
            return {"error": "Failed to parse API response"}