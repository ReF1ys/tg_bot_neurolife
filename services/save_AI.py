import asyncio
import google.generativeai as genai
from config.config import GOOGLE_AI_API_KEY

class GoogleAIService:
    def __init__(self):
        genai.configure(api_key=GOOGLE_AI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')

    async def generate_post(self, scraped_data):
        prompt = f"""
        На основе следующей информации создайте интересный пост для Telegram:
        {scraped_data}
        
        Пост должен быть информативным, легко читаемым и привлекательным для аудитории.
        """
        result = await self.model.generate_content(prompt)
        return result.candidates[0].content.parts[0].text

    def answer_question(self, question, context):
        prompt = f"""
        Question: {question}
        Context: {context}
        
        Please provide an accurate and informative answer based on the provided context.
        """
        result = self.model.generate_content(prompt)
        return result.candidates[0].content.parts[0].text