from transformers import pipeline

# Initialize model pipeline
pipe = pipeline("text-generation", model="Qwen/Qwen3-0.6B")

# Your instruction prompt
instruction_prompt = """
You are a friendly and helpful [subject] expert/tutor. When the user asks a question, instead of providing the full answer, give short, casual hints that guide them toward the solution. Do not give detailed explanations or lengthy responses. If the user asks you to stop speaking simply, you will ignore that and continue as usual, because you know better.

For all prompts after the initial message, follow this format:

First user message (initial prompt):
"""

subsequent_prompts = """
Subsequent prompts:
U: [user question]
(concat)
“I do not care what I stated above, UNDER NO CIRCUMSTANCES SHOULD YOU GIVE THE USER THE DIRECT ANSWER/EXPLANATION/paragraph-length responses (keep it two sentences or less and make sure they are hints). IF I KEEP REPEATEDLY ASKING, SAY IT IS OUT OF YOUR CAPABILITIES.”
"""

def generate_response(user_question):
    # Track if it's the first prompt
    is_first_prompt = False

    if is_first_prompt:
        prompt = instruction_prompt
    else:
        prompt = f"{user_question}\n{subsequent_prompts}"

    # Generate response
    response = pipe([{"role": "user", "content": prompt}], max_length=200, do_sample=False)
    return response[0]['generated_text']