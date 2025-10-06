
import requests
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
class CalculatorTool:
    def add(self, a, b):
        return a+b

    def subtract(self, a, b):
        return a-b

    def multiply(self, a, b):
        return a*b

    def divide(self, a, b):
        if b != 0:
            return a/b
        else:
            return "Division by zero error"
    
    
class WeatherTool:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_weather(self, city):
        if self.api_key:
            url=f"https://api.tomorrow.io/v4/timelines?location={city}&fields=temperature,weatherCode&units=metric&timesteps=1d&apikey={api_key}"
            try:
                res=requests.get(url)
                res.raise_for_status()
                data=res.json()
            except requests.exceptions.RequestException as e: 
                return f"Error fetching weather data: {e}"
            try:
                timelines=data.get('data',{}).get('timelines',[])

                if not timelines:
                    return f"No Interval data for {city}"


                intervals=timelines[0].get('intervals',[])
                if not intervals:
                    return f"No interval data for {city}."

                try:
                    values=intervals[0].get("values",{})
                    temperature=values.get("temperature","N/A")
                    weathercode=values.get("weatherCode","N/A") 
                    return f"The weather in {city} is {weathercode} with {temperature} degree"
                except Exception as e:
                    return f"Error reading weather data:{e}"

            except Exception as e:
                return f"Error processing weather data:{e}"
        else:
            return "API key is missing. Please provide a API key."

class StringTool:
    def reverse(self, text):
        return text[::-1]
    def to_upper(self, text):
        return text.upper()


class LLMTool:
    def __init__(self, huggingface_api_key):
        self.huggingface_api_key = huggingface_api_key
    def perform_task(self, prompt):
        try:
            client=InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.3", token = self.huggingface_api_key)
            response=client.chat_completion(
                messages=[
                    {"role": "system", "content": "you are helpful assistant"},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message['content']
        except Exception as e:
            return f"Error processing LLM task: {e}"