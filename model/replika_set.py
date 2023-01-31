from .data_set_an import BOT_CONFIG_EN
from .data_set_ru import BOT_CONFIG_RU


def create_replica_set():
    list_intens = [key for key, val in BOT_CONFIG_EN["intents"].items()]
    dict_itens = dict()
    for intens in list_intens:
        dict_itens[intens] = join_dict_intents(BOT_CONFIG_RU['intents'][intens], BOT_CONFIG_EN['intents'][intens])
    return {"intents": dict_itens}

def join_dict_intents(d:dict, c:dict):
    for k, v in d.items():
        if k in c:
            c[k].extend(v)
        else:
            c[k] = v
    return c

data_set =  create_replica_set()
