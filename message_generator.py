import sys
import traceback
import random
import time
from datetime import datetime



from exceptions import FieldSintaxError, FieldNotSupportedError


def generate_message(config, previuos_message):

    current_message = {}

    try:
        for field_config in config["Fields"]:
            try:
                if (field_config["Type"] == "int"):
                    current_message.update(number_field(field_config, previuos_message, True))
                elif (field_config["Type"] == "float"):
                    current_message.update(number_field(field_config, previuos_message, False))
                elif (field_config["Type"] == "boolean"):
                    current_message.update(boolean_field(field_config, previuos_message))
                elif (field_config["Type"] == "string"):
                    current_message.update(string_field(field_config))
                elif (field_config["Type"] == "date"):
                    current_message.update(date_field(field_config))
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

def number_field(field_config, previuos_message, is_int):
    try:
        name = field_config["Name"]
        _max = field_config["Max"]
        _min = field_config["Min"]
        behaviour = field_config["Behaviour"]
        decimals = None
        field_value = None

        if not is_int:
            decimals = field_config["Decimals"]

        if previuos_message == None or behaviour["Type"] == "Random":
            if is_int:
                #INT
                field_value = random.randint(_min, _max)
            else:  
                #FLOAT
                field_value = round(random.uniform(_min, _max), decimals)

        else:
            field_value = previuos_message[name]
            if random.random() < behaviour["VariationProbability"]:
                variation = previuos_message[name] * behaviour["VariationMagnitude"]
                field_value += random.choice([-1, 1]) * variation
                field_value = max(_min, min(_max, field_value))

        if is_int:
            #INT
            return {name: round(field_value)}
        else:  
            #FLOAT
            return {name: round(field_value, decimals)}
    except:
        raise FieldSintaxError(field_config, "Field Sintaxt Error")

def boolean_field(field_config, previuos_message):
    try:
        name = field_config["Name"]
        behaviour = field_config["Behaviour"]
        field_value = None

        if behaviour["Type"] == "Random":
            return {name: random.choice([1, 0])}
        else:
            if previuos_message == None:
                return {name: behaviour["Default"]}
            else:
                field_value = behaviour["Default"]
                if random.random() < behaviour["VariationProbability"]:
                    field_value = 1 - field_value
                return {name: field_value}

    except:
        raise FieldSintaxError(field_config, "Field Sintaxt Error")


def generate_random_sentence(total_characters):

    word_list = [
    "lorem", "ipsum", "dolor", "sit", "amet", "consectetur",
    "adipiscing", "elit", "sed", "do", "eiusmod", "tempor",
    "incididunt", "ut", "labore", "et", "dolore", "magna", "aliqua",
    "enim", "ad", "minim", "veniam", "quis", "nostrud", "exercitation",
    "ullamco", "laboris", "nisi", "aliquip", "ea",
    "commodo", "consequat", "duis", "aute", "irure", "in", "reprehenderit",
    "voluptate", "velit", "esse", "cillum", "fugiat", "nulla", "pariatur",
    "excepteur", "sint", "occaecat", "cupidatat", "non", "proident", "sunt",
    "culpa", "qui", "officia", "deserunt", "mollit", "anim", "id", "est",
    "topping", "jelly", "beans", "pudding", "gummies", "apple", "pie", "sesame", 
    "snaps", "tiramisu", "dessert", "chupa", "chups", "brownie", "soufflé", "croissant", 
    "halvah", "bear", "claw", "gingerbread", "tart", "lollipop", "toffee", "lemon", "drops", 
    "chocolate", "cake", "muffin", "cupcake", "dragée", "candy", "canes", "tootsie", "roll", 
    "fruitcake", "bonbon", "shortbread", "cheesecake", "danish", "sugar", "plum", "biscuit", 
    "donut", "oat", "wafer", "icing", "carrot", "o", "ice", "cream", "sweet", "macaroon", 
    "jujubes", "carrot", "pastry", "bar", "powder", "carrot", "a", "e", "i"
]
    generated_text = ""
    while len(generated_text) < total_characters:
        word = random.choice(word_list)
        if generated_text:
            generated_text += " " + word
        else:
            generated_text = word
    return generated_text[:total_characters]


def string_field(field_config):
    try:
        name = field_config["Name"]
        behaviour = field_config["Behaviour"]

        if behaviour["Type"] == "Random":
            return {name: generate_random_sentence(behaviour["Length"])}
        else:          
            return {name: behaviour["Default"]}

    except:
        raise FieldSintaxError(field_config, "Field Sintaxt Error")
    

def date_field(field_config):
    try:
        name = field_config["Name"]
        behaviour = field_config["Behaviour"]
        
        if behaviour["Type"] == "UnixEpoch":
            return {name: int(time.time())}
        elif behaviour["Type"] == "UnixEpochMilis":
            return {name: int(time.time() * 1000)}
        elif behaviour["Type"] == "ISO8601":
            return {name: datetime.utcnow().isoformat()}
        
    except:
        raise FieldSintaxError(field_config, "Field Sintaxt Error")


