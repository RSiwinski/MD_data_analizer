import importlib.metadata

for dist in importlib.metadata.distributions():
    print(f"{dist.metadata['Name']}=={dist.version}")
