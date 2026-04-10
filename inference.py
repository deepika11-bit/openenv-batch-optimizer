import os
import asyncio
from dotenv import load_dotenv
from openai import OpenAI

from env.environment import BatchEnvironment
from env.models import BatchAction

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")

TASK_NAME = "full_optimization"
BENCHMARK = "batch-optimizer-env"
MAX_STEPS = 10


def log_start():
    print(f"[START] task={TASK_NAME} env={BENCHMARK} model={MODEL_NAME}", flush=True)


def log_step(step, action, reward, done, error):
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error}",
        flush=True,
    )


def log_end(success, steps, score, rewards):
    rewards_str = ",".join([f"{r:.2f}" for r in rewards])
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}",
        flush=True,
    )


async def main():
    client = None
    if API_KEY:
        try:
            client = OpenAI(api_key=API_KEY, base_url=API_BASE_URL)
        except:
            pass

    env = BatchEnvironment()

    rewards = []
    steps_taken = 0

    log_start()

    try:
        obs = env.reset()

        for step in range(1, MAX_STEPS + 1):
            action = BatchAction(
                temperature_change=0.5,
                pressure_change=0.1,
                speed_change=0.5,
            )

            obs, reward, done, _ = env.step(action)

            reward = reward or 0.0
            rewards.append(reward)
            steps_taken = step

            log_step(
                step=step,
                action=str(action),
                reward=reward,
                done=done,
                error="null",
            )

            if done:
                break

        score = sum(rewards) / len(rewards)
        score = max(0.0, min(1.0, score))

        success = score >= 0.5

    except Exception as e:
        print("[ERROR]", str(e), flush=True)
        success = False
        score = 0.0

    finally:
        log_end(success, steps_taken, score, rewards)


if __name__ == "__main__":
    asyncio.run(main())