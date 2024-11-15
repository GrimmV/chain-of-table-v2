from pydantic import BaseModel, Field, create_model


class ReasoningStep(BaseModel):
    step: int = Field(description="The step number")
    subquestion: str = Field(description="Subquestion to solve")
    procedure: str = Field(
        description="""Any intermediate computation
        that was done in the reasoning process. Leave
        empty if no computation is needed""",
    )
    result: str


class StructuredReasoningBaseResponse(BaseModel):
    reasoning: list[ReasoningStep] = Field(
        description="reasoning steps to derive answer",
    )

def generate_structured_response(response_model: BaseModel) -> BaseModel:
    StructuredReasoningResponse = create_model(
        "StructuredReasoningResponse",
        final_response=(response_model, ...),
        __base__=StructuredReasoningBaseResponse
    )
    
    return StructuredReasoningResponse
