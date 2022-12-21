import xml.etree.ElementTree as ET

class Configuration():

    def __init__(self, configuration="mask/configuration.cnf"):
        self.conf = configuration
        conf_doc = ET.parse(self.conf)
        root = conf_doc.getroot()
        self.entities_list = []
        for elem in root:
            if elem.tag == "plugins":
                for entities in elem:
                    entity = {}
                    for ent in entities:
                        entity[ent.tag] = ent.text
                    self.entities_list.append(entity)
            if elem.tag == "dataset":
                for ent in elem:
                    if ent.tag == "input_file_location":
                        self.input_file_location = ent.text
                    if ent.tag == "mask_input_file_location":
                        self.mask_input_file_location = ent.text
                    if ent.tag == "output_file_location":
                        self.output_file_location = ent.text
            if elem.tag == "model":
                for ent in elem:
                    if ent.tag == "trained_model":
                        self.trained_model = ent.text