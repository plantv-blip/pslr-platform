#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM API Clients for PSLR Analysis
Unified interface for multiple LLM providers
"""

import re
import json
import time
from datetime import datetime
from typing import Dict, Any


class LLMClient:
    """Base class for LLM API clients"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def call(self, system_prompt: str, user_prompt: str) -> str:
        raise NotImplementedError


class OpenAIClient(LLMClient):
    def call(self, system_prompt: str, user_prompt: str) -> str:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API Error: {str(e)}")


class AnthropicClient(LLMClient):
    def call(self, system_prompt: str, user_prompt: str) -> str:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key)
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                temperature=0.3,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            return response.content[0].text
        except Exception as e:
            raise Exception(f"Anthropic API Error: {str(e)}")


class GoogleClient(LLMClient):
    def call(self, system_prompt: str, user_prompt: str) -> str:
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(
                model_name='gemini-2.0-flash-exp',
                system_instruction=system_prompt
            )
            response = model.generate_content(
                user_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,
                    max_output_tokens=1000,
                )
            )
            return response.text
        except Exception as e:
            raise Exception(f"Google API Error: {str(e)}")


class DeepSeekClient(LLMClient):
    def call(self, system_prompt: str, user_prompt: str) -> str:
        try:
            from openai import OpenAI
            client = OpenAI(
                api_key=self.api_key,
                base_url="https://api.deepseek.com"
            )
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"DeepSeek API Error: {str(e)}")


class XAIClient(LLMClient):
    def call(self, system_prompt: str, user_prompt: str) -> str:
        try:
            from openai import OpenAI
            client = OpenAI(
                api_key=self.api_key,
                base_url="https://api.x.ai/v1"
            )
            response = client.chat.completions.create(
                model="grok-2-1212",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"xAI API Error: {str(e)}")


class PSLRAnalyzer:
    """PSLR (Physical-Spiritual-Logical-Relational) 분석 엔진"""
    
    MODEL_CLIENTS = {
        "gpt-4o": OpenAIClient,
        "claude": AnthropicClient,
        "gemini": GoogleClient,
        "deepseek": DeepSeekClient,
        "grok": XAIClient
    }
    
    MODEL_NAMES = {
        "gpt-4o": "GPT-4o",
        "claude": "Claude-3.5-Sonnet",
        "gemini": "Gemini-2.0-Flash",
        "deepseek": "DeepSeek-V3",
        "grok": "Grok-2"
    }
    
    def generate_system_prompt(self, language: str) -> str:
        """Generate PSLR system prompt"""
        return f"""You are an expert in ontological analysis using the PSLR (Physical-Spiritual-Logical-Relational) framework.

PSLR Framework:
The framework represents any concept as a quaternion structure with four dimensions:

1. P (Physical): Material, tangible, concrete, substantial aspects - the "what exists" dimension
2. S (Spiritual): Root, origin, motivational, fundamental aspects - the "why it exists" dimension
3. L (Logical): Rational, systematic, structural, causal aspects - the "how it works" dimension
4. R (Relational): Interactive, connective, contextual, relational aspects - the "how it relates" dimension

CRITICAL CONSTRAINT: The sum of all four values must equal EXACTLY 2.0
(P + S + L + R = 2.0)

Each value must be between 0 and 1, with up to 2 decimal places.

Response Format (JSON only):
{{
  "P": 0.XX,
  "S": 0.XX,
  "L": 0.XX,
  "R": 0.XX,
  "reasoning": "Brief explanation of your analysis (2-3 sentences)"
}}

Verify: P + S + L + R = 2.0"""
    
    def parse_response(self, response_text: str) -> Dict[str, Any]:
        """Parse LLM response and extract PSLR values"""
        # Find JSON in response
        json_match = re.search(r'\{[^}]+\}', response_text, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON found in response")
        
        json_str = json_match.group(0)
        data = json.loads(json_str)
        
        # Extract PSLR values
        result = {
            "P": float(data.get("P", 0)),
            "S": float(data.get("S", 0)),
            "L": float(data.get("L", 0)),
            "R": float(data.get("R", 0)),
            "reasoning": data.get("reasoning", "")
        }
        
        # Normalize to sum = 2.0
        total = result["P"] + result["S"] + result["L"] + result["R"]
        if abs(total - 2.0) > 0.01:
            if total > 0:
                scale_factor = 2.0 / total
                result["P"] = round(result["P"] * scale_factor, 2)
                result["S"] = round(result["S"] * scale_factor, 2)
                result["L"] = round(result["L"] * scale_factor, 2)
                result["R"] = round(result["R"] * scale_factor, 2)
                
                # Fine-tune to exact 2.0
                new_total = result["P"] + result["S"] + result["L"] + result["R"]
                diff = 2.0 - new_total
                if abs(diff) > 0.001:
                    max_key = max(["P", "S", "L", "R"], key=lambda k: result[k])
                    result[max_key] = round(result[max_key] + diff, 2)
            else:
                result = {"P": 0.5, "S": 0.5, "L": 0.5, "R": 0.5, "reasoning": "Default values"}
        
        return result
    
    def analyze(self, concept: str, language: str, model: str, api_key: str) -> Dict[str, Any]:
        """Perform PSLR analysis on a concept"""
        system_prompt = self.generate_system_prompt(language)
        user_prompt = f"Analyze the concept: {concept}"
        
        client_class = self.MODEL_CLIENTS[model]
        client = client_class(api_key)
        
        try:
            start_time = time.time()
            response_text = client.call(system_prompt, user_prompt)
            result = self.parse_response(response_text)
            response_time = int((time.time() - start_time) * 1000)
            
            return {
                "success": True,
                "concept": concept,
                "language": language,
                "model": model,
                "model_name": self.MODEL_NAMES[model],
                "timestamp": datetime.now().isoformat(),
                "result": result,
                "raw_response": response_text,
                "response_time": response_time
            }
        except Exception as e:
            return {
                "success": False,
                "concept": concept,
                "language": language,
                "model": model,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
