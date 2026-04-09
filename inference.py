import os
import asyncio
from dotenv import load_dotenv
from openai import OpenAI

from env.environment import BatchEnvironment
from env.models import BatchAction

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def log_start():
    print("[START]", flush=True)


def log_step(step, action, reward, done, error):
    print(
        f"[STEP] step={step} action={action} reward={reward:.4f} done={done} error={error}",
        flush=True,
    )


def log_end(success, steps, score, rewards):
    print(
        f"[END] success={success} steps={steps} score={score:.4f} rewards={rewards}",
        flush=True,
    )


def get_model_message(client, step, obs, last_reward):
    try:
        if client is None:
            return "no-client"

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are optimizing a manufacturing process."},
                {"role": "user", "content": f"Step {step}, last reward {last_reward}"}
            ],
            max_tokens=5,
        )
        return response.choices[0].message.content
    except Exception as e:
        print("[MODEL ERROR]", str(e), flush=True)
        return "fallback"


async def main():
    # ✅ Safe client creation
    client = None
    if OPENAI_API_KEY:
        try:
            client = OpenAI(
                api_key=OPENAI_API_KEY,
                base_url=API_BASE_URL,
            )
        except Exception as e:
            print("[CLIENT ERROR]", str(e), flush=True)

    env = BatchEnvironment()

    MAX_STEPS = 10
    MAX_TOTAL_REWARD = 10
    SUCCESS_SCORE_THRESHOLD = 0.5

    rewards = []
    steps_taken = 0
    success = False
    score = 0.0

    log_start()

    try:
        obs = env.reset()
        last_reward = 0.0

        for step in range(1, MAX_STEPS + 1):
            # ✅ Safe model call
            _ = get_model_message(client, step, obs, last_reward)

            action = BatchAction(
                temperature_change=0.5,
                pressure_change=0.1,
                speed_change=0.5,
            )

            obs, reward, done, _ = env.step(action)

            reward = reward or 0.0

            rewards.append(reward)
            steps_taken = step
            last_reward = reward

            log_step(
                step=step,
                action=str(action),
                reward=reward,
                done=done,
                error=None,
            )

            if done:
                break

        score = sum(rewards) / MAX_TOTAL_REWARD
        score = max(0.0, min(1.0, score))

        success = score >= SUCCESS_SCORE_THRESHOLD

    except Exception as e:
        print("[ERROR]", str(e), flush=True)

    finally:
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)


if __name__ == "__main__":
    asyncio.run(main())