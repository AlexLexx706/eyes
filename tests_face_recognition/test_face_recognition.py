import face_recognition
image = face_recognition.load_image_file("./images/test_1.jpg")
print(type(image))
face_locations = face_recognition.face_locations(image)
print(face_locations)