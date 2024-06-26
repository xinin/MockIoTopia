import sys
import traceback
import random
import time
from datetime import datetime
import math

from exceptions import FieldSyntaxError, FieldNotSupportedError


index=1

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

def ensure_new_x_y_inside_radius(config_x, config_y, new_x, new_y,rad):
    distance = math.sqrt((new_x - config_x)**2 + (new_y - config_y)**2)
    return distance <= rad

def generate_coordinate_variance(field_value_x,field_value_y,var_magnitude):
    variation_x = field_value_x * var_magnitude
    variation_y = field_value_y * var_magnitude
    field_value_x += random.choice([-1, 1]) * variation_x
    field_value_y += random.choice([-1, 1]) * variation_y
    return field_value_x, field_value_y

def generate_random_coordinates(config_x,config_y, org_x,org_y, max_rad, behaviour):
    increment=behaviour['Increment']
    angle = random.uniform(0, 2 * math.pi)
    radius = random.uniform(1, increment)

    new_x = org_x + radius * math.cos(angle)
    new_y = org_y + radius * math.sin(angle)
    while not ensure_new_x_y_inside_radius(config_x, config_y, new_x,new_y,max_rad):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(1, increment)

        new_x = org_x + radius * math.cos(angle)
        new_y = org_y + radius * math.sin(angle)

    return new_x, new_y

def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def get_target_point(current_position, route, threshold):
    global index
    step=index
    if euclidean_distance(current_position, route[step]) < threshold:
        target_index = (step + 1) % len(route)
    else:
        target_index = step


    index=target_index
    return route[target_index]

def move_to_target(current_position, target_point, increment):
    direction = (target_point[0] - current_position[0], target_point[1] - current_position[1])
    distance_to_target = euclidean_distance(current_position, target_point)
    if distance_to_target < increment:
        new_position = target_point
    else:
        scale = increment / distance_to_target
        new_position = (current_position[0] + direction[0] * scale, current_position[1] + direction[1] * scale)
    return new_position

def gps_field(field_config, previous_message):
    try:
        behaviour = field_config["Behaviour"]
        max_rad=field_config['Max_radius']
        config_x=field_config['X']
        config_y=field_config['Y']
        time.sleep(field_config['Time_between_sends'])
        if previous_message is not None:
            org_x, org_y = previous_message
        else:
            org_x, org_y=config_x,config_y
        
        if behaviour["Type"] == "Random":
            x, y= generate_random_coordinates(config_x, config_y, org_x, org_y, max_rad, behaviour)
            return x, y
        elif behaviour["Type"] == "Static":
            if random.random() < behaviour["VariationProbability"]:
                x,y=generate_coordinate_variance(org_x, org_y,behaviour['VariationMagnitude'])
                if not ensure_new_x_y_inside_radius(config_x,config_y,org_x,org_y,max_rad):
                    x,y=config_x,config_y
                return x, y
            else:
                return org_x,org_y

        elif behaviour["Type"] == "Path":
            target=get_target_point((org_x,org_y), behaviour['Array_path'], threshold=1e-5)
            x, y=move_to_target((org_x,org_y), target, behaviour['Increment'])
            return x, y
    except:
        raise FieldSyntaxError(field_config, "Field Sintaxt Error")




