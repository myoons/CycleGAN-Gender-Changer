#!/usr/bin/python3

import argparse
import itertools
import os

import numpy as np

import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torch.autograd import Variable
from PIL import Image
import torch

from models.generator import Generator
from models.discriminator import Discriminator
from utils.utils import ReplayBuffer
from utils.utils import LambdaLR
from utils.utils import weights_init_normal
from datasets import ImageDataset

from tensorboardX import SummaryWriter
from collections import defaultdict

from datetime import datetime

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--epoch', type=int, default=0, help='starting epoch')
    parser.add_argument('--n_epochs', type=int, default=400, help='number of epochs of training')
    parser.add_argument('--batchSize', type=int, default=10, help='size of the batches')
    parser.add_argument('--dataroot', type=str, default='datasets/genderchange/', help='root directory of the dataset')
    parser.add_argument('--lr', type=float, default=0.0002, help='initial learning rate')
    parser.add_argument('--decay_epoch', type=int, default=100, help='epoch to start linearly decaying the learning rate to 0')
    parser.add_argument('--size', type=int, default=256, help='size of the data crop (squared assumed)')
    parser.add_argument('--input_nc', type=int, default=3, help='number of channels of input data')
    parser.add_argument('--output_nc', type=int, default=3, help='number of channels of output data')
    parser.add_argument('--cuda', action='store_true', help='use GPU computation')
    parser.add_argument('--n_cpu', type=int, default=8, help='number of cpu threads to use during batch generation')
    opt = parser.parse_args()
    print(opt)

    if torch.cuda.is_available() and not opt.cuda:
        print("WARNING: You have a CUDA device, so you should probably run with --cuda")

    ###### Definition of variables ######
    # Networks
    netG_A2B = Generator(opt.input_nc, opt.output_nc)
    netG_B2A = Generator(opt.output_nc, opt.input_nc)
    netD_A = Discriminator(opt.input_nc)
    netD_B = Discriminator(opt.output_nc)

    if opt.cuda:
        netG_A2B.cuda()
        netG_B2A.cuda()
        netD_A.cuda()
        netD_B.cuda()

    netG_A2B.apply(weights_init_normal)
    netG_B2A.apply(weights_init_normal)
    netD_A.apply(weights_init_normal)
    netD_B.apply(weights_init_normal)

    # Lossess
    criterion_GAN = torch.nn.MSELoss()
    criterion_cycle = torch.nn.L1Loss()
    criterion_identity = torch.nn.L1Loss()

    # Optimizers & LR schedulers
    optimizer_G = torch.optim.Adam(itertools.chain(netG_A2B.parameters(), netG_B2A.parameters()),
                                    lr=opt.lr, betas=(0.5, 0.999))
    optimizer_D_A = torch.optim.Adam(netD_A.parameters(), lr=opt.lr, betas=(0.5, 0.999))
    optimizer_D_B = torch.optim.Adam(netD_B.parameters(), lr=opt.lr, betas=(0.5, 0.999))

    lr_scheduler_G = torch.optim.lr_scheduler.LambdaLR(optimizer_G, lr_lambda=LambdaLR(opt.n_epochs, opt.epoch, opt.decay_epoch).step)
    lr_scheduler_D_A = torch.optim.lr_scheduler.LambdaLR(optimizer_D_A, lr_lambda=LambdaLR(opt.n_epochs, opt.epoch, opt.decay_epoch).step)
    lr_scheduler_D_B = torch.optim.lr_scheduler.LambdaLR(optimizer_D_B, lr_lambda=LambdaLR(opt.n_epochs, opt.epoch, opt.decay_epoch).step)

    # Inputs & targets memory allocation
    Tensor = torch.cuda.FloatTensor if opt.cuda else torch.Tensor
    input_A = Tensor(opt.batchSize, opt.input_nc, opt.size, opt.size)
    input_B = Tensor(opt.batchSize, opt.output_nc, opt.size, opt.size)
    target_real = Variable(Tensor(opt.batchSize).fill_(1.0), requires_grad=False)
    target_fake = Variable(Tensor(opt.batchSize).fill_(0.0), requires_grad=False)

    fake_A_buffer = ReplayBuffer()
    fake_B_buffer = ReplayBuffer()

    # Dataset loader
    transforms_ = [ transforms.Resize(int(opt.size*1.2), Image.BICUBIC), 
                    transforms.CenterCrop(opt.size),
                    transforms.ToTensor(),
                    transforms.Normalize((0.5,0.5,0.5), (0.5,0.5,0.5))]
                    
    dataloader = DataLoader(ImageDataset(opt.dataroot, transforms_=transforms_, unaligned=True), 
                            batch_size=opt.batchSize, shuffle=True, num_workers=opt.n_cpu, drop_last=True)

    # Plot Loss and Images in Tensorboard
    experiment_dir = 'logs/{}@{}'.format(opt.dataroot.split('/')[1], datetime.now().strftime("%d.%m.%Y-%H:%M:%S"))
    os.makedirs(experiment_dir, exist_ok=True)
    writer = SummaryWriter(os.path.join(experiment_dir, "tb"))

    metric_dict = defaultdict(list)
    n_iters_total = 0

    ###################################
    ###### Training ######
    for epoch in range(opt.epoch, opt.n_epochs):
        for i, batch in enumerate(dataloader):

            # Set model input
            real_A = Variable(input_A.copy_(batch['A']))
            real_B = Variable(input_B.copy_(batch['B']))

            ###### Generators A2B and B2A ######
            optimizer_G.zero_grad()

            # Identity loss
            # G_A2B(B) should equal B if real B is fed
            same_B = netG_A2B(real_B)
            loss_identity_B = criterion_identity(same_B, real_B)*5.0 # [batchSize, 3, ImgSize, ImgSize]

            # G_B2A(A) should equal A if real A is fed
            same_A = netG_B2A(real_A)
            loss_identity_A = criterion_identity(same_A, real_A)*5.0 # [batchSize, 3, ImgSize, ImgSize]

            # GAN loss
            fake_B = netG_A2B(real_A)
            pred_fake = netD_B(fake_B).view(-1)
            loss_GAN_A2B = criterion_GAN(pred_fake, target_real) # [batchSize]

            fake_A = netG_B2A(real_B)
            pred_fake = netD_A(fake_A).view(-1)
            loss_GAN_B2A = criterion_GAN(pred_fake, target_real) # [batchSize]

            # Cycle loss
            recovered_A = netG_B2A(fake_B)
            loss_cycle_ABA = criterion_cycle(recovered_A, real_A)*10.0 # [batchSize, 3, ImgSize, ImgSize]

            recovered_B = netG_A2B(fake_A)
            loss_cycle_BAB = criterion_cycle(recovered_B, real_B)*10.0 # [batchSize, 3, ImgSize, ImgSize]

            # Total loss
            loss_G = loss_identity_A + loss_identity_B + loss_GAN_A2B + loss_GAN_B2A + loss_cycle_ABA + loss_cycle_BAB

            loss_G.backward()
            optimizer_G.step()
            ###################################

            ###### Discriminator A ######
            optimizer_D_A.zero_grad()

            # Real loss
            pred_real = netD_A(real_A).view(-1)
            loss_D_real = criterion_GAN(pred_real, target_real) # [batchSize]

            # Fake loss
            fake_A = fake_A_buffer.push_and_pop(fake_A)
            pred_fake = netD_A(fake_A.detach()).view(-1) 
            loss_D_fake = criterion_GAN(pred_fake, target_fake) # [batchSize]

            # Total loss
            loss_D_A = (loss_D_real + loss_D_fake)*0.5
            loss_D_A.backward()

            optimizer_D_A.step()
            ###################################

            ###### Discriminator B ######
            optimizer_D_B.zero_grad()

            # Real loss
            pred_real = netD_B(real_B).view(-1) 
            loss_D_real = criterion_GAN(pred_real, target_real) # [batchSize]
            
            # Fake loss
            fake_B = fake_B_buffer.push_and_pop(fake_B)
            pred_fake = netD_B(fake_B.detach()).view(-1)
            loss_D_fake = criterion_GAN(pred_fake, target_fake) # [batchSize]

            # Total loss
            loss_D_B = (loss_D_real + loss_D_fake)*0.5
            loss_D_B.backward()

            optimizer_D_B.step()
            ###################################

            metric_dict['loss_G'].append(loss_G.item())
            metric_dict['loss_G_identity'].append(loss_identity_A.item() + loss_identity_B.item())
            metric_dict['loss_G_GAN'].append(loss_GAN_A2B.item() + loss_GAN_B2A.item())
            metric_dict['loss_G_cycle'].append(loss_cycle_ABA.item() + loss_cycle_BAB.item())
            metric_dict['loss_D'].append(loss_D_A.item() + loss_D_B.item())

            for title, value in metric_dict.items():
                writer.add_scalar('train/{}'.format(title), value[-1], n_iters_total)

            n_iters_total += 1

        print("""
        -----------------------------------------------------------
        Epoch : {} Finished
        Loss_G : {}
        Loss_G_identity : {}
        Loss_G_GAN : {}
        Loss_G_cycle : {}
        Loss_D : {}
        -----------------------------------------------------------
        """.format(epoch, loss_G, loss_identity_A + loss_identity_B, loss_GAN_A2B + loss_GAN_B2A, loss_cycle_ABA + loss_cycle_BAB, loss_D_A + loss_D_B))
        
        
        # Update learning rates
        lr_scheduler_G.step()
        lr_scheduler_D_A.step()
        lr_scheduler_D_B.step()

        # Save models checkpoints

        if loss_G.item() < 2.5 :
            os.makedirs(os.path.join(experiment_dir, str(epoch)), exist_ok=True) 
            torch.save(netG_A2B.state_dict(), '{}/{}/netG_A2B.pth'.format(experiment_dir, epoch))
            torch.save(netG_B2A.state_dict(), '{}/{}/netG_B2A.pth'.format(experiment_dir, epoch))
            torch.save(netD_A.state_dict(), '{}/{}/netD_A.pth'.format(experiment_dir, epoch))
            torch.save(netD_B.state_dict(), '{}/{}/netD_B.pth'.format(experiment_dir, epoch))

        for title, value in metric_dict.items():
            writer.add_scalar("train/{}_epoch".format(title), np.mean(value), epoch)

    ###################################

if __name__ == "__main__":
    main()
