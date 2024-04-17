def data_mapper(prompt_template:str, kwargs:dict ):
    return prompt_template.format(**kwargs)