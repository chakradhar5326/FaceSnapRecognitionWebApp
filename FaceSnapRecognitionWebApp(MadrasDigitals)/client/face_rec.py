import face_recognition
import os
import cv2
import numpy as np

def resize_and_compress_image(image_path, target_size_kb=300):
    img = cv2.imread(image_path)
    h, w, _ = img.shape
    target_size_bytes = target_size_kb * 1024
    
    # Compute the compression ratio needed to achieve target size
    compression_ratio = np.sqrt(target_size_bytes / (h * w * 3))
    
    # Resize the image while preserving aspect ratio
    img = cv2.resize(img, (int(w * compression_ratio), int(h * compression_ratio)))
    
    # Convert to JPEG format with compression quality 90
    _, encoded_img = cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    
    return encoded_img.tobytes()

def face_recognition_(reference_path, target_path, tolerance=0.65):
    # Load and encode the reference image
    Rimage = cv2.imread(reference_path)
    Rimage = cv2.resize(Rimage, (0, 0), None, 0.25, 0.25)
    Rimage = cv2.cvtColor(Rimage, cv2.COLOR_BGR2RGB)
    faceRimage = face_recognition.face_locations(Rimage)
    reference_face_encoding = face_recognition.face_encodings(Rimage, faceRimage)[0]
    images_path = []
    
    for filename in os.listdir(target_path):
        if filename.endswith(('.JPG', '.jpg', '.jpeg', '.png', '.gif', '.bmp')):
            target_image_path = os.path.join(target_path, filename)
            
            # Resize and compress the image
            image_bytes = resize_and_compress_image(target_image_path)
            image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
            
            # Convert the image to RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Find face locations and encodings
            face_locations = face_recognition.face_locations(image)
            target_face_encodings = face_recognition.face_encodings(image, face_locations)
            
            if target_face_encodings:
                # Face Comparison is Started
                results=[]
                for encoding in target_face_encodings:
                    result = face_recognition.compare_faces([reference_face_encoding], encoding, tolerance=tolerance)
                    results.append(result[0])
                
                print(results)
                if True in results:
                    print("It's a picture of me!", target_image_path)
                    images_path.append(filename)
                else:
                    print("It's not a picture of me!", target_image_path)
    return images_path

if __name__== "__main__":
    print(os.path.basename(__file__))
    reference_image_path = "C:\\Users\\User\\Desktop\\crud_on_student\\IMG20230519173848.jpg"
    target_images_path = "C:\\Users\\User\\Desktop\\target"
    print(face_recognition_(reference_image_path, target_images_path))
