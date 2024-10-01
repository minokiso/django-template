from rest_framework.fields import SkipField
from rest_framework.serializers import ModelSerializer


class ModelSerializerPlus(ModelSerializer):
    def to_internal_value(self, data):
        validated_data = super().to_internal_value(data)

        for field_name, field in self.fields.items():
            if validated_data.get(field_name) is None:
                try:
                    default = field.get_default()
                    validated_data[field_name] = default
                except SkipField:
                    continue

        return validated_data
