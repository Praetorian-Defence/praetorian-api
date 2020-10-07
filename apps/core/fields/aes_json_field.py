import json

from apps.core.fields.aes_text_field import AesTextField


class AesJSONField(AesTextField):
    def __init__(self, *args, **kwargs):
        super(AesJSONField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        # when getting data
        decrypted_data = self.decrypt(value)
        return json.loads(decrypted_data)

    def get_prep_value(self, value):
        # when saving data
        if not value:
            return value
        if not isinstance(value, str):
            value = json.dumps(value)
        return self.encrypt(value)
