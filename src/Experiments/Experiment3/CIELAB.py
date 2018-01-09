class Color_Lab(object):
    def __init__(self, L, a, b):
        self.L = L
        self.a = a
        self.b = b
        
    def toRGB(self):
        varY = (self.L + 16) / 115.0
        varX = self.a / 500.0 + varY
        varZ = varY - self.b / 200.0
        
        varX = self._filter_threshold(varX)
        varY = self._filter_threshold(varY)
        varZ = self._filter_threshold(varZ)
        
        refX =  95.047
        refY = 100.000
        refZ = 108.883
        
        X = refX * varX / 100
        Y = refY * varY / 100
        Z = refZ * varZ / 100
        
        varR = X * 3.2406 + Y * (-1.5374) + Z * (-0.4986)
        varG = X * (-0.9689) + Y * 1.8758 + Z * 0.0415
        varB = X * 0.0557 + Y * (-0.2040) + Z * 1.0570
        
        R = self._gamma_correction(varR) * 255
        G = self._gamma_correction(varG) * 255
        B = self._gamma_correction(varB) * 255
        
        R = self._trimming(R)
        G = self._trimming(G)
        B = self._trimming(B)
        
        return [R, G, B]
    
    def _gamma_correction(self, rgb):
        '''
        Gamma correction for IEC 61966-2-1 standard
        '''
        if rgb > 0.0031308:
            return 1.055 * (numpy.power(rgb, (1.0/2.4))) - 0.055
        else:
            return 12.92 * rgb
    
    def _filter_threshold(self, xyz):
        if numpy.power(xyz, 3.0) > 0.008856:
            return numpy.power(xyz, 3.0)
        else:
            return (xyz - 16.0/116.0) / 7.787
        
    def _trimming(self, rgb):
        if rgb > 255:
            rgb = 255
        elif rgb < 0:
            rgb = 0
            
        return int(rgb)
    
    def fromRGB(self):
        print('Warnning: function Lab_Color.fromRGB has not been implemented yet.')
        pass

def angle2RGB(ang, Lab_center, radius):
    theta = ang * 2.0 * numpy.pi / 360.0
    a = Lab_center.a + radius * numpy.cos(theta)
    b = Lab_center.b + radius * numpy.sin(theta)
    L = Lab_center.L
    
    Lab_color = Color_Lab(L, a, b)
    return Lab_color.toRGB()