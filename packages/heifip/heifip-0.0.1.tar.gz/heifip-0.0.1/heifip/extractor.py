import os

from PIL import Image as PILImage

from heifip.exceptions import FIPWrongParameterException
from heifip.images import NetworkTrafficImage
from heifip.images.flow import FlowImage
from heifip.images.packet import PacketImage
from heifip.layers import PacketProcessor, PacketProcessorType


class FIPExtractor:
    def __init__(self):
        self.processor = PacketProcessor()
        self.images_created = []
    
    def verify(self, image, min_image_dim: int, max_image_dim: int, remove_duplicates: bool):
        if image.shape[0] < min_image_dim or image.shape[1] < min_image_dim:
            return False

        if max_image_dim != 0 and (max_image_dim < image.shape[0] or max_image_dim < image.shape[1]):
            return False

        if remove_duplicates:
            im_str = image.tobytes()
            if im_str in self.images_created:
                return False 
            else:
                self.images_created.append(im_str)

        return True

    def create_image(
            self,
            input_file: str,
            preprocessing_type: PacketProcessorType = PacketProcessorType.NONE,
            image_type: NetworkTrafficImage = PacketImage,
            min_image_dim: int = 0,
            max_image_dim: int = 0,
            min_packets_per_flow: int = 0,
            remove_duplicates: bool = False,
            *args
        ):

        assert os.path.isfile(input_file)

        packets = self.processor.read_packets(input_file, preprocessing_type)

        images = []
        if image_type == FlowImage:
            # when no file matches the preprocessing
            if len(packets) == 0 or len(packets) < min_packets_per_flow:
                return images

            image = FlowImage(packets, *args)
            if self.verify(image.matrix, min_image_dim, max_image_dim, remove_duplicates):
                images.append(image.matrix)
        elif image_type  == PacketImage:
            for packet in packets:
                image = PacketImage(packet, *args)
                if self.verify(image.matrix, min_image_dim, max_image_dim, remove_duplicates):
                    images.append(image.matrix)
        else:
            raise FIPWrongParameterException

        return images

    def save_image(self, img, output_dir):
        pil_img = PILImage.fromarray(img)
        if not os.path.exists(os.path.realpath(os.path.dirname(output_dir))):
            os.makedirs(os.path.realpath(os.path.dirname(output_dir)))
        pil_img.save(f"{output_dir}_processed.png")
