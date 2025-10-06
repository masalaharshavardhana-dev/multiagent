import re

from tools import CalculatorTool, WeatherTool, StringTool, LLMTool
class CalculatorAgent:
    def __init__(self):
        self.tool = CalculatorTool()
        
    def perform_task(self, question):
        if any(word in question.lower() for word in ["add", "plus", "+", "multiply", "*", "times","subtract", "-", "divide", "/"]):
            numbers=list(map(int, [s for s in question.split() if s.isdigit()]))
            if len(numbers)<2:
                return "Please provide at least two numbers."
            else:
                if any(word in question.lower() for word in ["add", "plus", "+"]):
                    return self.tool.add(*numbers)
                elif any(word in question.lower() for word in ["subtract", "-"]):
                    return self.tool.subtract(*numbers)
                elif any(word in question.lower() for word in ["multiply", "*", "times"]):
                    return self.tool.multiply(*numbers)
                elif any(word in question.lower() for word in ["divide", "/", "over"]):
                    return self.tool.divide(*numbers)
            return None


class WeatherAgent:
    def __init__(self, api_key):
        self.tool = WeatherTool(api_key)
    
    def perform_task(self, question):
        if any(word in question.lower() for word in ["weather", "temperature", "forecast"]):
            city_match=re.search(r'weather in ([\w\s]+)',question,re.IGNORECASE)
            if city_match:
                city=city_match.group(1).strip()
                return self.tool.get_weather(city)
            else:
                return "Please specify a city."
        return None


class StringAgent:
    def __init__(self):
        self.tool=StringTool()
    def perform_task(self, question):
        if any(word in question.lower() for word in ["reverse", "uppercase", "to upper", "capital"]):
            if "reverse" in question.lower():
                text_match=re.search(r'reverse (.+)',question,re.IGNORECASE)
                if text_match:
                    text=text_match.group(1).strip()
                    return self.tool.reverse(text)
            elif "uppercase" in question.lower() or "to upper" in question.lower() or "capital" in question.lower():
                text_match=re.search(r'uppercase (.+)',question,re.IGNORECASE)
                if text_match:
                    text=text_match.group(1).strip()
                    return self.tool.to_upper(text)
        return None
    
    
class LLMAgent:
    def __init__(self, huggingface_api_key):
        self.tool=LLMTool(huggingface_api_key)

    def perform_task(self, question):
        return self.tool.perform_task(question)


class MasterAgent:
    def __init__(self, weather_api_key, huggingface_api_key):
        self.agents=[CalculatorAgent(), WeatherAgent(weather_api_key), StringAgent(), LLMAgent(huggingface_api_key)]
        
    def perform_task(self, question):
        for agent in self.agents:
            result=agent.perform_task(question)
            if result is not None:
                return result
        return "No suitable agent found."