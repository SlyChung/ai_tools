"""
PlanMemory is a class that manages the plan memory of the the orchestrator.

Has a bit more power than the task memory.
Meant to be a persistent memory that can be used to track the plan and its steps.
A new plan memory is created when a new plan is created.?

See the design document for more details:

Contracted Fields:
- plan_id: str
- plan_objective: str
- plan_steps: Dict[str, Any] # {step_id: {step_name: str, step_description: str, step_status: str, step_progress: float}
- plan_status: str
- plan_progress: float
"""

from ai_tools.working_memory.Memory import WorkingMemory

class PlanMemory(WorkingMemory):
    def __init__(self):
        super().__init__()

    def add_plan(self, plan: str) -> None:
        """
        Add a plan to the working memory
        """
        pass