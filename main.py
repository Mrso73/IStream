import inference as llm

import pygame
import pygame.camera

import threading


frame_image_name = "frame.png"

# Start pygame
pygame.init()
gameDisplay = pygame.display.set_mode((640,480))

# Open the webcam
pygame.camera.init()
cam = pygame.camera.Camera(0)
cam.start()


def run_llm_thread():
     
    # Convert a frame into base 64 to send it to the llm 
    base64_string = llm.img_to_b64(frame_string)
    llm.generate_comments(base64_string) 


# Main loop
while True:
   
    # Draw the current webcame frame
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
                
                # Save the current frame
                pygame.image.save(gameDisplay, frame_image_name)  

                # Create a new thread to calculate the llm response
                thread = threading.Thread(target=run_llm_thread)
                thread.start()      
                
