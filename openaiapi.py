import openai


class OpenAIAPI:
    def __init__(self, key):
        openai.api_key = key

    def completion(self, prompt):
        response = openai.Completion.create(
            model='text-davinci-003',
            prompt=prompt,
            temperature=1,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response['choices'][0]['text']

    def generation(self, prompt):
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size='256x256'
        )

        return response['data'][0]['url']
