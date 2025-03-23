import time
import requests
import logging

# Hyperbolic API configuration
HYPERBOLIC_API_URL = "https://api.hyperbolic.xyz/v1/chat/completions"
HYPERBOLIC_API_KEY = "$API_KEY"  # Replace with your API key
MODEL = "meta-llama/Llama-3.3-70B-Instruct"      # Or specify your desired model
MAX_TOKENS = 2048
TEMPERATURE = 0.7
TOP_P = 0.9
DELAY_BETWEEN_QUESTIONS = 30  # Delay between questions in seconds

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_response(question: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {HYPERBOLIC_API_KEY}"
    }
    data = {
        "messages": [{"role": "user", "content": question}],
        "model": MODEL,
        "max_tokens": MAX_TOKENS,
        "temperature": TEMPERATURE,
        "top_p": TOP_P
    }
    response = requests.post(HYPERBOLIC_API_URL, headers=headers, json=data, timeout=30)
    response.raise_for_status()
    json_response = response.json()
    # Assuming the response structure is similar to the OpenAI API:
    return json_response.get("choices", [{}])[0].get("message", {}).get("content", "No answer")

def main():
    # Reading questions from the "questions.txt" file
    try:
        with open("questions.txt", "r", encoding="utf-8") as f:
            questions = [line.strip() for line in f if line.strip()]
    except Exception as e:
        logger.error(f"Error reading the questions.txt file: {e}")
        return

    if not questions:
        logger.error("There are no questions in the questions.txt file.")
        return

    index = 0
    while True:
        question = questions[index]
        logger.info(f"Question #{index+1}: {question}")
        try:
            answer = get_response(question)
            logger.info(f"Answer: {answer}")
        except Exception as e:
            logger.error(f"Error while getting the answer for question: {question}\n{e}")
        index = (index + 1) % len(questions)
        time.sleep(DELAY_BETWEEN_QUESTIONS)

if __name__ == "__main__":
    main()
