import cloudinary
import cloudinary.uploader
import os

# Configurar Cloudinary
cloudinary.config(
    cloud_name="devfncp85",
    api_key="498194629494134",
    api_secret="_EhddXk2IJtd7bjU8ZTuCusdN0Y"
)

def subir_imagenes():
    media_path = "media"
    
    # Subir imágenes de la carpeta images
    images_path = os.path.join(media_path, "images")
    if os.path.exists(images_path):
        for filename in os.listdir(images_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(images_path, filename)
                print(f"Subiendo imagen: {filename}")
                try:
                    result = cloudinary.uploader.upload(
                        file_path,
                        folder="images",
                        public_id=filename.split('.')[0]
                    )
                    print(f"✅ Subido: {result['secure_url']}")
                except Exception as e:
                    print(f"❌ Error subiendo {filename}: {str(e)}")
    
    # Subir logos
    logos_path = os.path.join(media_path, "logos")
    if os.path.exists(logos_path):
        for filename in os.listdir(logos_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(logos_path, filename)
                print(f"Subiendo logo: {filename}")
                try:
                    result = cloudinary.uploader.upload(
                        file_path,
                        folder="logos",
                        public_id=filename.split('.')[0]
                    )
                    print(f"✅ Subido: {result['secure_url']}")
                except Exception as e:
                    print(f"❌ Error subiendo {filename}: {str(e)}")
    
    # Subir fotos
    fotos_path = os.path.join(media_path, "fotos")
    if os.path.exists(fotos_path):
        for filename in os.listdir(fotos_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(fotos_path, filename)
                print(f"Subiendo foto: {filename}")
                try:
                    result = cloudinary.uploader.upload(
                        file_path,
                        folder="fotos",
                        public_id=filename.split('.')[0]
                    )
                    print(f"✅ Subido: {result['secure_url']}")
                except Exception as e:
                    print(f"❌ Error subiendo {filename}: {str(e)}")

if __name__ == "__main__":
    subir_imagenes()
    print("🎉 ¡Proceso de subida completado!")