import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# =========================
# CONFIG
# =========================
IMAGES_DIR = os.path.join("assets", "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

# Colors
BG_DARK = (8, 15, 30)
CYAN = (0, 220, 255)
CYAN_GLOW = (80, 255, 255)
BLUE = (0, 120, 255)
WHITE = (240, 245, 255)
YELLOW = (255, 220, 0)
YELLOW_GLOW = (255, 245, 120)
RED = (255, 80, 80)
GREEN = (0, 255, 140)
GRAY = (55, 65, 85)
DARK_GRAY = (30, 35, 45)
BLACK = (0, 0, 0)

# =========================
# HELPERS
# =========================
def save_image(img, filename):
    path = os.path.join(IMAGES_DIR, filename)
    img.save(path)
    print(f"Generated: {path}")

def create_canvas(size, color=(0, 0, 0, 0)):
    return Image.new("RGBA", size, color)

def glow_effect(base_img, blur_radius=8):
    glow = base_img.filter(ImageFilter.GaussianBlur(blur_radius))
    return glow

def draw_glowing_rect(size, fill_color, glow_color, border_radius=8, glow_blur=8):
    img = create_canvas(size)
    glow_layer = create_canvas(size)
    glow_draw = ImageDraw.Draw(glow_layer)

    # Glow larger rect
    pad = 4
    glow_draw.rounded_rectangle(
        [pad, pad, size[0]-pad, size[1]-pad],
        radius=border_radius,
        fill=glow_color
    )
    glow_layer = glow_effect(glow_layer, glow_blur)

    # Main rect
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(
        [8, 8, size[0]-8, size[1]-8],
        radius=border_radius,
        fill=fill_color
    )

    # Border
    draw.rounded_rectangle(
        [8, 8, size[0]-8, size[1]-8],
        radius=border_radius,
        outline=WHITE,
        width=2
    )

    final = Image.alpha_composite(glow_layer, img)
    return final

def get_font(size=24):
    # Try common fonts; fallback to default
    font_candidates = [
        "arial.ttf",
        "Arial.ttf",
        "DejaVuSans-Bold.ttf",
        "DejaVuSans.ttf"
    ]
    for f in font_candidates:
        try:
            return ImageFont.truetype(f, size)
        except:
            continue
    return ImageFont.load_default()

# =========================
# GENERATORS
# =========================
def generate_player():
    """
    32x32 neon bot-like player icon
    """
    size = (32, 32)
    img = create_canvas(size)
    glow = create_canvas(size)
    glow_draw = ImageDraw.Draw(glow)

    # Glow body
    glow_draw.rounded_rectangle([6, 6, 26, 26], radius=6, fill=CYAN_GLOW)
    glow = glow_effect(glow, 5)

    draw = ImageDraw.Draw(img)

    # Body
    draw.rounded_rectangle([7, 7, 25, 25], radius=6, fill=BLUE, outline=WHITE, width=2)

    # Eyes
    draw.rectangle([11, 13, 14, 16], fill=WHITE)
    draw.rectangle([18, 13, 21, 16], fill=WHITE)

    # Mouth line
    draw.line([12, 21, 20, 21], fill=WHITE, width=2)

    final = Image.alpha_composite(glow, img)
    save_image(final, "player.png")

def generate_wall():
    """
    32x32 sci-fi wall tile
    """
    size = (32, 32)
    img = create_canvas(size)
    draw = ImageDraw.Draw(img)

    # Base tile
    draw.rounded_rectangle([0, 0, 31, 31], radius=4, fill=DARK_GRAY)

    # Inner panel
    draw.rounded_rectangle([3, 3, 28, 28], radius=4, fill=GRAY)

    # Tech lines
    draw.line([6, 8, 26, 8], fill=CYAN, width=2)
    draw.line([6, 24, 26, 24], fill=CYAN, width=2)
    draw.line([8, 6, 8, 26], fill=WHITE, width=1)
    draw.line([24, 6, 24, 26], fill=WHITE, width=1)

    # Center detail
    draw.rectangle([13, 13, 19, 19], fill=CYAN)

    save_image(img, "wall.png")

def generate_key():
    """
    24x24 glowing key icon
    """
    size = (24, 24)
    img = create_canvas(size)
    glow = create_canvas(size)

    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse([2, 2, 12, 12], fill=YELLOW_GLOW)
    glow_draw.rectangle([10, 6, 19, 10], fill=YELLOW_GLOW)
    glow_draw.rectangle([16, 10, 18, 13], fill=YELLOW_GLOW)
    glow_draw.rectangle([13, 10, 15, 12], fill=YELLOW_GLOW)
    glow = glow_effect(glow, 5)

    draw = ImageDraw.Draw(img)
    draw.ellipse([4, 4, 12, 12], outline=WHITE, width=2, fill=YELLOW)
    draw.rectangle([10, 7, 19, 9], fill=YELLOW)
    draw.rectangle([16, 9, 18, 12], fill=YELLOW)
    draw.rectangle([13, 9, 15, 11], fill=YELLOW)

    final = Image.alpha_composite(glow, img)
    save_image(final, "key.png")

def generate_door_locked():
    """
    40x60 locked red sci-fi door
    """
    size = (40, 60)
    img = create_canvas(size)
    glow = create_canvas(size)

    glow_draw = ImageDraw.Draw(glow)
    glow_draw.rounded_rectangle([4, 4, 36, 56], radius=6, fill=(255, 100, 100, 180))
    glow = glow_effect(glow, 6)

    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([6, 6, 34, 54], radius=6, fill=(80, 20, 20), outline=WHITE, width=2)

    # Inner panel
    draw.rounded_rectangle([11, 12, 29, 48], radius=4, fill=RED)

    # Lock symbol
    draw.arc([14, 18, 26, 30], start=180, end=360, fill=WHITE, width=2)
    draw.rectangle([16, 24, 24, 34], fill=WHITE)

    # Side lights
    draw.line([9, 14, 9, 46], fill=WHITE, width=1)
    draw.line([31, 14, 31, 46], fill=WHITE, width=1)

    final = Image.alpha_composite(glow, img)
    save_image(final, "door_locked.png")

def generate_door_unlocked():
    """
    40x60 unlocked green sci-fi door
    """
    size = (40, 60)
    img = create_canvas(size)
    glow = create_canvas(size)

    glow_draw = ImageDraw.Draw(glow)
    glow_draw.rounded_rectangle([4, 4, 36, 56], radius=6, fill=(100, 255, 160, 180))
    glow = glow_effect(glow, 6)

    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([6, 6, 34, 54], radius=6, fill=(10, 60, 35), outline=WHITE, width=2)

    # Inner panel
    draw.rounded_rectangle([11, 12, 29, 48], radius=4, fill=GREEN)

    # Unlock symbol
    draw.arc([14, 18, 26, 30], start=220, end=360, fill=WHITE, width=2)
    draw.rectangle([16, 24, 24, 34], fill=WHITE)

    # Side lights
    draw.line([9, 14, 9, 46], fill=WHITE, width=1)
    draw.line([31, 14, 31, 46], fill=WHITE, width=1)

    final = Image.alpha_composite(glow, img)
    save_image(final, "door_unlocked.png")

def generate_background():
    """
    800x600 cyber grid background
    """
    size = (800, 600)
    img = create_canvas(size, BG_DARK)
    draw = ImageDraw.Draw(img)

    # Gradient-ish horizontal bars
    for y in range(0, 600, 4):
        alpha = int(15 + (y / 600) * 20)
        line_color = (10, 25, 45, alpha)
        line = create_canvas(size)
        line_draw = ImageDraw.Draw(line)
        line_draw.line([0, y, 800, y], fill=line_color, width=1)
        img = Image.alpha_composite(img, line)

    # Grid lines
    grid = create_canvas(size)
    gdraw = ImageDraw.Draw(grid)

    for x in range(0, 800, 40):
        gdraw.line([x, 0, x, 600], fill=(0, 180, 255, 35), width=1)

    for y in range(0, 600, 40):
        gdraw.line([0, y, 800, y], fill=(0, 180, 255, 35), width=1)

    # Stronger major lines
    for x in range(0, 800, 160):
        gdraw.line([x, 0, x, 600], fill=(80, 255, 255, 70), width=2)

    for y in range(0, 600, 160):
        gdraw.line([0, y, 800, y], fill=(80, 255, 255, 70), width=2)

    grid = glow_effect(grid, 1)
    img = Image.alpha_composite(img, grid)

    # Decorative HUD corners
    hud = create_canvas(size)
    hdraw = ImageDraw.Draw(hud)

    # Top-left
    hdraw.line([20, 20, 120, 20], fill=CYAN, width=3)
    hdraw.line([20, 20, 20, 80], fill=CYAN, width=3)

    # Top-right
    hdraw.line([680, 20, 780, 20], fill=CYAN, width=3)
    hdraw.line([780, 20, 780, 80], fill=CYAN, width=3)

    # Bottom-left
    hdraw.line([20, 580, 120, 580], fill=CYAN, width=3)
    hdraw.line([20, 520, 20, 580], fill=CYAN, width=3)

    # Bottom-right
    hdraw.line([680, 580, 780, 580], fill=CYAN, width=3)
    hdraw.line([780, 520, 780, 580], fill=CYAN, width=3)

    hud = glow_effect(hud, 2)
    img = Image.alpha_composite(img, hud)

    save_image(img, "background.png")

def generate_logo():
    """
    500x140 logo image with LearnPy Quest text
    """
    size = (500, 140)
    img = create_canvas(size)
    glow = create_canvas(size)

    font_big = get_font(42)
    font_small = get_font(18)

    # Glow text
    gdraw = ImageDraw.Draw(glow)
    gdraw.text((40, 35), "LearnPy", font=font_big, fill=CYAN_GLOW)
    gdraw.text((250, 35), "Quest", font=font_big, fill=YELLOW_GLOW)
    glow = glow_effect(glow, 8)

    draw = ImageDraw.Draw(img)

    # Title text
    draw.text((40, 35), "LearnPy", font=font_big, fill=CYAN)
    draw.text((250, 35), "Quest", font=font_big, fill=YELLOW)

    # Subtitle
    draw.text((45, 90), "Python Basics Through Gameplay", font=font_small, fill=WHITE)

    # Decorative underline
    draw.line([45, 82, 430, 82], fill=WHITE, width=2)

    final = Image.alpha_composite(glow, img)
    save_image(final, "logo.png")

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    print("Generating LearnPy Quest image assets...\n")
    generate_player()
    generate_wall()
    generate_key()
    generate_door_locked()
    generate_door_unlocked()
    generate_background()
    generate_logo()
    print("\nAll image files generated successfully in assets/images/")