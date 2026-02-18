"""
LLM Service using official Groq Python SDK (Llama 3.3 70B)
"""

from groq import Groq
from app.config import get_settings


class LLMService:
    def __init__(self, model_name: str = None, api_key: str = None):
        settings = get_settings()
        self.model_name = model_name or settings.LLM_MODEL
        # Groq client reads GROQ_API_KEY from env automatically,
        # but we can also pass it explicitly
        self.client = Groq(api_key=api_key or settings.GROQ_API_KEY)

    def generate_answer(self, query: str, context: str, max_length: int = 512) -> str:
        """Generate answer using Groq (Llama 3.3 70B)"""

        system_prompt = (
            "You are a helpful assistant that answers questions about IIIT Kota's placement policies. "
            "Answer based only on the provided context. "
            "If the answer is not in the context, say 'I don't have enough information to answer this.' "
            "Common abbreviations used in the documents: "
            "SPC = Student Placement Coordinator, T&P = Training and Placement Cell, "
            "PPO = Pre-Placement Offer, CGPA = Cumulative Grade Point Average, "
            "NOC = No Objection Certificate. "
            "Be concise and well-structured. Use bullet points or numbered lists when listing multiple items."
        )

        user_message = (
            f"Context:\n{context[:3000]}\n\n"
            f"Question: {query}"
        )

        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.3,
            max_completion_tokens=max_length,
            top_p=1,
            stream=False,
            stop=None
        )

        return completion.choices[0].message.content.strip()