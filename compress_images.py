from PIL import Image
import os

def compress_images(input_folder, output_folder, compression_quality):
    for filename in os.listdir(input_folder):
        if filename.endswith((".jpg", ".jpeg", ".png")):
            # 입력 이미지 경로
            input_path = os.path.join(input_folder, filename)
            # 출력 이미지 경로
            output_path = os.path.join(output_folder, filename)

            # 이미지 압축
            with Image.open(input_path) as img:
                img.save(output_path, quality=compression_quality)
                print(f"Compressed: {filename}")

input_folder = "input_images_folder"
output_folder = "output_images_folder"
compression_quality = 70  # 압축 품질 (0 ~ 100)

compress_images(input_folder, output_folder, compression_quality)
