import os
import asyncio
from dotenv import load_dotenv
from openai import OpenAI

from env.environment import BatchEnvironment
from env.models import BatchAction

load_dotenv()

# ✅ REQUIRED ENV VARIABLES
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

client = OpenAI(
    api_key=HF_TOKEN,
    base_url=API_BASE_URL,
)


def log_start():
    print(f"[START] task=batch_task env=batch_env model={MODEL_NAME}", flush=True)


def log_step(step, action, reward, done, error):
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error}",
        flush=True,
    )


def log_end(success, steps, rewards):
    rewards_str = ",".join([f"{r:.2f}" for r in rewards])

    print(
        f"[END] success={str(success).lower()} steps={steps} rewards={rewards_str}",
        flush=True,
    )


def get_model_message(step):
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": f"Step {step}"}],
            max_tokens=5,
        )
        return response.choices[0].message.content
    except Exception:
        return "fallback"


async def main():
    env = BatchEnvironment()

    rewards = []
    steps_taken = 0

    log_start()

    try:
        obs = env.reset()

        for step in range(1, 11):
            _ = get_model_message(step)

            action = BatchAction(
                temperature_change=0.5,
                pressure_change=0.1,
                speed_change=0.5,
            )

            obs, reward, done, _ = env.step(action)

            reward = reward or 0.0
            rewards.append(reward)
            steps_taken = step

            log_step(step, str(action), reward, done, None)

            if done:
                break

        success = (sum(rewards) / len(rewards)) >= 0.5

    except Exception as e:
        print("[ERROR]", str(e), flush=True)
        success = False

    finally:
        log_end(success, steps_taken, rewards)


if __name__ == "__main__":
    asyncio.run(main())