# GPT-4 NCAA Bracket Predictions
## WARNING: THIS IS JUST A JOKE / FUN EXPERIMENT
There is no reason to believe GPT-4 would be good at predicting the outcomes in March Madness primarily because the knowledge base is out of date. This was done purely because I was asked to complete a bracket and I don't care about sports. Use at your own risk. 

Here's the bulk of the code.

```python
df = pd.read_excel(r"./bracket-predictions/NCAA_Games.xlsx")
teams_list = list(df.Team)
team_pairs = list(zip(teams_list[::2], teams_list[1::2]))

i = 1
while len(team_pairs) > 0:
    len_pairs = len(team_pairs)
    winners = []
    for x in team_pairs:
        system_prompt = """You are an avid NCAA basketball fan and sports analyst."""
        user_prompt = f"""Using only your own knowledge, pretend there is a men's basketball matchup between {x[0]} and {x[1]}. Who might
        be expected to win this theoretical matchup? Please provide only the name of the team you might expect to win, no other prose required."""

        messages = [{"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}]

        response = gpt_4_chat_completion(messages)

        winners.append(response)

    print("Winners:", winners)
    
    output = pd.DataFrame(winners, columns = ["Winners"])
    current_time = datetime.now()
    filename = f"Winners_{i}_{current_time.strftime('%H%M')}.xlsx"
    output.to_excel(filename, index = False)

    team_pairs = list(zip(winners[::2], winners[1::2]))
    i += 1
    ```

