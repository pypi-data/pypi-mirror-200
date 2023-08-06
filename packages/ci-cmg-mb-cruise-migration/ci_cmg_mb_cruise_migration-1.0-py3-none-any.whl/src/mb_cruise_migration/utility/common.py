def dict_value_or_none(dictionary, key):
    return dictionary[key] if key in dictionary else None


def multiple_values_in_survey_instrument(survey_instrument) -> bool:
    instruments = survey_instrument.split(";")
    return len(instruments) != 1


def strip_none(may_have_nones: list):
    return [item for item in may_have_nones if item is not None]
