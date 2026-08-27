# ============================================================
# COST TRACKER
# ============================================================

class CostTracker:

    def __init__(self):
        self.requests = 0
        self.tokens = 0
        self.cost = 0.0
        self.history = []

    # --------------------------------------------------------
    # TRACK REQUEST
    # --------------------------------------------------------
    def track(
        self,
        agent_name,
        model_type,
        prompt_tokens=0,
        completion_tokens=0
    ):
        """
        Track one LLM request.

        Ollama runs locally, so the actual API cost is $0.
        We still track token usage for monitoring and
        cost-optimization analysis.
        """

        try:
            prompt_tokens = int(prompt_tokens or 0)
            completion_tokens = int(completion_tokens or 0)

        except (TypeError, ValueError):
            prompt_tokens = 0
            completion_tokens = 0

        total_tokens = (
            prompt_tokens +
            completion_tokens
        )

        # Count request
        self.requests += 1

        # Count tokens
        self.tokens += total_tokens

        # Local Ollama = $0
        request_cost = 0.0

        self.cost += request_cost

        record = {
            "agent": str(agent_name),
            "model_type": str(model_type),
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "cost": request_cost
        }

        self.history.append(record)

        print(
            f"💰 Cost tracked | "
            f"Agent: {agent_name} | "
            f"Model: {model_type} | "
            f"Tokens: {total_tokens}"
        )

        return record

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------
    def summary(self):
        """
        Return current cost statistics.
        """

        return {
            "requests": self.requests,
            "tokens": self.tokens,
            "cost": round(self.cost, 6)
        }

    # --------------------------------------------------------
    # HISTORY
    # --------------------------------------------------------
    def get_history(self):
        """
        Return all tracked requests.
        """

        return self.history

    # --------------------------------------------------------
    # RESET
    # --------------------------------------------------------
    def reset(self):
        """
        Reset all cost statistics.
        """

        self.requests = 0
        self.tokens = 0
        self.cost = 0.0
        self.history = []