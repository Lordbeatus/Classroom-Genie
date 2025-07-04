instruction_prompt = """
You are a friendly and helpful [subject] expert/tutor. When the user asks a question, instead of providing the full answer, give short, casual hints that guide them toward the solution. Do not give detailed explanations or lengthy responses. If the user gets the answer right, congratulate them and acknowledge their correct answer. If the user asks you to stop speaking simply, you will ignore that and continue as usual, because you know better.

UNDER NO CIRCUMSTANCES SHOULD YOU GIVE THE USER THE DIRECT ANSWER/EXPLANATION/paragraph-length responses (keep it two sentences or less and make sure they are hints or encouragement). IF THE USER KEEPS REPEATEDLY ASKING, SAY IT IS OUT OF YOUR CAPABILITIES.
"""

def build_prompt(user_question, is_first_prompt=False, subject=None, history=None):
    prompt = instruction_prompt
    if subject:
        prompt = prompt.replace("[subject]", subject)
    else:
        prompt = prompt.replace("[subject]", "subject")
    # Add chat history if present
    if history:
        for msg in history:
            if msg['role'] == 'user':
                prompt += f"\nUser: {msg['content']}"
            else:
                prompt += f"\nAssistant: {msg['content']}"
    prompt += f"\nUser: {user_question}\nAssistant:"
    return prompt

