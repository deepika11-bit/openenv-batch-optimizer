from env.tasks import (
    EnergyOptimizationTask,
    YieldEnergyTask,
    FullOptimizationTask,
)

def get_tasks():
    return [
        EnergyOptimizationTask(),
        YieldEnergyTask(),
        FullOptimizationTask(),
    ]