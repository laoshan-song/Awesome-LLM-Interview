from dataclasses import dataclass


@dataclass
class BusinessKpiSnapshot:
    total_questions: int
    answered_questions: int
    human_handoffs: int
    accepted_ticket_suggestions: int
    total_ticket_suggestions: int
    total_cost: float

    @property
    def self_service_rate(self) -> float:
        if self.total_questions == 0:
            return 0.0
        return round(self.answered_questions / self.total_questions, 4)

    @property
    def handoff_rate(self) -> float:
        if self.total_questions == 0:
            return 0.0
        return round(self.human_handoffs / self.total_questions, 4)

    @property
    def ticket_acceptance_rate(self) -> float:
        if self.total_ticket_suggestions == 0:
            return 0.0
        return round(self.accepted_ticket_suggestions / self.total_ticket_suggestions, 4)

    @property
    def cost_per_question(self) -> float:
        if self.total_questions == 0:
            return 0.0
        return round(self.total_cost / self.total_questions, 6)
