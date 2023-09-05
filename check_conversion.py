import os
import shutil

import numpy as np
from PIL import Image
from pikepdf import Pdf, PdfImage


def pdfs_to_images(source_path, save_path):
    # Get all PDFS
    all_paths = [source_path]

    for filepath in all_paths:

        filename = os.path.splitext(os.path.basename(filepath))[0]

        try:

            # Grab pdf an dload first page
            pdf_file = Pdf.open(filepath)
            page1 = pdf_file.pages[0]
            # Grab image layer
            # rawimage = page1.images['/im1']
            relevant_key = [key for key in page1.images.keys()][0]
            rawimage = page1.images[relevant_key]
            # Convert image
            # print(repr(rawimage.ColorSpace))
            pdfimage = PdfImage(rawimage)
            image = pdfimage.as_pil_image()

            # convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')

            # Save and add to data table
            image.save(f'{save_path}/{filename}.jpg', quality=60)
            return "Pass"

        except Exception as e:
            print(repr(e))

            return "Fail"


def check_output(save_path, expected_output_path):
    if os.path.exists(save_path):
        img = Image.open(save_path)
        img_array = np.array(img)

        expected_img = Image.open(expected_output_path)
        expected_img_array = np.array(expected_img)

        if np.allclose(img_array, expected_img_array):
            return "Pass"
        else:
            return "Fail"
    else:
        return "Skipped"


if __name__ == '__main__':
    root_dir = "./"
    output_dir = "./output"
    expected_output_dir = "./expected_output"

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    test_1 = "87245415-post-herald-and-register-Jun-11-1972-p-1"
    test_2 = "65150963-idaho-state-journal-Jun-11-1972-p-1"
    test_3 = "101250036-jefferson-city-post-tribune-Feb-16-1967-p-1"

    print("============================")
    print("Testing pdf 1 ... (should pass)")
    print("Converting .................", pdfs_to_images(os.path.join(root_dir, test_1 + ".pdf"), output_dir))
    print("Matching expected output ...", check_output(os.path.join(output_dir, test_1 + ".jpg"),
                                                       os.path.join(expected_output_dir, test_1 + ".jpg")))

    print("\n============================")
    print("Testing pdf 2 ... (should fail)")
    print("Converting .................", pdfs_to_images(os.path.join(root_dir, test_2 + ".pdf"), output_dir))
    print("Matching expected output ...", check_output(os.path.join(output_dir, test_2 + ".jpg"),
                                                       os.path.join(expected_output_dir, test_2 + ".jpg")))

    print("\n============================")
    print("Testing pdf 3 ... (should fail)")
    print("Converting .................", pdfs_to_images(os.path.join(root_dir, test_3 + ".pdf"), output_dir))
    print("Matching expected output ...", check_output(os.path.join(output_dir, test_3 + ".jpg"),
                                                       os.path.join(expected_output_dir, test_3 + ".jpg")))

    print("============================")
