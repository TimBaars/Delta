import cv2
import numpy as np
import os

class SegmentationProcessor:
    def __init__(self, txt_path, img_path, output_dir):
        self.txt_path = txt_path
        self.img_path = img_path
        self.output_dir = output_dir

    def process_segmentation_file(self):
        original_img = cv2.imread(self.img_path)
        height, width = original_img.shape[:2]

        bw_img = np.ones((height, width, 3), dtype=np.uint8) * 255  # Use a 3-channel image for color

        with open(self.txt_path, 'r') as file:
            for line in file.readlines():
                parts = list(map(float, line.split()))
                class_id = int(parts[0])
                points = np.array([(int(x*width), int(y*height)) for x, y in zip(parts[1::2], parts[2::2])], np.int32)
                points = points.reshape((-1, 1, 2))

                if class_id == 0:  # For roses, draw filled polygons
                    cv2.fillPoly(bw_img, [points], (0, 0, 0))
                elif class_id == 1:  # For weeds, mark with a circle
                    center_x = np.mean(points[:, :, 0])
                    center_y = np.mean(points[:, :, 1])
                    cv2.circle(bw_img, (int(center_x), int(center_y)), 10, (0, 0, 255), -1)
        
        composite_img = np.hstack((original_img, bw_img))
        composite_output_path = f"{self.output_dir}/composite_{os.path.basename(self.img_path)}"
        cv2.imwrite(composite_output_path, bw_img)
        #cv2.imwrite(composite_output_path, composite_img)

def process_folder(image_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file_name in os.listdir(image_dir):
        if file_name.endswith('.jpg'):  # Assuming images are in JPG format
            base_name = os.path.splitext(file_name)[0]
            txt_path = os.path.join(image_dir, base_name + '.txt')
            img_path = os.path.join(image_dir, file_name)
            if os.path.exists(txt_path):
                processor = SegmentationProcessor(txt_path, img_path, output_dir)
                processor.process_segmentation_file()
            else:
                print(f"No corresponding .txt file for {file_name}")

# Example usage
image_dir = 'dataset'
output_dir = 'Testing'
process_folder(image_dir, output_dir)
