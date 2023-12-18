# XAI_TCAV_ONTO
![Alt Text](https://github.com/jihenAM/XAI_TCAV_ONTO/blob/main/framework.png)
This repository contains the code for Integrating domain knowledge for enhanced concept model explainability in Plant Disease classification
For more details, please check our paper.

## Installation
To execute our method you need first to: 
  1.  Clone the repository
  2.  Create a new virtual environment with Python 3.7
  3. Run the following command from the repository folder:

```shell
pip install -r requirements.txt
```
## Download example models and images
These files could be added to the source_dir folder.
   source_dir: where images of concepts, target class, segmented images for targect class from test set, and random images (negative samples when learning CAVs) exist. Each should be a sub-folder within this directory
You can find an example for a source_dir to use to reproduce results for the class BacterialSpot here with the following components:
### Images
  * Images for the target class BacterialSpot disease from PlantVillage Tomaoto dataset [2]
  * Segmented  images for the target class from its test set ( the model was not trained on these images)
  * Random Tomato healthy class images [2] used by TCAV for hypothesis testing of important concepts
### Models
  * Trained InceptionV3 model on Tomaoto dataset.
  * Class labels
### Ontology
The structure of TomatoDCO ontology is divided into three parts: (a) the class hierarchy of TomatoDCO; (b) the object properties of TomatoDCO; (c) the object properties descriptions (range and domain); and (d ) an example of axioms representing concepts of abnormalities of the tomato bacterial spot disease.
A detailed description of these components is given in our paper.
![ontology_structure](https://github.com/jihenAM/XAI_TCAV_ONTO/blob/main/ontology/ontology_structure.png))
## Usage

  * The script [main.py](https://github.com/jihenAM/XAI_TCAV_ONTO/blob/main/main.py) run the whole algorithm to generate concepts automatically from the ontology and compute     tcav scores for each generated concepts.
  * Based on the target class label, the ontology [TomatoDCO.owl](https://github.com/jihenAM/XAI_TCAV_ONTO/blob/main/ontology/TomatoDCO.owl) provides all important   properties linked to the specified disease class using the method  [*fetch_concepts_from_ontology(ontology_path, class_name)*](https://github.com/jihenAM/XAI_TCAV_ONTO/blob/main/ontology/ontology_concepts.py) Where *Ontology_path* is the path to TomatoDCO.owl ontology and *Class_name* is the target class in test. For example, some of these properties (concepts) could be color, symptom and shape abnormalities. The generated concept labels (i.e., color brown) are then used to automatically generate corresponding images (i.e., different shades of brown images).
  * To generate color concepts, the method (generate_color_concept(color, source_dir)) is used where *color* is the color to generate images for and *source_dir* is the directory where the generated color images will be saved.
  * To generate symptom concepts, the method [*generate_shape_concept(segmented_images_dir,shape_folder)*](https://github.com/jihenAM/XAI_TCAV_ONTO/blob/main/generate_concepts/generate_shape.py) is used where *segmented_images_dir* is the directory where the segmented images of target class from test set are saved and *shape_folder* is the folder where the generated shape images will be saved.
  * To generate shape concepts, the method [*generate_symptom_concept(source_dir,segmented_images_dir, symptom)*](https://github.com/jihenAM/XAI_TCAV_ONTO/blob/main/generate_concepts/generate_symptom.py)is used Where *symptom* is the concept to be generated.
More details on the generation process could be found in our paper **section 4.2**.

These generated concepts in the form of images with target class images and random images are subsequently employed to derive Concept Activation vectors (CAVs)[1].
After running main.py, tcav scores for each generated concept from ontology will be given.

## References
 * [1] Interpretability Beyond Feature Attribution: Quantitative Testing with Concept Activation Vectors (https://arxiv.org/abs/1711.11279; Kim, B. et al https://github.com/tensorflow/tcav/blob/master/README.md)
 * [2] [An open access repository of images on plant health to enable the development of mobile disease diagnostics](https://arxiv.org/ftp/arxiv/papers/1511/1511.08060.pdf). (Hughes, P. et al, https://github.com/spMohanty/PlantVillage-Dataset)
