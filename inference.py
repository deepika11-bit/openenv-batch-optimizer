import asyncio
from tasks import TASKS


def log_start():
    print("[START]", flush=True)


def log_end(success, steps, score, rewards):
    print(
        f"[END] success={success} steps={steps} score={score:.4f} rewards={rewards}",
        flush=True,
    )


async def main():
    log_start()

    rewards = []
    steps = 0

    try:
        # 🔥 RUN ALL TASKS
        for task_name, TaskClass in TASKS.items():
            task = TaskClass()

            print(f"[RUNNING TASK] {task_name}", flush=True)

            score = task.run()

            # ensure valid range again (safety)
            if score <= 0:
                score = 0.01
            elif score >= 1:
                score = 0.99

            print(f"[TASK RESULT] {task_name} score={score}", flush=True)

            rewards.append(score)
            steps += 1

        # 🔥 FINAL SCORE (average of tasks)
        final_score = sum(rewards) / max(1, len(rewards))

        success = final_score > 0.5

    except Exception as e:
        print("[ERROR]", str(e), flush=True)
        final_score = 0.01
        success = False

    finally:
        log_end(
            success=success,
            steps=steps,
            score=final_score,
            rewards=rewards,
        )


if __name__ == "__main__":
    asyncio.run(main())