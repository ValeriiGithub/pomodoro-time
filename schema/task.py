from pydantic import BaseModel, Field, field_validator, model_validator


class Task(BaseModel):
    id: int
    name: str | None = None
    pomodoro_count: int | None = None
    category_id: int = Field(alias='category_id')   # для входных параметров используется alias

    @model_validator(mode='after')
    def check_name_is_not_none(self):
        # print(self)
        if self.name is None and self.pomodoro_count is None:
            raise ValueError('Task name and pomodoro count cannot be both None')
        return self

    # @field_validator('name', 'pomodoro_count')
    # @classmethod
    # def check_name_is_not_none(cls, value: Optional[str]):
    #     print(value)
    #     if value is None:
    #         raise ValueError('Task name cannot be None')
    