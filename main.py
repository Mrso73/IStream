import pygame
import pygame.camera


import threading
import inference as llm

frame_string = "frame.png"

pygame.init()
gameDisplay = pygame.display.set_mode((640,480))

pygame.camera.init()
print (pygame.camera.list_cameras())

cam = pygame.camera.Camera(0)
cam.start()


def run_llm():
    base64_string = llm.img_to_b64(frame_string)
    llm.generate_comments(base64_string) 


while True:
   
    img = cam.get_image()
    gameDisplay.blit(img,(0,0))

    pygame.display.update()
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:    
            cam.stop()
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:

                pygame.image.save(gameDisplay, frame_string)  

                thread = threading.Thread(target=run_llm)
                thread.start()      
                


