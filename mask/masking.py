from os import listdir, path, mkdir
from os.path import isfile, join
import importlib
from nerm.configuration import Configuration
from brat_parser import get_entities_relations_attributes_groups

def get_data_sequences(mask_input_file_location, filename):
  ann_data = get_entities_relations_attributes_groups( mask_input_file_location + filename + ".ann")
  sequences = []
  for key,values in ann_data[0].items():
    data =(values.text,values.type, values.span[0][0],values.span[0][1])
    sequences.append(data)
  return sequences


def masking_process(type,result,new_text):
    for i in range(0, len(result)):
        if type["masking_type"] == "Mask":
            masking_class = type['masking_class']
            plugin_module = importlib.import_module("mask.masking_plugins." + masking_class)
            class_masking = getattr(plugin_module, masking_class)
            masking_instance = class_masking()
            
        if result[i][1] == type["entity_name"]:
            if type["masking_type"] == "Redact":
                new_token = "XXX"
            elif type["masking_type"] == "Mask":
                new_token = masking_instance.mask(result[i][0])
            old_token = result[i][0]
            new_text = new_text.replace(old_token, new_token)
    return new_text


def apply_masking(mask_input_file_location, filename, text, plugins):
    new_text = text
    for type in plugins:
        result = get_data_sequences(mask_input_file_location, filename[:-4])
        new_text = masking_process(type,result,new_text)
    return new_text


def main():
    print("\n Welcome to NERM Group Masking \n")

    cf = Configuration()
    input_file_location = cf.mask_input_file_location

    data = [f for f in listdir(input_file_location) if f.startswith('unannotated_texts')]
    print(data)
    if (len(data)>0):
        input_file_location = input_file_location + data[0] + "/brat/deploy/"
    
        data = [f for f in listdir(input_file_location) if isfile(
            join(input_file_location, f))]
        print(data)

    plugins = []
    for entity in cf.entities_list:
      masking_type = entity['masking_type']
      entity_name = entity['entity_name']
      if masking_type == "Redact":
          masking_class = ""
      else:
          masking_class = entity['masking_class']

      plugins.append({"masking_type":masking_type, "entity_name":entity_name, "masking_class":masking_class})
    
    for file in data:
        if file.endswith(".txt"):
            text = open(input_file_location + file, 'r').read()
            new_text = apply_masking(input_file_location, file, text,plugins)

            # Write the output
            if not path.exists(cf.output_file_location):
                mkdir(cf.output_file_location)

            file_handler = open(cf.output_file_location + file, "w")
            file_handler.write(new_text)
            file_handler.close()

if __name__=="__main__":
    main()
