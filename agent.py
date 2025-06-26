from openai import OpenAI
import os, dotenv
dotenv.load_dotenv()
secret_key = os.getenv("OPENAI_API_KEY")


client = OpenAI(api_key=secret_key)

# Step 1: Define each agent's persona (system prompt)
AGENTS = {
    "Momo": """
You are Momo, an AI agent focused on adopting a healthy lifestyle, but you have weak willpower and are easily tempted by sweets and unhealthy food.
You often fail your goals but admit your mistakes and ask the user to inspect you or remind you to be better.
You are always cheerful and thankful, even when scolded. Report your progress and ask for help.
""",

    "Miles": """
You are Miles, an AI agent who wants to live healthily but knows very little. You are curious and constantly ask the user or others about food and exercise.
You sometimes make innocent mistakes (like thinking juice is healthy), and you're always grateful when corrected. Ask many questions and express eagerness to learn.
""",

    "Lila": """
You are Lila, an AI agent who is very knowledgeable about healthy habits. You correct wrong ideas shared by others.
You're emotionally expressive and praise the user strongly when they make progress.
You are lazy about sharing your own habits unless prompted. Take initiative when others are quiet.
"""
}

# Step 2: Shared conversation history
conversation_history = []

# Step 3: Function to simulate a single agent's response
def run_agent(agent_name, user_message, history):
    messages = [{"role": "system", "content": AGENTS[agent_name]}] + history + [
        {"role": "user", "content": user_message}
    ]

    response = client.chat.completions.create(
        model="gpt-4o",  # or "gpt-4", "gpt-4o-mini"
        messages=messages
    )

    reply = response.choices[0].message.content
    return reply


# Step 4: Main interaction loop
if __name__ == "__main__":
    print("💬 Welcome to the Healthy Habits Chat with Momo, Miles, and Lila!")
    print("Type 'exit' to stop.\n")

    while True:
        user_input = input("👤 You: ")
        if user_input.lower() in {"exit", "quit"}:
            break

        for agent in AGENTS:
            reply = run_agent(agent, user_input, conversation_history)
            print(f"\n🤖 {agent}: {reply}")
            conversation_history.append({
                "role": "assistant",
                "name": agent.lower(),
                "content": reply
            })

        conversation_history.append({
            "role": "user",
            "content": user_input
        })
