import torch,torch.nn as nn
from motifgnn.model import EdgeMotifGNN
from motifwl.parity import private_triangle_parity_pair
torch.manual_seed(0)
G0,G1=private_triangle_parity_pair(d=1)
def train(mode,steps=300,lr=5e-3):
 m=EdgeMotifGNN(d=32,layers=4,mode=mode,out=1).double()
 opt=torch.optim.Adam(m.parameters(),lr=lr);lf=nn.BCEWithLogitsLoss()
 y=torch.tensor([0.,1.],dtype=torch.float64)
 for _ in range(steps):
  opt.zero_grad()
  out=torch.stack([m(G0).squeeze(),m(G1).squeeze()])
  loss=lf(out,y);loss.backward();opt.step()
 with torch.no_grad():
  o=torch.stack([m(G0).squeeze(),m(G1).squeeze()])
  acc=((o>0).float()==y).float().mean().item()
 return loss.item(),acc
print(f"Train to separate the 80-vertex parity pair G0 vs G1 (theory: tri_square1 CAN, tri_square2 CANNOT)\n")
print(f"{'mode':14}{'final_loss':14}{'accuracy':10}verdict")
for mode in ['tri_square2','tri_square1']:
 loss,acc=train(mode)
 v='separates (learns)' if acc==1.0 else 'CANNOT separate (stuck at chance)'
 print(f"{mode:14}{loss:<14.4f}{acc:<10.2f}{v}")
