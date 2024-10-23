import os
import json
import sys
import importlib
from PIL import Image
import numpy as np
import random
from pathlib import Path

def load_effects(effects_folder):
    effects = {}
    effects_path = Path(effects_folder)
    if not effects_path.exists() or not effects_path.is_dir():
        print(f"Error: Effects folder '{effects_folder}' does not exist or is not a directory.")
        sys.exit(1)
    
    for file in effects_path.glob("*.py"):
        if file.name.startswith("__"):
            continue  # Skip __init__.py and other special files
        module_name = file.stem
        try:
            module = importlib.import_module(f"effects.{module_name}")
            if hasattr(module, 'apply'):
                effects[module_name] = module.apply
                print(f"Loaded effect '{module_name}' from '{file.name}'.")
            else:
                print(f"Warning: Module '{module_name}' does not have an 'apply' function. Skipping.")
        except Exception as e:
            print(f"Error loading effect '{module_name}': {e}")
    
    return effects

def apply_effects(image_np, effects_order, effects_params, available_effects):
    processed_image = image_np.copy()
    
    for effect in effects_order:
        if effect not in available_effects:
            print(f"Warning: Effect '{effect}' not found. Skipping.")
            continue
        params = effects_params.get(effect, {})
        print(f"Applying '{effect}' with parameters: {params}")
        try:
            processed_image = available_effects[effect](processed_image, params)
        except Exception as e:
            print(f"Error applying effect '{effect}': {e}")
    
    return processed_image

def load_config(config_path):
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"Error loading configuration file '{config_path}': {e}")
        sys.exit(1)

def is_image_file(filename):
    image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif']
    return Path(filename).suffix.lower() in image_extensions

def process_images(input_folder, output_folder, config, available_effects):
    if not os.path.exists(input_folder):
        print(f"Error: Input folder '{input_folder}' does not exist.")
        sys.exit(1)

    os.makedirs(output_folder, exist_ok=True)

    seed = config.get('seed', None)
    if seed is not None:
        np.random.seed(seed)
        random.seed(seed)
        print(f"Random seed set to {seed} for reproducibility.\n")

    effects_order = config.get('effects_order', [])
    effects_params = config.get('effects', {})

    for filename in os.listdir(input_folder):
        if is_image_file(filename):
            input_path = os.path.join(input_folder, filename)
            try:
                with Image.open(input_path) as img:
                    img = img.convert('RGB')
                    image_np = np.array(img)

                print(f"Processing '{filename}'...")

                processed_image_np = apply_effects(image_np, effects_order, effects_params, available_effects)

                processed_image = Image.fromarray(processed_image_np)
                output_path = os.path.join(output_folder, filename)
                processed_image.save(output_path)
                print(f"Saved processed image to '{output_path}'.\n")

            except Exception as e:
                print(f"Error processing '{filename}': {e}\n")
        else:
            print(f"Skipping non-image file '{filename}'.\n")

def main():
    print("Starting script...")  # Debug print
    script_dir = Path(__file__).parent
    config_path = script_dir / 'config.json'

    if not config_path.is_file():
        print(f"Error: Configuration file 'config.json' not found in '{script_dir}'.")
        sys.exit(1)

    config = load_config(config_path)
    print("Configuration loaded successfully.\n")

    input_folder = config.get('input_folder', 'input_images')
    output_folder = config.get('output_folder', 'output_images')

    input_folder = (script_dir / input_folder).resolve()
    output_folder = (script_dir / output_folder).resolve()

    print(f"Input Folder: {input_folder}")
    print(f"Output Folder: {output_folder}\n")

    # Load effects from the 'effects' folder
    effects_folder = script_dir / 'effects'
    available_effects = load_effects(effects_folder)

    process_images(input_folder, output_folder, config, available_effects)
    print("All images have been processed successfully.")

if __name__ == "__main__":
    main()
