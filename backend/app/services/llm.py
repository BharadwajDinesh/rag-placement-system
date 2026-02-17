from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

class LLMService:
    def __init__(self, model_name: str):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            model_name,
            torch_dtype=torch.float32  # Use float32 for CPU
        ).to(self.device)
    
    def generate_answer(self, query: str, context: str, max_length: int = 256) -> str:
        """Generate answer based on context"""
        prompt = f"""Answer the question based on the context below. If the answer cannot be found in the context, say "I don't have enough information to answer this question."

Context: {context}

Question: {query}

Answer:"""
        
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            max_length=512,
            truncation=True
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                num_beams=4,
                temperature=0.7,
                do_sample=True,
                top_p=0.9
            )
        
        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return answer.strip()