import numpy as np
import random

def apply(image, params):
    shift_range = tuple(params.get('shift_range', (-10, 10)))
    num_lines = params.get('num_lines', 10)
    shift_line_height = params.get('shift_line_height', 1)
    rgb = params.get('rgb', False)
    
    glitched_image = image.copy()
    height, width = glitched_image.shape[:2]

    for _ in range(num_lines):
        y = random.randint(0, height - shift_line_height)
        shift = random.randint(*shift_range)
        glitched_image[y:y+shift_line_height, :] = np.roll(glitched_image[y:y+shift_line_height, :], shift, axis=1)

    return glitched_image
