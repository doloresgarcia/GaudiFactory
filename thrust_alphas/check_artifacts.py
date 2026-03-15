import numpy as np

rm = np.load('phase3_selection/exec/response_matrix.npz')
print("response_matrix keys:", list(rm.keys()))
print("R shape:", rm['R'].shape)
print("edges:", rm['edges'])
print("efficiency shape:", rm['efficiency'].shape)
print("efficiency values:", rm['efficiency'])
print("diagonal_frac:", rm['diagonal_frac'])

dt = np.load('phase3_selection/exec/hist_tau_data.npz')
print("\nhist_tau_data keys:", list(dt.keys()))
print("data counts sum:", dt['counts'].sum())

bbb = np.load('phase3_selection/exec/bbb_corrections.npz')
print("\nbbb_corrections keys:", list(bbb.keys()))
for k in bbb.keys():
    print(f"  {k}: shape={bbb[k].shape}, first few={bbb[k][:5]}")

cl = np.load('phase3_selection/exec/closure_results.npz')
print("\nclosure_results keys:", list(cl.keys()))

proto = np.load('phase3_selection/exec/prototype_unfolded.npz')
print("\nprototype_unfolded keys:", list(proto.keys()))
for k in proto.keys():
    v = proto[k]
    if hasattr(v, 'shape'):
        print(f"  {k}: shape={v.shape}")
    else:
        print(f"  {k}: {v}")
