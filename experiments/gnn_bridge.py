import torch,networkx as nx
from motifgnn.model import EdgeMotifGNN
from motifwl.wl import canonical_edge_motif_signature as csig
from motifwl.parity import private_triangle_parity_pair
torch.manual_seed(0)
def U(a,b):return nx.disjoint_union(a,b)
def pairs():
 yield "C3+C3 vs C6",U(nx.cycle_graph(3),nx.cycle_graph(3)),nx.cycle_graph(6)
 yield "C4+C4 vs C8",U(nx.cycle_graph(4),nx.cycle_graph(4)),nx.cycle_graph(8)
 yield "C5+C5 vs C10",U(nx.cycle_graph(5),nx.cycle_graph(5)),nx.cycle_graph(10)
 g0,g1=private_triangle_parity_pair(d=1);yield "parity80 (G0 vs G1)",g0,g1
MODES=["tri","square1","square2","tri_square1","tri_square2"]
def main():
 print(f"{'pair':24}{'mode':14}{'discrete_sep':14}{'neural_sep':12}match")
 ok=tot=0
 for name,G,H in pairs():
  for m in MODES:
   mdl=EdgeMotifGNN(d=32,layers=4,mode=m).eval()
   with torch.no_grad():d=(mdl.embed(G)-mdl.embed(H)).abs().max().item()
   ds=csig(G,m)!=csig(H,m);ns=d>1e-3;tot+=1;ok+=ds==ns
   print(f"{name:24}{m:14}{str(ds):14}{str(ns):12}{'OK' if ds==ns else 'MISMATCH (d=%.2g)'%d}")
 print(f"\nneural matches discrete refinement on {ok}/{tot} (pair,mode) cases")
if __name__=="__main__":main()
