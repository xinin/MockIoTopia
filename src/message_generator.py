import sys
import traceback
import random
import time
from datetime import datetime
import math

from exceptions import FieldSyntaxError, FieldNotSupportedError


def generate_message(config, previous_message, is_array=False):
    current_message = [] if is_array else {}

    try:
        for field_config in config.get("Fields", []):
            field_name = field_config.get("Name")

            previuos_message_field = None
            if previous_message is not None:
                if field_name is not None:
                    previuos_message_field = previous_message.get(field_name)
                else:
                    previuos_message_field = previous_message[len(current_message)]

            field_type = field_config["Type"]
            if field_type in ("int", "float"):
                new_value = number_field(field_config, previuos_message_field, field_type == "int")
            elif field_type == "boolean":
                new_value = boolean_field(field_config, previuos_message_field)
            elif field_type == "string":
                new_value = string_field(field_config)
            elif field_type == "date":
                new_value = date_field(field_config)
            elif field_type == "GPS":
                new_value = gps_field(field_config, previuos_message_field)
            elif field_type in ("object", "array"):
                new_value = generate_message(field_config, previuos_message_field, field_type == "array")
            else:
                raise FieldNotSupportedError(field_config, "Field not supported")

            if field_name:
                current_message[field_name] = new_value
            else:
                current_message.append(new_value)

    except (KeyError, FieldSyntaxError):
        print("\nERROR parsing Fields configuration")
        traceback.print_exc()
        sys.exit()

    return current_message

def number_field(field_config, previuos_message, is_int):
    try:
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
            field_value = previuos_message
            if random.random() < behaviour["VariationProbability"]:
                variation = previuos_message * behaviour["VariationMagnitude"]
                field_value += random.choice([-1, 1]) * variation
                field_value = max(_min, min(_max, field_value))

        if is_int:
            #INT
            return round(field_value)
        else:  
            #FLOAT
            return round(field_value, decimals)
    except:
        raise FieldSyntaxError(field_config, "Field Sintaxt Error")

def boolean_field(field_config, previuos_message):
    try:
        behaviour = field_config["Behaviour"]
        field_value = None

        if behaviour["Type"] == "Random":
            return random.choice([1, 0])
        else:
            if previuos_message == None:
                return behaviour["Default"]
            else:
                field_value = behaviour["Default"]
                if random.random() < behaviour["VariationProbability"]:
                    field_value = 1 - field_value
                return field_value

    except:
        raise FieldSyntaxError(field_config, "Field Sintaxt Error")


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
        behaviour = field_config["Behaviour"]

        if behaviour["Type"] == "Random":
            return generate_random_sentence(behaviour["Length"])
        else:          
            return behaviour["Default"]

    except:
        raise FieldSyntaxError(field_config, "Field Sintaxt Error")
    

def date_field(field_config):
    try:
        behaviour = field_config["Behaviour"]
        
        if behaviour["Type"] == "UnixEpoch":
            return int(time.time())
        elif behaviour["Type"] == "UnixEpochMilis":
            return int(time.time() * 1000)
        elif behaviour["Type"] == "ISO8601":
            return datetime.utcnow().isoformat()
        
    except:
        raise FieldSyntaxError(field_config, "Field Sintaxt Error")

def ensure_new_x_y_inside_radius(org_x, org_y, new_x, new_y,rad):
    distance = math.sqrt((new_x - org_x)**2 + (new_y - org_y)**2)
    return distance <= rad

def generate_coordinate_variance(field_value_x,field_value_y,var_magnitude):
    variation_x = field_value_x * var_magnitude
    variation_y = field_value_y * var_magnitude
    field_value_x += random.choice([-1, 1]) * variation_x
    field_value_y += random.choice([-1, 1]) * variation_y
    return field_value_x, field_value_y

def generate_random_coordinates(config_x,config_y, max_rad):
    angle = random.uniform(0, 2 * math.pi)
    radius = random.uniform(0, max_rad)

    new_x = config_x + radius * math.cos(angle)
    new_y = config_y + radius * math.sin(angle)

    return new_x, new_y

def current_index_distance_based_(org_x, org_y, path):
    min_distance = float('inf')
    step_index = None
    
    for i, (x, y) in enumerate(path):
        distance = math.sqrt((org_x - x)**2 + (org_y - y)**2)
        if distance < min_distance:
            min_distance = distance
            step_index = i
    
    return step_index


def delta_coordinates(org_x, org_y,path,increment,):
    nearest_index = current_index_distance_based_(org_x, org_y, path)
        
    next_ind=(nearest_index+1)%len(path)

    increment_x = random.uniform(0, increment)  
    increment_y = random.uniform(0, increment)
    
    new_org_x = org_x + increment_x*(path[next_ind][0]-org_x)
    new_org_y = org_y + increment_y*(path[next_ind][1]-org_y)
    
    return new_org_x, new_org_y

def gps_field(field_config, previous_message):
    try:
        behaviour = field_config["Behaviour"]
        max_rad=field_config['Max_radius']
        config_x=field_config['X']
        config_y=field_config['Y']
        time.sleep(field_config['Time_between_sends'])

        if behaviour["Type"] == "Random":
            x, y= generate_random_coordinates(config_x, config_y, max_rad)
            return x, y
        elif behaviour["Type"] == "Static":
            if previous_message is not None:
                org_x, org_y = previous_message
            else:
                org_x, org_y = config_x, config_y

            if random.random() < behaviour["VariationProbability"]:
                x,y=generate_coordinate_variance(org_x, org_y,behaviour['VariationMagnitude'])
                if not ensure_new_x_y_inside_radius(config_x,config_y,org_x,org_y,max_rad):
                    x,y=config_x,config_y
                return x, y
            else:
                return org_x,org_y

        elif behaviour["Type"] == "Path":
            if previous_message is not None:
                org_x, org_y = previous_message
            else:
                org_x, org_y=config_x,config_y

            x, y=delta_coordinates(org_x, org_y,behaviour['Array_path'],behaviour['Increment'])
            if random.random() < behaviour["VariationProbability"]:
                x,y=generate_coordinate_variance(org_x, org_y,behaviour['VariationMagnitude'])
                return x, y

            return x, y
    except:
        raise FieldSyntaxError(field_config, "Field Sintaxt Error")




