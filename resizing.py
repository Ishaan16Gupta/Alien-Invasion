import pygame as pg

pg.init()

# Load original image
image = pg.image.load("images/laserBullet.bmp")

# Resize it to new dimensions (e.g., 40x40)
resized_image = pg.transform.scale(image, (3,12))

# Save the resized image back to file
pg.image.save(resized_image, "images/laserBullet_resized.bmp")

pg.quit()
