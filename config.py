from configparser import ConfigParser


path = "Data/config.cfg"


# def create_config():
#    config = ConfigParser()
#    config.add_section("Settings")
#    config.set("Settings", "bot_token", "token")

#    with open(path, "w") as config_file:
#        config.write(config_file)


def add_in_config(key, param, value):
    config = ConfigParser()
    config.set(f"{key}", f"{param}", f"{value}")

    with open(path, "w") as config_file:
        config.write(config_file)


def get_config(key, what):
    config = ConfigParser()
    config.read(path)
    value = config.get(key, what)

    return value


def edit_config(key, setting, value):
    config = ConfigParser()
    config.read(path)

    config.set(key, setting, value)

    with open(path, "w") as config_file:
        config.write(config_file)
