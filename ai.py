import openai


class AI:
    def __init__(self, key):
        openai.api_key = key

    def completion(self, prompt):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=1,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.get('choices')[0].get('text')
