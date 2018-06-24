import yaml as pyyaml

class Yaml:
    def __init__(self):
        pass

    def readYaml(self, yamlFile: str) -> dict:
        """
        Read a yaml file and spits out the content in a dictionary format

        Parameters
        ----------
        yamlFile : str
            string of the name of the yaml file you want to parse

        Returns
        -------
        yamlDictionary : dict
            dictionary equivalent of the yaml file
        """
        with open(yamlFile, 'r') as stream:
            try:
                yamlDictionary = pyyaml.load(stream)
            except pyyaml.YAMLError as exception:
                print(exception)

        return yamlDictionary
