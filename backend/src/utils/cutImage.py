from io import BytesIO
from PIL import Image as PILImage
from reportlab.platypus import Image
from PIL import ImageOps
import io



def cropImage(image_path: str, margin: int = 200, desired_width: int = 400, max_width: int = 450, max_height: int = 600) -> Image:


    original_image = PILImage.open(image_path)
    width, height = original_image.size

  
    cropped_image = original_image.crop((
        margin,            
        margin,           
        width - margin,    
        height - margin     
    ))
    
    aspect = cropped_image.width / cropped_image.height

    if aspect >= 1:  
        new_width = min(max_width, cropped_image.width)
        new_height = new_width / aspect
    else: 
        new_height = min(max_height, cropped_image.height)
        new_width = new_height * aspect

    img_buffer = io.BytesIO()
    cropped_image.save(img_buffer, format="PNG")
    img_buffer.seek(0)

    cropped_image = ImageOps.expand(cropped_image, border=1, fill='black')
    
    
    img_buffer = BytesIO()
    cropped_image.save(img_buffer, format="PNG")
    img_buffer.seek(0)


 
    return Image(img_buffer, width=new_width, height=new_height)
