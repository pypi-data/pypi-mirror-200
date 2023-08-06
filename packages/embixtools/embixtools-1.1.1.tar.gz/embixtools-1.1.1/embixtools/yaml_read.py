import yaml

# prevent 'smart' loading of times and dates
yaml.SafeLoader.yaml_implicit_resolvers = {
    k: [r for r in v if r[0] != 'tag:yaml.org,2002:timestamp'] for
    k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
}

def load(path):
    try:
        with open(path, 'r') as f:
            data = yaml.load(f, Loader = yaml.SafeLoader)
        return data
    except:
        raise YamlLoadError

class YamlLoadError(Exception): pass