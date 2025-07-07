import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY','')

class AnalyticsEngine:
    @staticmethod
    def categorize(transactions: list) -> list:
        if not openai.api_key:
            return transactions
        # NLP categorization via OpenAI
        return transactions

    @staticmethod
    def summarize(transactions: list) -> str:
        if not openai.api_key:
            return ''
        prompt = 'Analyze these transactions: ' + str(transactions)
        resp = openai.ChatCompletion.create(
            model='gpt-4o-mini',
            messages=[{'role':'user','content':prompt}]
        )
        return resp.choices[0].message.content
