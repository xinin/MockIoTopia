import sys
import traceback
import random


from exceptions import FieldSintaxError, FieldNotSupportedError


def generate_message(config, previuos_message):

    current_message = {}

    try:
        for field_config in config["Fields"]:
            try:
                if (field_config["Type"] == "int"):
                    current_message.update(int_field(field_config, previuos_message))
            except FieldSintaxError as e:
                traceback.print_exc()
                sys.exit()
            except:
                raise FieldNotSupportedError(field_config, "Field not supported")
    except(KeyError):
        print("\nERROR parsing Fields configuration")
        traceback.print_exc()
        sys.exit()

    return current_message

def int_field(field_config, previuos_message):
    try:
        name = field_config["Name"]
        _max = field_config["Max"]
        _min = field_config["Min"]
        behaviour = field_config["Behaviour"]

        field_value = None
        if behaviour["Type"] == "Random":
            field_value = random.randint(_min, _max)

        else:
            if previuos_message == None:
                field_value = random.randint(_min, _max)
            else:
                field_value = previuos_message[name]
                if random.random() < behaviour["VariationProbability"]:
                    variation = previuos_message[name] * behaviour["VariationMagnitude"]
                    field_value += random.choice([-1, 1]) * variation
                    field_value = max(_min, min(_max, field_value))

        field = {name: round(field_value)}

        return field
    except:
        raise FieldSintaxError(field_config, "Field Sintaxt Error")

 







