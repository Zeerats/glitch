import numpy as np

def apply(image_np, params):
    distortion_strength = params.get('distortion_strength', 10)
    num_bands = params.get('num_bands', 10)
    
    height, width, channels = image_np.shape
    assert channels == 3, "Image must have 3 channels (RGB)."
    
    center_y = height / 2
    center_x = width / 2
    max_shift = int(distortion_strength)
    shifted_image = image_np.copy()
    max_radius = np.sqrt(center_x**2 + center_y**2)
    band_radii = np.linspace(0, max_radius, num_bands + 1)
    shift_increment = max_shift / num_bands
    
    for i in range(num_bands):
        inner_radius = band_radii[i]
        outer_radius = band_radii[i + 1]
        shift_amount = int(shift_increment * (i + 1))
        
        y_indices, x_indices = np.ogrid[:height, :width]
        distance = np.sqrt((x_indices - center_x)**2 + (y_indices - center_y)**2)
        mask = (distance >= inner_radius) & (distance < outer_radius)
        
        # Shift Red Channel
        shifted_image[:, :, 0][mask] = np.roll(image_np[:, :, 0][mask], shift=shift_amount)
        # Shift Green Channel
        shifted_image[:, :, 1][mask] = np.roll(image_np[:, :, 1][mask], shift=-shift_amount)
        # Shift Blue Channel
        shifted_image[:, :, 2][mask] = np.roll(image_np[:, :, 2][mask], shift=shift_amount)
    
    return shifted_image
