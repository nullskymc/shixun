import cv2
import numpy as np
from sklearn.mixture import GaussianMixture

# 读取图像
img = cv2.imread('./dataset/Top-0001.bmp')

# 将图像转换为灰度图像
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 对灰度图像进行预处理
denoised_img = cv2.fastNlMeansDenoising(gray_img, None, 10, 7, 21)

# 将图像转换为一维数组
data = denoised_img.reshape(-1, 1)

# 使用高斯混合模型聚类算法进行聚类
gmm = GaussianMixture(n_components=5)
gmm.fit(data)
labels = gmm.predict(data)

# 将聚类结果转换为图像
segmented_img = labels.reshape(denoised_img.shape)

# 根据聚类结果对图像进行分类
fangjie = np.zeros_like(segmented_img)
shiying = np.zeros_like(segmented_img)
niantu = np.zeros_like(segmented_img)
kongxi = np.zeros_like(segmented_img)
changshi = np.zeros_like(segmented_img)

for i in np.unique(segmented_img):
    mask = segmented_img == i
    if np.mean(gray_img[mask]) > 190:
        fangjie[mask] = 255
    elif np.mean(gray_img[mask]) > 124.8:
        changshi[mask] = 255
    elif np.mean(gray_img[mask]) > 120:
        shiying[mask] = 255
    elif np.mean(gray_img[mask]) > 55:
        niantu[mask] = 255
    else:
        kongxi[mask] = 255

# 将分类结果转换为彩色图像
fangjie = cv2.cvtColor(fangjie.astype(np.uint8), cv2.COLOR_GRAY2BGR)
shiying = cv2.cvtColor(shiying.astype(np.uint8), cv2.COLOR_GRAY2BGR)
niantu = cv2.cvtColor(niantu.astype(np.uint8), cv2.COLOR_GRAY2BGR)
kongxi = cv2.cvtColor(kongxi.astype(np.uint8), cv2.COLOR_GRAY2BGR)
changshi = cv2.cvtColor(changshi.astype(np.uint8), cv2.COLOR_GRAY2BGR)



# 将分类结果叠加到原图上
img = cv2.add(img, fangjie)
img = cv2.add(img, shiying)
img = cv2.add(img, niantu)
img = cv2.add(img, kongxi)
img = cv2.add(img, changshi)

# 保存分类结果图片到对应的文件夹
cv2.imwrite('./dataset/fangjie/Top-0001_fangjie.bmp', fangjie)
cv2.imwrite('./dataset/shiying/Top-0001_shiying.bmp', shiying)
cv2.imwrite('./dataset/niantu/Top-0001_niantu.bmp', niantu)
cv2.imwrite('./dataset/kongxi/Top-0001_kongxi.bmp', kongxi)
cv2.imwrite('./dataset/changshi/Top-0001_changshi.bmp', changshi)
cv2.imwrite('./dataset/Top-0001_result.bmp', img)