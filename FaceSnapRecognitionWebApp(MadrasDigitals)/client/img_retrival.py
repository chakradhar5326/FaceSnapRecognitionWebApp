from . import face_rec
import shutil
import os 

target_path = 'C:\\Users\\User\\Desktop\\21.8.23\\'
reference_path = "C:\\Users\\User\\Desktop\\21.8.23\\_DSC0990.jpg"
import os
import shutil
from . import face_rec

def image_retrival(target_path, reference_path, directory_name):
    Selected_Images = face_rec.face_recognition_(reference_path, target_path)
    print(Selected_Images)
    
    parent_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'images', 'prd_images')
    path = os.path.join(parent_dir, directory_name) 
    os.makedirs(path, exist_ok=True)
    print("Directory '%s' created" % directory_name)

    destination = os.path.join(parent_dir, str(directory_name))
    for f in Selected_Images:
        src_path = os.path.join(target_path, f)
        dst_path = os.path.join(destination, f)
        shutil.copy(src_path, dst_path)
    print("Successfully copied.")
    return Selected_Images

    