def RETINEX_BASED(im):
    mu = 2.3
    H,W,garbage = np.shape(im)

    ################################################### Color Correction ########################################################
    im_c = im*255
    for i in range(3):
        var = np.sum((im_c[:,:,i]-np.mean(im_c[:,:,i]))**2)/(H*W)
        var = np.sqrt(var)
        mx = np.mean(im_c[:,:,i])+mu*var
        mn = np.mean(im_c[:,:,i])-mu*var
        x = (im_c[:,:,i]-mn)/(mx-mn)*255
        # x[x>1] = 1
        # x[x<0] = 0
        x[x>255] = 255
        x[x<0] = 0
        im_c[:,:,i] = x*1
        print(np.min(im_c),np.max(im_c))
    im_c = im_c.astype(int)
    im_c = np.float32(im_c/255)
    im_c_lab = cv2.cvtColor(im_c,cv2.COLOR_RGB2LAB)


    ################################################### Calculate I0 ########################################################
    sigma = 5;
    window_size = 3*sigma    
    gaussian_kernel_1d = signal.gaussian(window_size, std=sigma).reshape(window_size, 1)
    gaussian_kernel_2d = np.outer(gaussian_kernel_1d, gaussian_kernel_1d)
    gaussian_kernel_2d /= np.sum(gaussian_kernel_2d)
    L = im_c_lab*1
    L[:,:,0] = L[:,:,0]/100*255
    I0 = np.abs(cv2.filter2D(L[:,:,0], -1, gaussian_kernel_2d))

    ################################################### Parameters ########################################################
    lamb = 10
    alpha = 100
    beta = 0.1
    gamma = 1

    ###################################################### Loop ###########################################################

    #-------------- Initialize ----------------#
    R = np.zeros(np.shape(L[:,:,0]))
    I = I0*1

    #---------------- Shrink ------------------#
    diff_x = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
    diff_y = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])

    dx = cv2.filter2D(R,-1,diff_x)
    dy = cv2.filter2D(R,-1,diff_y)

    max_dx = np.abs(dx)-0.5/lamb
    dx = (max_dx>0).astype(float)*max_dx*((dx>=0).astype(float)-(dx<0).astype(float))

    max_dy = np.abs(dy)-0.5/lamb
    dy = (max_dy>0).astype(float)*max_dy*((dy>=0).astype(float)-(dy<0).astype(float))

    #---------------- R ------------------#
    one = np.zeros(np.shape(L[:,:,0]))
    # one[int(np.shape(one)[0]/2),int(np.shape(one)[1]/2)] = 1
    one[0,0] = 1

    if np.min(I)==0:
        I+=1e-10
    R_1 = (1+beta*lamb)*np.fft.fft2(L[:,:,0]/I)
    R_2 = np.fft.fft2(one) + beta*lamb*(np.fft.fft2(dx)*np.conjugate(np.fft.fft2(dx)) + np.fft.fft2(dy)*np.conjugate(np.fft.fft2(dy)))
    R_ = R_1/R_2
    R = np.abs(np.fft.ifft2(R_))

    #---------------- I ------------------#
    one = one*(1+gamma)
    if np.min(R)==0:
        R+=1e-20
    I_1 = np.fft.fft2(gamma*I0+L[:,:,0]/R)
    I_2 = np.fft.fft2(one)+alpha*(np.fft.fft2(dx)*np.conjugate(np.fft.fft2(dx))+np.fft.fft2(dy)*np.conjugate(np.fft.fft2(dy)))
    I_ = I_1/I_2
    I = np.real(np.fft.ifft2(I_))
    I = (I>=L[:,:,0]).astype(float)*I+(I<L[:,:,0]).astype(float)*L[:,:,0]

    #--------------- remap ---------------#
    decimal = 1
    C = np.zeros(230*decimal+1)
    for i in range(230*decimal+1):
        if i==0:
            C[i] = np.arctan(0-15)
        else:
            C[i] = C[i-1]+np.arctan(i/decimal-15)
    C = C/C[230*decimal]

    I_new = np.round(I*decimal)
    upper_bound = np.int(np.max(np.round(I*decimal))+1)
    sum = 0
    for i in range(upper_bound):
        sum += np.arctan(i/decimal)*np.sum((np.round(I*decimal)==i))
    # print(sum)
    for i in range(upper_bound):
        c = np.arctan(i/decimal)*np.sum((np.round(I*decimal)==i))/sum
        idx = np.argmax(C>=c)
        I_new[np.round(I*decimal)==i] = idx
    I_new = I_new/decimal
    # I = I_new*1

    #------------- update ----------------#
    # L_ = L*1
    # L_[:,:,0] = R*I/np.max(R)
    # L_ = cv2.cvtColor(L_,cv2.COLOR_LAB2RGB)
    # return L_
    L_ = L*1
    L_[:,:,0] = R*I/255*100/2
    L_ = cv2.cvtColor(L_,cv2.COLOR_LAB2RGB)
    return L_
