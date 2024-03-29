from openai import OpenAI
import pandas as pd
from keys import openai_key
from datetime import datetime

openai_key = openai_key
client = OpenAI(api_key = openai_key)

def gpt_4_chat_completion(messages:list, temp:float = .9, pres:float = 0, freq:float = 0):
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


df = pd.read_excel(r"./bracket-predictions/NCAA_Games.xlsx")
teams_list = list(df.Team)
team_pairs = list(zip(teams_list[::2], teams_list[1::2]))

current_time = datetime.now()

i = 1
while len(team_pairs) > 0:
    len_pairs = len(team_pairs)
    winners = []
    for x in team_pairs:
        system_prompt = """You are an avid NCAA basketball fan and sports analyst."""
        user_prompt = f"""Using your own knowledge, pretend there is a men's basketball matchup between {x[0]} and {x[1]}. Who might
        be expected to win this theoretical matchup? Please provide only the name of the team you might expect to win, no other prose required."""

        messages = [{"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}]

        response = gpt_4_chat_completion(messages)

        winners.append(response)

    print("Winners:", winners)
    
    output = pd.DataFrame(winners, columns = ["Winners"])
    filename = f"Winners_{current_time.strftime('%H%M')}_{i}.xlsx"
    output.to_excel(filename, index = False)

    team_pairs = list(zip(winners[::2], winners[1::2]))
    i += 1

    if len_pairs != len(winners):
        print("Pairs:", len_pairs)
        print("Winners:", len(winners))
        break

df1 = pd.read_excel(f"Winners_{current_time.strftime('%H%M')}_1.xlsx")
df2 = pd.read_excel(f"Winners_{current_time.strftime('%H%M')}_2.xlsx")
df3 = pd.read_excel(f"Winners_{current_time.strftime('%H%M')}_3.xlsx")
df4 = pd.read_excel(f"Winners_{current_time.strftime('%H%M')}_4.xlsx")
df5 = pd.read_excel(f"Winners_{current_time.strftime('%H%M')}_5.xlsx")
df6 = pd.read_excel(f"Winners_{current_time.strftime('%H%M')}_6.xlsx")

all_winners = pd.concat([df1,df2,df3,df4,df5,df6], axis =1)
all_winners.to_excel(f"AllWinners_{current_time.strftime('%H%M')}.xlsx", index = False)