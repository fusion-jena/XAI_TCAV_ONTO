# Import necessary libraries
import os
import random
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import tcav.activation_generator as act_gen
import tcav.cav as cav
import tcav.model  as model
import tcav.tcav as tcav
import tcav.utils as utils
import tcav.utils_plot as utils_plot # utils_plot requires matplotlib
from ontology.ontology_concepts import fetch_concepts_from_ontology
from generate_concepts.generate_color import generate_color_concept
from generate_concepts.generate_shape import generate_shape_concept
from generate_concepts.generate_symptom import generate_symptom_concept


'''
====================================================
# Parameters :
    source_dir: where images of concepts, target class, segmented images for targect class from test set,
        and random images (negative samples when learning CAVs) exist. Each should be a sub-folder within this directory
    cav_dir: directory to store CAVs 
    target: names of the target class that you want to investigate/ a list of the target classes in our use case is given in class_labels
    bottlenecks: list of bottleneck names (intermediate layers in your model) that you want to use for TCAV. These names are defined in the model wrapper below.
    ontology_path: The path for the tomato disease ontology
    concepts_dict : the concepts extracted from the ontology for the given target class
    concepts (strings) - these are folder names in source_dir ( these concepts are extracted from ontology and generated automatically as images)
====================================================
'''


class_labels =["BacterialSpot", "EarlyBlight", "Healthy", "LateBlight", "LeafMold" "MosaicVirus", "SeptoriaLeafSpot", "TargetSpot" , "TwoSpottedSpiderMite", "YellowLeafCurlVirus"]
model_to_run = 'inception_v3' 
working_dir = './source_dir/working'
activation_dir =  working_dir+ '/activations/'
cav_dir = working_dir + '/cavs/'

source_dir = './source_dir/'
segmented_images_dir = source_dir+ '/segmentedtarget/'
bottlenecks = ['mixed8']
utils.make_dir_if_not_exists(activation_dir)
utils.make_dir_if_not_exists(working_dir)
utils.make_dir_if_not_exists(cav_dir)
alphas = [0.1]

target="BacterialSpot"

bottlenecks = ['mixed8']

#Get Concepts from ontology for the chosen target class
ontology_path ='./ontology/TomatoDCO.owl'
concepts_dict = fetch_concepts_from_ontology(ontology_path,target)

hasColor_concepts=concepts_dict["hasColor"]
print(hasColor_concepts)
hasShape_concepts=[concepts_dict["hasShape"]]
print(hasShape_concepts)
hasSymptom_concepts=[concepts_dict["hasSymptom"]]
print(hasSymptom_concepts)

# Generate concepts automatically
# we need to check if concepts are already generated for the given class if not than we will generate them

for color in hasColor_concepts:
    # Check if the folder for the color exists
    print(f"Generating images for concept: {color}")
    color_folder = os.path.join(source_dir, color)
    
    if not os.path.exists(color_folder):
        # If it doesn't exist, create the folder
        os.mkdir(color_folder)
        print(f"Folder for {color} created.")
        # Call the generate_color_concept function
        generate_color_concept(color, source_dir)
    else:
        print(f"Folder for {color} already exists.")

for shape in hasShape_concepts:
    print('shape',shape)
    # Check if the folder for the color exists
    shape_folder = os.path.join(source_dir, shape)
    if not os.path.exists(shape_folder):
        # If it doesn't exist, create the folder
        os.mkdir(shape_folder)
        print(f"Folder for {shape} created.")
        # Call the generate_shape_concept function
        generate_shape_concept(segmented_images_dir,shape_folder)
    else:
        print(f"Folder for {shape} already exists.")
        
for symptom in hasSymptom_concepts:
    # Check if the folder for the color exists
    symptom_folder = os.path.join(source_dir,symptom)
    if not os.path.exists(symptom_folder):
        # If it doesn't exist, create the folder
        os.mkdir(symptom_folder)
        print(f"Folder for {symptom} created.")
        # Call the generate_symptom_concept function
        generate_symptom_concept(source_dir,segmented_images_dir, symptom)
    else:
        print(f"Folder for {symptom} already exists.")

concepts=[]
#add colors concepts and other concepts extracted from the ontology to the list of concepts 
concepts = hasColor_concepts+hasShape_concepts+hasSymptom_concepts

print('concepts to check', concepts)


# Create TensorFlow session.
sess = utils.create_session()

# GRAPH_PATH is where the trained model is stored.
GRAPH_PATH = 'C:/Users/admin/Desktop/documentsgithub/source_dir/inceptionv3_model.h5'

LABEL_PATH = source_dir + "/graph_label_strings.txt"

mymodel = model.KerasModelWrapper(sess,
                                  GRAPH_PATH,
                                  LABEL_PATH,
                                 [256, 256, 3])


act_generator = act_gen.ImageActivationGenerator(mymodel, source_dir, activation_dir, max_examples=100)

import absl
absl.logging.set_verbosity(0)
num_random_exp=10
mytcav = tcav.TCAV(sess,
                   target,
                   concepts,
                   bottlenecks,
                   act_generator,
                   alphas,
                   cav_dir=cav_dir,
                   num_random_exp=num_random_exp)#10)
print ('This may take a while... Go get coffee!')
results = mytcav.run(run_parallel=False)
print ('done!')

utils_plot.plot_results(results, num_random_exp=num_random_exp)



