CUDA_LIBS = {
    '9.0':
        # dict(cublas='9.0', cudnn='7', cufft='9.0', curand='9.0', cudart='9.0'),
        dict(cudart='9.0'),
}

CURA_LIBS_MAP = {
    '1.7': CUDA_LIBS['9.0'],
    '1.8': CUDA_LIBS['9.0'],
    '1.9': CUDA_LIBS['9.0'],
    '1.10': CUDA_LIBS['9.0'],
}

