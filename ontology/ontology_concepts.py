from owlready2 import *


def fetch_concepts_from_ontology(ontology_path, class_name):
    # Load your ontology

    onto = get_ontology(ontology_path).load()

    # Get the class from the ontology
    disease_class = getattr(onto, class_name)
    # Extract color components
    color_components = disease_class.hasColor
    print(color_components)
    # Create a new list without the "tomdco2" prefix and "or" separation
    color_list = []

    # Iterate through each color class or individual and add to the list
    for color_expression in color_components:
        if isinstance(color_expression, Or):
            for color_class in color_expression.Classes:
                color_list.append(color_class)
        else:
            color_list.extend(color_expression.instances())

    # Extract the names of the color classes without the "tomdco2" prefix
    result_hasColor = [str(color).split('.')[-1] for color in color_list]
    # Remove duplicates from the list
    result_hasColor = list(set(result_hasColor))
    # Print the extracted color components
    print("Color List:", result_hasColor)


    #===========Symptom==============
    prop_symptom = onto.hasSymptom
    print("prop_symptom[onto[disease_class]]",prop_symptom[disease_class])
    # retutrn [tomato_disease_onto.BlightonLeaf]
    concept_symptom = str(prop_symptom[disease_class]).split('.')[-1][:-1]
    print("concept_symptom=",concept_symptom)

    #===========Shape==============
    prop_shape = onto.hasShape
    print("prop_shape[onto[disease_class]]",prop_shape[disease_class])
    concept_shape = str(prop_shape[disease_class]).split('.')[-1][:-1]
    print("concept_symptom=",concept_shape)
    ConceptsDictionary = {
    "hasShape": concept_shape,
    "hasColor": result_hasColor,
    "hasSymptom": concept_symptom
    }

    return ConceptsDictionary