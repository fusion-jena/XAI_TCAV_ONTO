# this code is adapted from https://github.com/gyhandy/Humanoid-Vision-Engine/blob/main/preprocess_dataset/3_compute_feature_images/generate_texture_feature.py#L14
import sys
import argparse
import os
import cv2 #OpenCV library
import random
import numpy as np
#from project_dir import project_dir
import matplotlib.pyplot as plt

def get_candidate_patch(mask_img, step_num):
    step_y, step_x = [lens // step_num for lens in mask_img.shape]

    candidates = []
    for y in range(0, mask_img.shape[0] - step_y + 1, step_y):
        for x in range(0, mask_img.shape[1] - step_x + 1, step_x):
            candidate = mask_img[y:y + step_y, x:x + step_x].copy()
            if np.count_nonzero(candidate) / candidate.size > 0.99:
                candidates.append(candidate)
                # plt.imshow(candidate, cmap='gray')
                # plt.show()
    return candidates, step_y, step_x

def generate_symptom_concept(source_dir,segmented_images_dir, texture_name):
    patch_num = 4
    img_files = os.listdir(segmented_images_dir)
    for i, img_dir in enumerate(img_files):
        concept_folder = os.path.join(source_dir, texture_name)
        save_dir = os.path.join(concept_folder, img_dir)
        img = cv2.imread(os.path.join(segmented_images_dir, img_dir), 0)
        range_y, range_x = np.where(img != 0)
        print(range_y)
        print(range_x)
        min_y, max_y = range_y.min(), range_y.max()
        min_x, max_x = range_x.min(), range_x.max()
        #mask_img = cv2.resize(img[min_y:max_y, min_x:max_x].copy(), (224,224))
        mask_img = cv2.resize(img[min_y:max_y, min_x:max_x].copy(), (256,256))
        #plt.imshow(mask_img, cmap='gray')
        #plt.show()
        for step_num in range(3, 8):
            candidates, step_y, step_x = get_candidate_patch(mask_img, step_num)
            if len(candidates) >= patch_num:
                break
        candidates = random.sample(candidates, patch_num)
        texture_img = np.zeros([lens * 2 for lens in candidates[0].shape])
        #texture_img = np.zeros(mask_img.shape)
        steps = int(np.sqrt(patch_num))
        for j in range(steps):
            for k in range(steps):
                texture_img[j*step_y:(j+1)*step_y, k*step_x:(k+1)*step_x] = candidates[j*steps+k]
                #texture_img[j*step_y:(j+1)*step_y, k*step_x:(k+1)*step_x] = candidates[j*steps+k]
        #plt.imshow(texture_img, cmap='gray')
        #plt.show()
        cv2.imwrite(save_dir, texture_img)
        print('saved')
