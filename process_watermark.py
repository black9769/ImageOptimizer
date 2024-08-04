import logging
import os
from PIL import Image

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 배경 이미지가 위치한 디렉토리
background_dir = r'C:\Users\박정준PC\Documents\watermarkprocess\m_bg'
# 워터마크 이미지 파일 경로
watermark_path = r'C:\Users\박정준PC\Documents\watermarkprocess\watermark.png'
# 결과 이미지를 저장할 디렉토리
output_dir = r'C:\Users\박정준PC\Documents\watermarkprocess\wmbg'

# 디렉토리가 존재하지 않으면 생성
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    logging.info('디렉토리 생성 완료: %s', output_dir)
else:
    logging.info('디렉토리 이미 존재함: %s', output_dir)

try:
    # 워터마크 이미지 열기
    watermark = Image.open(watermark_path).convert("RGBA")
    logging.info('워터마크 이미지 열기 성공: %s', watermark_path)
except Exception as e:
    logging.error('워터마크 이미지 열기 실패: %s', e)
    raise

# 워터마크 크기 조정 (필요시)
watermark_width, watermark_height = watermark.size
new_width = 200  # 새로운 너비 설정 (예: 200 픽셀)
aspect_ratio = watermark_height / watermark_width
new_height = int(new_width * aspect_ratio)

# 최신 Pillow에서는 `Resampling.LANCZOS`를 사용합니다.
watermark = watermark.resize((new_width, new_height), resample=Image.Resampling.LANCZOS)
logging.info('워터마크 이미지 크기 조정 완료: %s x %s', new_width, new_height)

# 배경 이미지 디렉토리에서 모든 이미지 파일을 가져와서 워터마크 추가
for filename in os.listdir(background_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        background_path = os.path.join(background_dir, filename)
        output_path = os.path.join(output_dir, f'{filename}')

        try:
            # 배경 이미지 열기
            background = Image.open(background_path).convert("RGBA")
            logging.info('배경 이미지 열기 성공: %s', background_path)
        except Exception as e:
            logging.error('배경 이미지 열기 실패: %s', e)
            continue

        # 중앙 위치 계산
        bg_width, bg_height = background.size
        wm_width, wm_height = watermark.size
        position = ((bg_width - wm_width) // 2, (bg_height - wm_height) // 2)
        logging.info('워터마크 위치 설정 완료: %s', position)

        # 워터마크 추가
        transparent = Image.new('RGBA', background.size, (0, 0, 0, 0))
        transparent.paste(background, (0, 0))
        transparent.paste(watermark, position, mask=watermark)
        final_image = transparent.convert("RGB")
        logging.info('워터마크 추가 완료')

        # 결과 이미지 저장
        try:
            final_image.save(output_path)
            logging.info('결과 이미지 저장 완료: %s', output_path)
        except Exception as e:
            logging.error('결과 이미지 저장 실패: %s', e)
            continue