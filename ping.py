import time
import subprocess
import sys
import os
import pygame

def play_sound_loop(sound_file):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play(-1) 
    except Exception as e:
        print(f"Sound error: {e}")

def stop_sound():
    try:
        pygame.mixer.music.stop()
    except Exception as e:
        print(f"Sound stop error: {e}")

def ping_and_alert(target, lost_sound_file, restored_sound_file, interval=1):
    connection_lost = False  

    while True:
        try:
            ping_cmd = ["ping", "-n", "1", target] if "win" in sys.platform else ["ping", "-c", "1", target]
            result = subprocess.run(
                ping_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            if result.returncode == 0:  
                if connection_lost:  
                    print(f"Ping to {target} succeeded. Connection restored!")
                    stop_sound()  
                    play_sound_loop(restored_sound_file)  
                    time.sleep(4.5)  
                    stop_sound()  
                    connection_lost = False  
                else:
                    print(f"Ping to {target} succeeded. Continuing...")
            else:  
                if not connection_lost:  
                    print(f"Ping to {target} failed. Connection lost!")
                    play_sound_loop(lost_sound_file)  
                    connection_lost = True 
                
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(interval)

if __name__ == "__main__":
    target = "google.com"  
    lost_sound_file = "assets/box.mp3"  
    restored_sound_file = "assets/restored.mp3"  
    
    # Verify sound files exist
    if not os.path.exists(lost_sound_file):
        print(f"Error: Sound file '{lost_sound_file}' not found!")
    elif not os.path.exists(restored_sound_file):
        print(f"Error: Sound file '{restored_sound_file}' not found!")
    else:
        ping_and_alert(target, lost_sound_file, restored_sound_file)