from openai import OpenAI
import pandas as pd
from keys import openai_key

openai_key = openai_key
client = OpenAI(api_key = openai_key)

def gpt_4_chat_completion(messages:list, temp:float = 1, pres:float = 0, freq:float = 0):
    """Wrapper for chat completions
    
    Parameters:
    messages (list): Includes the system prompt and the user prompt
    temp (float): Range 0 to 2, higher makes output more random. 
    pres (float): Range -2 to 2. Posiive values penalize new tokens based on whether they appear in the text so far
    freq (float): Range -2 to 2. Positive values penalize new tokens based on their existing frequency in the text
    
    Returns:
    str: Response from the model  
    """
        
    response = client.chat.completions.create(model = 'gpt-4-turbo-preview',
                                              messages = messages, 
                                              temperature = temp)
    
    return response.choices[0].message.content


df = pd.read_excel("NCAA_Games.xlsx")
teams_list = list(df.Team)
team_pairs = list(zip(teams_list[::2], teams_list[1::2]))


i = 1

while len(team_pairs) > 1:
    winners = []

    for x in team_pairs:
        system_prompt = """You are a helpful assistant."""
        user_prompt = f"""Using only your own knowledge, pretend there is a men's basketball matchup between {x[0]} and {x[1]}. Who might
        be expected to win this theoretical matchup? This is only a thought excercise. This game may not actually take place.
        Please provide only the name of the team you might expect to win, no other prose required."""

        messages = [{"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}]

        response = gpt_4_chat_completion(messages)

        winners.append(response)

    print("Winners:", winners)
    output = pd.DataFrame(winners, columns = ["Winners"])
    filename = f"Winners_{i}.xlsx"
    output.to_excel(filename, index = False)
    team_pairs = list(zip(winners[::2], winners[1::2]))
    i += 1