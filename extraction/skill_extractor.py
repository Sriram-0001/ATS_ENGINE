from groq import Groq
import os
import json
import re


client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class SkillExtractor:

    def extract(self, text: str, source: str = "jd"):
        if source == "jd":
            instruction = "Extract ONLY required technical skills from this job description."
        else:
            instruction = "Extract technical skills that the candidate possesses from this resume."
        # 🔥 TRY LLM FIRST
        try:
            prompt = f"""
{instruction}

Text:
{text}

Rules:
- Return ONLY a JSON list
- No explanation
- No extra text
- Include tools, technologies, frameworks

Example:
["python", "sql", "docker"]
"""

            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You extract technical skills."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )

            content = response.choices[0].message.content

            print("LLM SKILL OUTPUT:", content)

            # 🔥 clean JSON
            json_match = re.search(r"\[[^\[\]]*\]", content)

            if not json_match:
                raise Exception("No JSON found")

            skills = json.loads(json_match.group())

            # normalize
            skills = [
                s.lower().strip()
                for s in skills
                if len(s) < 30 and (" " not in s or "/" in s)
            ]
            return list(set([s.lower().strip() for s in skills]))

        except Exception as e:

            print("LLM FAILED → fallback:", e)

            # 🔥 FALLBACK (your old logic)
            TECH_KEYWORDS = [
                "python", "java", "sql", "linux", "debugging",
                "troubleshooting", "backend", "systems",
                "logs", "monitoring", "communication",
                "docker", "microservices", "support"
            ]

            text = text.lower()
            skills = []

            for keyword in TECH_KEYWORDS:
                if keyword in text:
                    skills.append(keyword)

            return list(set(skills))