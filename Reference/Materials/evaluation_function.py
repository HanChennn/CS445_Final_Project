# input: original & dehaze image
# output: evaluation e value
def evaluation_e(original, dehaze):
    if np.max(original)<=1:
        original_ = original*255
    if np.max(dehaze)<=1:
        dehaze_ = dehaze*255
    edges_origin = cv2.Canny(np.uint8(original_), threshold1=10, threshold2=35)
    edges_dehaze = cv2.Canny(np.uint8(dehaze_), threshold1=10, threshold2=35)
    plt.imshow(edges_origin,cmap='gray')
    plt.show()
    plt.imshow(edges_dehaze,cmap='gray')
    plt.show()
    return (np.sum(edges_dehaze)-np.sum(edges_origin))/np.sum(edges_origin)

# input: original & dehaze should be in RGB sequence
#        threshold_uppor: the value large than this is regarded as saturated (black)
#        threshold_lower: the value smaller than this is regarded as saturated (white)
# output: evaluation sigma value
def evaluation_sigma(original, dehaze, threshold_upper=250, threshold_lower=10):
    H,W,garbage = np.shape(original)
    if np.max(original)<=1:
        original_ = np.uint8(original*255)
    if np.max(dehaze)<=1:
        dehaze_ = np.uint8(dehaze*255)
    original_gray = cv2.cvtColor(original_, cv2.COLOR_RGB2GRAY)
    dehaze_gray = cv2.cvtColor(dehaze_, cv2.COLOR_RGB2GRAY)
    sigma = np.sum((dehaze_gray>threshold_upper)*(1-(original_gray>threshold_upper)))
    sigma+= np.sum((dehaze_gray<threshold_lower)*(1-(original_gray<threshold_lower)))
    return 1.0*sigma/(H*W)