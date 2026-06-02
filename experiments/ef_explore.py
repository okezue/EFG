import networkx as nx
from efgames.ef import ef_equiv, spoiler_rank
from efgames.arith_graphs import interval_graph_1d, congruence_graph
from motifwl.wl import canonical_edge_motif_signature as csig, canonical_wl2_signature as c2
MODES=["base","tri","tri_square1","2wl"]
def wl_sep(G,H):
 out=[]
 for m in MODES:
  s=(c2(G)!=c2(H)) if m=="2wl" else (csig(G,m)!=csig(H,m))
  out.append(m if s else f"~{m}")
 return out
def sanity():
 print("=== EF engine sanity ===")
 P2=nx.path_graph(2);P3=nx.path_graph(3)
 print(f"  P2 vs P3 spoiler_rank={spoiler_rank(P2,P3)} (expect small: a degree-2 vertex distinguishes)")
 print(f"  K3 vs K3 ef_equiv r=4 = {ef_equiv(nx.complete_graph(3),nx.complete_graph(3),4)} (expect True)")
 print(f"  K3 vs K4 spoiler_rank={spoiler_rank(nx.complete_graph(3),nx.complete_graph(4))}")
def main():
 sanity()
 print("\n=== Arithmetic constraint graphs: EF rank vs WL distinguishability ===")
 print(f"{'pair':38}{'spoiler_rank(FO)':18}WL_distinguishes")
 pairs=[
  ("C6 vs C3+C3 (both 2-regular)", nx.cycle_graph(6), nx.disjoint_union(nx.cycle_graph(3),nx.cycle_graph(3))),
  ("band N=5,c=1  vs  N=6,c=1", interval_graph_1d(5,1), interval_graph_1d(6,1)),
  ("band N=6,c=2  vs  N=6,c=1", interval_graph_1d(6,2), interval_graph_1d(6,1)),
  ("cong N=6,m=2,r=1 vs band N=6,c=1", congruence_graph(6,2,1), interval_graph_1d(6,1)),
  ("cong N=7,m=3,r=1 vs N=7,m=3,r=2", congruence_graph(7,3,1), congruence_graph(7,3,2)),
 ]
 for name,G,H in pairs:
  sr=spoiler_rank(G,H,maxr=4)
  print(f"{name:38}{str(sr):18}{' '.join(wl_sep(G,H))}")
 print("\n(~mode = that refinement does NOT separate; mode = it does. spoiler_rank=None means EF-equal up to r=4.)")
if __name__=="__main__":main()
