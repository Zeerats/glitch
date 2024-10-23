import numpy as np
import random

def apply(image, params):
    block_size = params.get('block_size', 10)
    displacement = params.get('displacement', 20)
    num_blocks = params.get('num_blocks', 50)
    rgb = params.get('rgb', False)
    
    glitched_image = image.copy()
    height, width = glitched_image.shape[:2]

    for _ in range(num_blocks):
        x = random.randint(0, width - block_size - 1)
        y = random.randint(0, height - block_size - 1)

        dx = random.randint(-displacement, displacement)
        dy = random.randint(-displacement, displacement)

        new_x = max(0, min(x + dx, width - block_size))
        new_y = max(0, min(y + dy, height - block_size))

        block = glitched_image[y:y+block_size, x:x+block_size].copy()
        glitched_image[y:y+block_size, x:x+block_size] = glitched_image[new_y:new_y+block_size, new_x:new_x+block_size]
        glitched_image[new_y:new_y+block_size, new_x:new_x+block_size] = block

    return glitched_image
