from server.tasks import (
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