from matplotlib import pyplot as plt

tab20 = plt.get_cmap("tab20")

def get_color(idx):
    base_idx = idx % 16
    layer = idx // 16

    # --- Anpassung: überspringe Index 6 ---
    if base_idx >= 6:
        base_idx += 1  # 6 wird übersprungen

    rgba = tab20(base_idx / 20)  # Skaliere auf 20 Farben
    r, g, b, _ = rgba
    if layer == 1:
        r = max(0.0, r * 0.9)
        g = min(1.0, g * 1.4)
        b = max(0.0, b * 0.9)
    elif layer == 2:
        r = min(1.0, r * 1.15)
        g = max(0.0, g * 0.85)
        b = min(1.0, b * 1.15)

    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)
    return f'#{r:02x}{g:02x}{b:02x}'


class Job:
    def __init__(self, job_id, color_idx):
        self.job_id = job_id
        self.color = get_color(color_idx)

