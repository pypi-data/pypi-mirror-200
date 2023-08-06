from brisque import BRISQUE


def brisque_quality_score(img):
    """
    input:
        img: (H W C) uint8 ndarray.
    return:
        brisque score - see
    import package requirements: 
        python -m pip install brisque
    Instructions:
    """
    img = img.copy()
    obj = BRISQUE(url=False)
    return obj.score(img)
