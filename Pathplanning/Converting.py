import cv2
import numpy as np

class SegmentationProcessor:
    def __init__(self, txt_path, img_path, output_dir='Pathplanning'):
        self.txt_path = txt_path
        self.img_path = img_path
        self.output_dir = output_dir

    def process_segmentation_file(self):
        original_img = cv2.imread(self.img_path)
        height, width = original_img.shape[:2]

        bw_img = np.ones((height, width, 3), dtype=np.uint8) * 255  # Use a 3-channel image for color

        weed_centers = []  # List to store the centers of weeds

        with open(self.txt_path, 'r') as file:
            for line in file.readlines():
                parts = list(map(float, line.split()))
                class_id = int(parts[0])
                points = np.array([(int(x*width), int(y*height)) for x, y in zip(parts[1::2], parts[2::2])], np.int32)
                points = points.reshape((-1, 1, 2))

                if class_id == 0:  # For roses, draw filled polygons
                    cv2.fillPoly(bw_img, [points], (0, 0, 0))
                elif class_id == 1:  # For weeds, calculate the geometric center
                    center_x = np.mean(points[:, :, 0])
                    center_y = np.mean(points[:, :, 1])
                    weed_centers.append([center_x, center_y])

        # Save the black and white image to the specified directory
        bw_output_path = f"{self.output_dir}/bw_output.png"
        cv2.imwrite(bw_output_path, bw_img)

        # Optionally, create and save a composite image
        composite_img = np.hstack((original_img, bw_img))
        composite_output_path = f"{self.output_dir}/composite_output.png"
        cv2.imwrite(composite_output_path, composite_img)

        return weed_centers  # Return the list of weed centers