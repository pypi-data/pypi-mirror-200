from skimage.metrics import structural_similarity
# import cv2 as cv


class SSIM:
    def __init__(self):
        self.win_size = None
        self.gradient = False
        self.data_range = 255
        self.multichannel = 2
        self.gaussian_weights = False
        self.full = False

    def ssim_quality_score(self, img1, img2):
        """
        input:
            img1 and img2: (H W C) uint8 ndarray - 3 channel RGB images
        return:
            ssim score, float.
        import package requirements: 
            python -m pip install scikit-image==0.20.0
        
        """
        img1, img2 = img1.copy(), img2.copy()
        return structural_similarity(img1, img2, win_size=self.win_size, gradient=self.gradient,
                                     data_range=self.data_range, channel_axis=self.multichannel,
                                     gaussian_weights=self.gaussian_weights, full=self.full)
  


# img = cv.imread("M:\\Project 2 - Camera Sensor\\Images\\cat.jpeg", flags=cv.IMREAD_COLOR)
# img_blur_1 = cv.GaussianBlur(img,(3,3),cv.BORDER_DEFAULT)

# ssim_obj = SSIM()
# ssim_score = ssim_obj.ssim_quality_score(img,img_blur_1)
# print(ssim_score)
