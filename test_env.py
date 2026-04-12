from environment import BatchEnvironment
from models import BatchAction

env = BatchEnvironment()
obs = env.reset()

print("Initial:", obs)

for i in range(5):
    action = BatchAction(
        temperature_change=1,
        pressure_change=0.1,
        speed_change=2
    )

    obs, reward, done, _ = env.step(action)

    print(f"Step {i+1}:", obs, "Reward:", reward)

    if done:
        break