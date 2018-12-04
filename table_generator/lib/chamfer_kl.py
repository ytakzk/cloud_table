
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from pdb import set_trace as brk

class ChamferKLLoss(nn.Module):

    # https://github.com/345ishaan/DenseLidarNet/blob/master/code/chamfer_loss.py
	def __init__(self):
		super(ChamferKLLoss, self).__init__()
		self.use_cuda = torch.cuda.is_available()        

	def forward(self, preds, gts, mu, logvar):
		P = self.batch_pairwise_dist(gts, preds)
		mins, _ = torch.min(P, 1)
		loss_1 = torch.sum(mins)
		mins, _ = torch.min(P, 2)
		loss_2 = torch.sum(mins)

		CH = loss_1 + loss_2

		KL = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp()) 

		return CH + KL


	def batch_pairwise_dist(self, x, y):
		x = x.transpose(2, 1)
		y = y.transpose(2, 1)
		_, num_points_x, _ = x.size()
		_, num_points_y, _ = y.size()
		xx = torch.bmm(x, x.transpose(2,1))
		yy = torch.bmm(y, y.transpose(2,1))
		zz = torch.bmm(x, y.transpose(2,1))
		if self.use_cuda:
			dtype = torch.cuda.LongTensor
		else:
			dtype = torch.LongTensor
		diag_ind_x = torch.arange(0, num_points_x).type(dtype)
		diag_ind_y = torch.arange(0, num_points_y).type(dtype)
		rx = xx[:, diag_ind_x, diag_ind_x].unsqueeze(1).expand_as(zz.transpose(2,1))
		ry = yy[:, diag_ind_y, diag_ind_y].unsqueeze(1).expand_as(zz)
		P = (rx.transpose(2,1) + ry - 2*zz)
		return P