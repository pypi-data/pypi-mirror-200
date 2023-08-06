"""
tk_r_em network suites designed to restore different modalities of electron microscopy data

Author: Ivan Lobato
Email: Ivanlh20@gmail.com
"""

import os
import matplotlib

# Check if running on remote SSH and use appropriate backend for matplotlib
remote_ssh = "SSH_CONNECTION" in os.environ
matplotlib.use('Agg' if remote_ssh else 'TkAgg')
import matplotlib.pyplot as plt

from tk_r_em.model import load_network, load_test_data

def fcn_inference():
    # select one of the available networks from [hrsem, lrsem, hrstem, lrstem, hrtem, lrtem]
    net_name = 'hrstem'

    # load its corresponding data
    x, y = load_test_data(net_name)

    # load its corresponding model
    r_em_nn = load_network(net_name)
    r_em_nn.summary()

    n_data = x.shape[0]
    batch_size = 16

    # run inference
    y_p = r_em_nn.predict(x, batch_size)

    fig, axs = plt.subplots(1, 3, figsize=(12, 6))

    cb = [None, None, None]

    for ik in range(n_data):
        x_ik = x[ik, :, :, 0].squeeze()
        y_ik = y[ik, :, :, 0].squeeze()
        y_p_ik = y_p[ik, :, :, 0].squeeze()

        vmin = min(y_ik.min(), y_p_ik.min())
        vmax = max(y_ik.max(), y_p_ik.max())

        axs[0].imshow(x_ik, cmap='viridis')
        axs[0].set_xticks([])
        axs[0].set_yticks([])
        axs[0].grid(False)
        axs[0].set_title(f"Detected {net_name} image", fontsize=14)
        if cb[0] is not None:
            cb[0].remove()
        cb[0] = fig.colorbar(axs[0].images[0], ax=axs[0], orientation='vertical', shrink=0.6)

        axs[1].imshow(y_p_ik, vmin=vmin, vmax=vmax, cmap='viridis')
        axs[1].set_xticks([])
        axs[1].set_yticks([])
        axs[1].grid(False)
        axs[1].set_title(f"Restored {net_name} image", fontsize=14)
        if cb[1] is not None:
            cb[1].remove()
        cb[1] = fig.colorbar(axs[1].images[0], ax=axs[1], orientation='vertical', shrink=0.6)

        axs[2].imshow(y_ik, vmin=vmin, vmax=vmax, cmap='viridis')
        axs[2].set_xticks([])
        axs[2].set_yticks([])
        axs[2].grid(False)
        axs[2].set_title(f"Ground truth {net_name} image", fontsize=14)
        if cb[2] is not None:
            cb[2].remove()
        cb[2] = fig.colorbar(axs[2].images[0], ax=axs[2], orientation='vertical', shrink=0.6)

        if remote_ssh:
            plt.savefig(f"restored_{net_name}.png", format='png')
        else:
            fig.show()

        print(ik)

if __name__ == '__main__':
    fcn_inference()