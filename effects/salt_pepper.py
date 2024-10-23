import numpy as np

def apply(image, params):
    amount = params.get('amount', 0.005)
    salt_vs_pepper = params.get('salt_vs_pepper', 0.5)
    rgb = params.get('rgb', False)
    
    if rgb:
        noisy_image = image.copy()
        num_salt = np.ceil(amount * image.size * salt_vs_pepper).astype(int)
        num_pepper = np.ceil(amount * image.size * (1.0 - salt_vs_pepper)).astype(int)

        # Add Salt
        coords = [np.random.randint(0, i - 1, num_salt) for i in image.shape[:2]]
        noisy_image[coords[0], coords[1], :] = 255

        # Add Pepper
        coords = [np.random.randint(0, i - 1, num_pepper) for i in image.shape[:2]]
        noisy_image[coords[0], coords[1], :] = 0

        return noisy_image
    else:
        noisy_image = image.copy()
        num_salt = np.ceil(amount * image.size * 0.5).astype(int)
        num_pepper = np.ceil(amount * image.size * 0.5).astype(int)

        # Add Salt
        coords = [np.random.randint(0, i - 1, num_salt) for i in image.shape[:2]]
        noisy_image[coords[0], coords[1]] = 255

        # Add Pepper
        coords = [np.random.randint(0, i - 1, num_pepper) for i in image.shape[:2]]
        noisy_image[coords[0], coords[1]] = 0

        return noisy_image
