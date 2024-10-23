import numpy as np

def apply(image_np, params):
    distortion_strength = params.get('distortion_strength', 0.5)
    
    height, width, channels = image_np.shape
    x = np.linspace(-1, 1, width)
    y = np.linspace(-1, 1, height)
    xv, yv = np.meshgrid(x, y)
    
    r = np.sqrt(xv**2 + yv**2)
    r_distorted = r + distortion_strength * (r**3)
    r_distorted = np.where(r == 0, 1, r_distorted)
    
    theta = np.arctan2(yv, xv)
    x_distorted = r_distorted * np.cos(theta)
    y_distorted = r_distorted * np.sin(theta)
    
    x_new = ((x_distorted + 1) / 2) * (width - 1)
    y_new = ((y_distorted + 1) / 2) * (height - 1)
    
    x0 = np.floor(x_new).astype(int)
    y0 = np.floor(y_new).astype(int)
    x1 = x0 + 1
    y1 = y0 + 1
    
    x0 = np.clip(x0, 0, width - 1)
    y0 = np.clip(y0, 0, height - 1)
    x1 = np.clip(x1, 0, width - 1)
    y1 = np.clip(y1, 0, height - 1)
    
    wa = (x1 - x_new) * (y1 - y_new)
    wb = (x_new - x0) * (y1 - y_new)
    wc = (x1 - x_new) * (y_new - y0)
    wd = (x_new - x0) * (y_new - y0)
    
    image_flat = image_np.reshape(-1, channels)
    idx_a = y0 * width + x0
    idx_b = y0 * width + x1
    idx_c = y1 * width + x0
    idx_d = y1 * width + x1
    
    # Flatten the indices to ensure correct broadcasting
    idx_a_flat = idx_a.flatten()
    idx_b_flat = idx_b.flatten()
    idx_c_flat = idx_c.flatten()
    idx_d_flat = idx_d.flatten()
    
    distorted_flat = (
        wa.flatten()[:, np.newaxis] * image_flat[idx_a_flat] +
        wb.flatten()[:, np.newaxis] * image_flat[idx_b_flat] +
        wc.flatten()[:, np.newaxis] * image_flat[idx_c_flat] +
        wd.flatten()[:, np.newaxis] * image_flat[idx_d_flat]
    )
    
    return distorted_flat.reshape((height, width, channels)).astype(np.uint8)
