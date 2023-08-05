from skimage.metrics import peak_signal_noise_ratio
# import cv2 as cv

class PSNR:
    def __init__(self):
        self.data_range = 255

    def psnr_quality_score(self, img1, img2):
        """
        input:
            img1/img2: (H W C) uint8 ndarray.
        return:
            psnr score, float.
        import package requirements: 
            python -m pip install scikit-image==0.20.0 
        Instructions:
        """
        img1, img2 = img1.copy(), img2.copy()
        return peak_signal_noise_ratio(img1, img2, data_range=self.data_range)
    


# img = cv.imread("M:\\Project 2 - Camera Sensor\\Images\\cat.jpeg", flags=cv.IMREAD_COLOR)
# img_blur_1 = cv.GaussianBlur(img,(3,3),cv.BORDER_DEFAULT)

# psnr_obj = PSNR()
# psnr_score = psnr_obj.psnr_quality_score(img,img_blur_1)
# print(psnr_score)
