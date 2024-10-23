import numpy as np

def apply(image, params):
    mean = params.get('mean', 0.0)
    std = params.get('std', 25.0)
    rgb = params.get('rgb', False)
    
    if rgb:
        channels = []
        for c in range(3):
            channel = image[:, :, c].astype('float32')
            gaussian = np.random.normal(mean, std, channel.shape).astype('float32')
            noisy_channel = channel + gaussian
            noisy_channel = np.clip(noisy_channel, 0, 255).astype('uint8')
            channels.append(noisy_channel)
        return np.stack(channels, axis=2)
    else:
        gaussian = np.random.normal(mean, std, image.shape).astype('float32')
        noisy_image = image.astype('float32') + gaussian
        noisy_image = np.clip(noisy_image, 0, 255).astype('uint8')
        return noisy_image
