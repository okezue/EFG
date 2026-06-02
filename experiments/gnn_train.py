import torch,torch.nn as nn,networkx as nx
from motifgnn.model import EdgeMotifGNN
from motifwl.wl import canonical_edge_motif_signature as csig
torch.manual_seed(0)
def U(a,b):return nx.disjoint_union(a,b)
PAIRS=[("C3+C3 vs C6",U(nx.cycle_graph(3),nx.cycle_graph(3)),nx.cycle_graph(6)),
       ("C4+C4 vs C8",U(nx.cycle_graph(4),nx.cycle_graph(4)),nx.cycle_graph(8))]
MODES=["tri","square1","square2","tri_square1","tri_square2"]
def train(G,H,mode,steps=400,lr=5e-3):
 m=EdgeMotifGNN(d=32,layers=4,mode=mode,out=1)
 opt=torch.optim.Adam(m.parameters(),lr=lr);lf=nn.BCEWithLogitsLoss();y=torch.tensor([0.,1.])
 for _ in range(steps):
  opt.zero_grad();out=torch.stack([m(G).squeeze(),m(H).squeeze()])
  loss=lf(out,y);loss.backward();opt.step()
 with torch.no_grad():
  o=torch.stack([m(G).squeeze(),m(H).squeeze()]);acc=((o>0).float()==y).float().mean().item()
 return acc
print(f"Train each mode to classify each witness pair. Accuracy should be 1.0 iff the\nmode discretely distinguishes the pair, else 0.5 (provably cannot).\n")
print(f"{'pair':16}{'mode':14}{'discrete_distinguishes':24}{'trained_acc':12}match")
ok=tot=0
for name,G,H in PAIRS:
 for mode in MODES:
  dd=csig(G,mode)!=csig(H,mode);acc=train(G,H,mode)
  learned=acc==1.0;tot+=1;ok+=dd==learned
  print(f"{name:16}{mode:14}{str(dd):24}{acc:<12.2f}{'OK' if dd==learned else 'MISMATCH'}")
print(f"\ntrained learnability matches discrete expressivity on {ok}/{tot} cases")
