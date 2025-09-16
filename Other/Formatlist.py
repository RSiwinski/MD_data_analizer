def formatlist(min_list, max_list, frame_idx):
        lines = []
        col_width = 20
        lines.append(f"Ramka nr {frame_idx}")
        lines.append(f"{'Min':<{col_width}} | {'Max':<{col_width}}")
        lines.append(f"{'-'*col_width} | {'-'*col_width}")

        for i in range(len(min_list)):
            imin, jmin, vmin = min_list[i]
            min_str = f"({imin},{jmin}): {vmin:.6f}"
            imax, jmax, vmax = max_list[i]
            max_str = f"({imax},{jmax}): {vmax:.6f}"
            lines.append(f"{min_str:<{col_width}} | {max_str:<{col_width}}")

        return "\n".join(lines)