from pydantic import BaseModel, Field, model_validator


class TaskSchema(BaseModel):
    id: int | None = None
    name: str | None = None
    pomodoro_count: int | None = None
    # category_id: int = Field(alias='category_id')  # для входных параметров используется alias
    category_id: int

    class Config:
        from_attributes: bool = True

    @model_validator(mode='after')
    def check_name_or_pomodoro_count_is_not_none(self):
        # print(self)
        if self.name is None and self.pomodoro_count is None:
            raise ValueError('TaskSchema "name" and "pomodoro_count" cannot be both None')
        return self

    # @field_validator('name', 'pomodoro_count')
    # @classmethod
    # def check_name_is_not_none(cls, value: Optional[str]):
    #     print(value)
    #     if value is None:
    #         raise ValueError('TaskSchema name cannot be None')
