import torch
import torch.nn as nn
def CBR2d(in_channels, out_channels, kernel_size = 3, stride = 1, padding = 1, bias =True):
            return nn.Sequential(
                nn.Conv2d(
                    in_channels = in_channels,
                    out_channels = out_channels,
                    kernel_size = kernel_size,
                    stride = stride,
                    padding = padding,
                    bias = bias),
                nn.BatchNorm2d(num_features = out_channels),
                nn.ReLU()
            )
class UNet(nn.Module):
    def __init__(self, num_classes=12):
        super(UNet, self).__init__()
            
        
        # ===========================Encoder===========================
        self.enc1_1 =  CBR2d(in_channels = 3,out_channels = 64,kernel_size = 3,stride = 1,padding = 1, bias = True)
        self.enc1_2 = CBR2d(in_channels = 64,out_channels = 64,kernel_size = 3,stride = 1,padding = 1, bias = True)
        self.pool1 =  nn.MaxPool2d(kernel_size = 2) # 1/2
        
        self.enc2_1 = CBR2d(in_channels = 64,out_channels = 128,kernel_size = 3,stride = 1,padding = 1,bias = True)
        self.enc2_2 = CBR2d(in_channels = 128,out_channels = 128,kernel_size = 3,stride = 1,padding = 1,bias = True)
        self.pool2 = nn.MaxPool2d(kernel_size = 2) # 1/2
        
        self.enc3_1 = CBR2d(in_channels = 128,out_channels = 256,kernel_size = 3,stride = 1,padding = 1,bias = True)
        self.enc3_2 = CBR2d(in_channels = 256,out_channels = 256,kernel_size = 3,stride = 1,padding = 1,bias = True)
        self.pool3 = nn.MaxPool2d(kernel_size = 2)
        
        self.enc4_1 = CBR2d(in_channels = 256,out_channels = 512,kernel_size = 3,stride = 1,padding = 1,bias = True)
        self.enc4_2 = CBR2d(in_channels = 512,out_channels = 512,kernel_size = 3,stride = 1,padding = 1,bias = True)
        self.pool4 = nn.MaxPool2d(kernel_size = 2)
        
        # ===========================Encoder&Decoder===========================
        self.enc5_1 = CBR2d(in_channels = 512,out_channels = 1024,kernel_size = 3,stride = 1,padding = 1,bias = True)
        self.enc5_2 = CBR2d(in_channels =1024,out_channels = 1024,kernel_size = 3,stride = 1,padding = 1,bias = True)
        self.upconv4 = nn.ConvTranspose2d(in_channels = 1024,out_channels = 512,kernel_size = 2,stride = 2,padding = 0,bias = True)
        
        # ===========================Decoder===================================
        self.dec4_2 = CBR2d(in_channels = 1024, out_channels = 512, kernel_size = 3, stride = 1, padding = 1,  bias = True)
        self.dec4_1 = CBR2d(in_channels = 512, out_channels = 512, kernel_size = 3, stride = 1, padding = 1, bias = True)
        self.upconv3 = nn.ConvTranspose2d(in_channels= 512, out_channels = 256, kernel_size = 2, stride = 2, padding = 0, bias = True)
        
        self.dec3_2 = CBR2d(in_channels = 512, out_channels = 256, kernel_size = 3, stride = 1, padding = 1, bias = True)
        self.dec3_1 = CBR2d(in_channels = 256, out_channels = 256, kernel_size = 3, stride = 1, padding = 1, bias = True)
        self.upconv2 = nn.ConvTranspose2d(in_channels = 256, out_channels = 128, kernel_size = 2, stride = 2, padding = 0, bias = True)
        
        self.dec2_2 = CBR2d(in_channels = 256, out_channels = 128, kernel_size = 3, stride = 1, padding = 1, bias = True)
        self.dec2_1 = CBR2d(in_channels = 128, out_channels = 128, kernel_size = 3, stride = 1, padding = 1, bias = True)
        self.upconv1 = nn.ConvTranspose2d(in_channels = 128, out_channels = 64, kernel_size = 2, stride = 2, padding = 0, bias = True)
        
        self.dec1_2 = CBR2d(in_channels = 128, out_channels = 64, kernel_size = 3, stride = 1, padding = 1, bias = True)
        self.dec1_1 = CBR2d(in_channels = 64, out_channels = 64, kernel_size = 3, stride = 1, padding = 1, bias = True)
        self.score_fr = nn.Conv2d(in_channels = 64, out_channels = num_classes, kernel_size = 1, stride = 1, padding = 0, bias = True)
            
        
    def forward(self, x):
        enc1_1 = self.enc1_1(x)
        enc1_2 = self.enc1_2(enc1_1)
        pool1 = self.pool1(enc1_2)
        
        enc2_1 = self.enc2_1(pool1)
        enc2_2 = self.enc2_2(enc2_1)
        pool2 = self.pool2(enc2_2)
        
        enc3_1 = self.enc3_1(pool2)
        enc3_2 = self.enc3_2(enc3_1)
        pool3 = self.pool3(enc3_2)
        
        enc4_1 = self.enc4_1(pool3)
        enc4_2 = self.enc4_2(enc4_1)
        pool4 = self.pool4(enc4_2)
        
        enc5_1 = self.enc5_1(pool4)
        enc5_2 = self.enc5_2(enc5_1)
        upconv4 = self.upconv4(enc5_2)
        
        cat4 = torch.cat([upconv4, enc4_2], dim = 1) # 채널 concat
        
        dec4_2 = self.dec4_2(cat4)
        dec4_1 = self.dec4_1(dec4_2)
        upconv3 = self.upconv3(dec4_1)
        
        cat3 = torch.cat([upconv3, enc3_2], dim = 1)
        
        dec3_2 = self.dec3_2(cat3)
        dec3_1 = self.dec3_1(dec3_2)
        upconv2 = self.upconv2(dec3_1)
        
        cat2 = torch.cat([upconv2, enc2_2], dim = 1)
        
        dec2_2 = self.dec2_2(cat2)
        dec2_1 = self.dec2_1(dec2_2)
        upconv1 = self.upconv1(dec2_1)
        
        cat1 = torch.cat([upconv1,enc1_2], dim = 1)
        
        dec1_2 = self.dec1_2(cat1)
        dec1_1 = self.dec1_1(dec1_2)
        x = self.score_fr(dec1_1)
        
        return x

if __name__ == '__main__':
    model = UNet(num_classes=12)
    x = torch.randn([1, 3, 512, 512])
    print("input shape : ", x.shape)
    out = model(x)
    print("output shape : ", out.size())