# Gripper

sudo docker build -t gripper .

sudo docker run -d 
-v ~/Roms:/RETRODE 
-v ~/testRom:/rom 
-e api-key=GIANT_BOMB_API_KEY
--name=Gripper gripper