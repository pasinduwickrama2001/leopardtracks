import os
from PIL import Image, ImageDraw, ImageFilter

def create_pastel_cream_logo_assets():
    output_dir = "static/images"
    os.makedirs(output_dir, exist_ok=True)

    size = 1024
    
    # Exact Colors:
    # Background: pastel-cream (#FAF6EE -> RGB: 250, 246, 238)
    pastel_cream = (250, 246, 238, 255)
    # Leopard Track: button bg color olive-btn (#606C38 -> RGB: 96, 108, 56)
    olive_btn = (96, 108, 56, 255)
    olive_dark = (71, 81, 40, 255)

    # 1. Base Image Canvas with pastel-cream background
    img = Image.new("RGBA", (size, size), pastel_cream)
    
    # Subtle Soft Outer Ring / Glow in olive-btn tint
    glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw_glow = ImageDraw.Draw(glow)
    center = size // 2
    for r in range(480, 0, -8):
        alpha = int(25 * (1 - r / 480))
        draw_glow.ellipse([center - r, center - r, center + r, center + r], fill=(96, 108, 56, alpha))
    img = Image.alpha_composite(img, glow)

    # 2. Leopard Track Layer using button bg color (olive-btn #606C38)
    track_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))

    def draw_toe(x, y, rx, ry, angle=0):
        t_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        td = ImageDraw.Draw(t_img)
        td.ellipse([x - rx, y - ry, x + rx, y + ry], fill=olive_btn)
        if angle != 0:
            t_img = t_img.rotate(angle, center=(x, y))
        return t_img

    # 4 Digital Toe Pads (Feline - No Claws)
    t1 = draw_toe(320, 380, 52, 72, angle=22)
    t2 = draw_toe(435, 260, 62, 88, angle=8)
    t3 = draw_toe(585, 270, 62, 86, angle=-8)
    t4 = draw_toe(700, 390, 52, 72, angle=-22)

    for toe in [t1, t2, t3, t4]:
        track_layer = Image.alpha_composite(track_layer, toe)

    # Feline Metacarpal Heel Pad (3-lobed base)
    heel_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    hd = ImageDraw.Draw(heel_img)
    heel_pts = [
        (370, 550), (430, 520), (512, 560), (594, 520), (654, 550),
        (715, 630), (705, 700), (640, 740), (512, 730), (384, 740),
        (319, 700), (309, 630)
    ]
    hd.polygon(heel_pts, fill=olive_btn)
    track_layer = Image.alpha_composite(track_layer, heel_img)

    # Soft subtle shadow in olive-dark tint
    shadow = track_layer.split()[3].filter(ImageFilter.GaussianBlur(10))
    shadow_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    shadow_img.paste((71, 81, 40, 90), mask=shadow)

    final_img = Image.alpha_composite(img, shadow_img)
    final_img = Image.alpha_composite(final_img, track_layer)

    # Save PNG Assets
    final_img.save(os.path.join(output_dir, "theme-share-card.png"))
    final_img.save(os.path.join(output_dir, "logo-official.png"))
    final_img.save(os.path.join(output_dir, "logo.png"))

    # Favicons with pastel-cream background & olive-btn track footprint
    fav = final_img.resize((192, 192), Image.Resampling.LANCZOS)
    fav.save(os.path.join(output_dir, "favicon.png"))
    fav.save(os.path.join(output_dir, "apple-touch-icon.png"))

    fav_ico = final_img.resize((32, 32), Image.Resampling.LANCZOS)
    fav_ico.save(os.path.join(output_dir, "favicon.ico"))

    # SVG Asset with pastel-cream background & olive-btn fill
    svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="512" height="512" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect width="100" height="100" rx="20" fill="#FAF6EE"/>
    <path d="M 22 36 C 16 36 13 44 18 51 C 23 57 29 51 28 43 C 27 38 25 36 22 36 Z" fill="#606C38"/>
    <path d="M 40 18 C 33 18 31 27 35 34 C 39 41 46 35 45 26 C 44 20 42 18 40 18 Z" fill="#606C38"/>
    <path d="M 60 20 C 58 20 56 22 55 28 C 54 37 61 43 65 36 C 69 29 67 20 60 20 Z" fill="#606C38"/>
    <path d="M 78 38 C 75 38 73 40 72 45 C 71 53 77 59 82 53 C 87 46 84 38 78 38 Z" fill="#606C38"/>
    <path d="M 34 60 C 25 60 20 70 26 79 C 32 87 40 88 50 88 C 60 88 68 87 74 79 C 80 70 75 60 66 60 C 59 60 56 64 50 64 C 44 64 41 60 34 60 Z" fill="#606C38"/>
</svg>
'''
    with open(os.path.join(output_dir, "logo.svg"), "w") as f:
        f.write(svg_content)

    print("Updated logo assets with pastel-cream background (#FAF6EE) and olive button track color (#606C38)!")

if __name__ == "__main__":
    create_pastel_cream_logo_assets()
