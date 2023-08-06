from datetime import date, datetime
import pydantic
import pendulum


class BaseModel(pydantic.BaseModel):
    @pydantic.validator('*', pre=True)
    def validate(cls, value, values, config, field: pydantic.fields.ModelField):
        if field.type_ in (date, datetime) and type(value) is str:
            value = datetime.fromisoformat(pendulum.parser.parse(value).to_datetime_string())
        
        return value
    
    class Config:
        json_encoders = {
            date: lambda dt: dt.isoformat()
        }
