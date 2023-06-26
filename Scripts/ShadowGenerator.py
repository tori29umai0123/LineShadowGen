import torch
from diffusers import AutoencoderKL, StableDiffusionControlNetPipeline, StableDiffusionControlNetPipeline, ControlNetModel
from torch import autocast
from PIL import Image, ImageOps, ImageEnhance
import numpy as np

CUDA_DEVICE = 'cuda'

def round_to_multiple_of_8(value):
    # 値を8の倍数に丸める
    return (value // 8) * 8

def resize_image(image, max_size):
    # 画像を指定した最大サイズにリサイズする
    old_width, old_height = image.size
    new_max_size = round_to_multiple_of_8(max_size)
    aspect_ratio = old_width / old_height

    if aspect_ratio >= 1:
        if old_width > old_height:
            new_width = new_max_size
            new_height = int(round(new_width / aspect_ratio))
        else:
            new_height = new_max_size
            new_width = int(round(new_height * aspect_ratio))
    else:
        if old_height > old_width:
            new_height = new_max_size
            new_width = int(round(new_height * aspect_ratio))
        else:
            new_width = new_max_size
            new_height = int(round(new_width / aspect_ratio))

    # リサイズされた画像と元の幅と高さを返す
    resized_image = image.resize((new_width, new_height))
    return resized_image, old_width, old_height

def trim_image_with_mask(init_image, mask_image):
    old_width, old_height = init_image.size
    # 画像とマスクを配列に変換
    image_array = np.array(init_image)
    mask_array = np.array(mask_image)
    # マスクの非ゼロ要素のインデックスを取得
    nonzero_indices = np.nonzero(mask_array)
    min_row, min_col = np.min(nonzero_indices[0]), np.min(nonzero_indices[1])
    max_row, max_col = np.max(nonzero_indices[0]), np.max(nonzero_indices[1])
    # トリミングされた画像の配列を作成
    trimmed_image_array = image_array[min_row: max_row + 1, min_col: max_col + 1]
    # トリミングされた画像をPILイメージに変換
    trimmed_image = Image.fromarray(trimmed_image_array)
    # 初期画像の幅と高さを返す
    init_width, init_height = init_image.size
    return trimmed_image, min_row, min_col, init_width, init_height, old_width / old_height

def restore_trim_size(resized_image, trimmed_width, trimmed_height):
    # リサイズされた画像のサイズを元のトリミングされたサイズに復元
    restored_size_image = resized_image.resize((trimmed_width, trimmed_height))
    return restored_size_image

def restore_image_size(image, init_width, init_height, max_size):
    max_dim = max_size
    restored_image = image.resize((init_width, init_height))
    restored_image = restored_image.resize(calculate_resized_dimensions(restored_image.size, max_dim))
    return restored_image

def restore_image_trim(trimmed_image, init_width, init_height, min_row, min_col):
    # 元の画像と同じサイズの新しい空の画像を作成（白で塗りつぶす）
    original_image = Image.new("RGB", (init_width, init_height), (255, 255, 255))
    # トリミングされた画像を正しい位置に貼り付ける
    original_image.paste(trimmed_image, (min_col, min_row))
    # 復元されたトリミング画像を返す
    restored_trim_image = original_image
    return restored_trim_image

def restore_image_mask(restored_trim_image, mask_image, init_image, max_size):
    # restored_trim_image、mask_image、init_imageのアスペクト比を崩さずにmax_sizeを長辺の値にする
    max_dim = max_size
    restored_trim_image = restored_trim_image.resize(calculate_resized_dimensions(restored_trim_image.size, max_dim))
    mask_image = mask_image.resize(calculate_resized_dimensions(mask_image.size, max_dim))
    init_image = init_image.resize(calculate_resized_dimensions(init_image.size, max_dim))

    # 画像をNumPy配列に変換
    restored_array = np.array(restored_trim_image)
    mask_array = np.array(mask_image)
    init_array = np.array(init_image)

    # マスク画像が白い部分を特定（RGBすべてが255の部分）
    white_area = np.all(mask_array == [255, 255, 255], axis=-1)

    # 白い部分でのrestored_arrayの値をinit_arrayに代入
    init_array[white_area] = restored_array[white_area]

    # 修復された画像をPILオブジェクトに変換して返す
    restored_image = Image.fromarray(init_array)
    return restored_image

def restore_image_process(image, trimmed_width, trimmed_height, min_row, min_col, mask_image, init_image, max_size):
    # Restore trim size
    restored_size_image = restore_trim_size(image, trimmed_width, trimmed_height)
    # Restore image trim
    init_width, init_height = init_image.size
    restored_trim_image = restore_image_trim(restored_size_image, init_width, init_height, min_row, min_col)
    # Restore image mask
    restored_image = restore_image_mask(restored_trim_image, mask_image, init_image, max_size)
    return restored_image

def calculate_resized_dimensions(image_size, max_dim):
    width, height = image_size
    if width > height:
        new_width = max_dim
        new_height = int(height * max_dim / width)
    else:
        new_width = int(width * max_dim / height)
        new_height = max_dim
    return new_width, new_height

# メインのロジック

def set_torch_cuda_memory_allocation():
    torch.cuda.memory._set_allocator_settings("max_split_size_mb:100")

def load_counterfeit_autoencoder():
    return AutoencoderKL.from_pretrained('Models/vae/sd_vae_ft_ema_diffusers/', torch_dtype=torch.float16).to(CUDA_DEVICE)

def load_model_from_pretrained_path(path):
    return ControlNetModel.from_pretrained(path, torch_dtype=torch.float16).to(CUDA_DEVICE)

def load_pipeline(vae, control_net, control_net_canny):
    return StableDiffusionControlNetPipeline.from_pretrained(
        "Models/Stable-diffusion/Secta_hakoMayD_diffusers",
        controlnet=[control_net, control_net_canny],        
        vae=vae,
        revision="fp16", 
        torch_dtype=torch.float16,
    )

def main(init_image, mask_image, MaskON, max_size,prompt):
    torch.cuda.empty_cache()
    set_torch_cuda_memory_allocation()
    vae = load_counterfeit_autoencoder()

    control_model_path = "Models/controlnet/control_v11p_sd21_shadow_front"
    control_net = load_model_from_pretrained_path(control_model_path)

    control_model_canny_path = "Models/controlnet/control_v11p_sd21_canny"
    control_net_canny = load_model_from_pretrained_path(control_model_canny_path)

    pipe = load_pipeline(vae, control_net, control_net_canny).to(CUDA_DEVICE) 
    pipe.load_textual_inversion("Models/textual_inversion/hakoMay", weight_name="Mayng.safetensors", token="Mayng", torch_dtype=torch.float16)
    pipe.enable_attention_slicing("max")
    pipe.enable_xformers_memory_efficient_attention() # required
    pipe.safety_checker = None if pipe.safety_checker is None else lambda images, **kwargs: (images, False)
    negative_prompt = "Mayng, (low quality, worst quality:1.4)"

    if MaskON != False:
        trimmed_image, min_row, min_col, init_width, init_height, init_aspect_ratio = trim_image_with_mask(init_image, mask_image)
        resized_image, trimmed_width, trimmed_height = resize_image(trimmed_image, max_size)
        invert_image = ImageOps.invert(resized_image)

        image = pipe(
            prompt="(greyscale, monochrome:1.4)," + prompt,
            negative_prompt=negative_prompt,
            guidance_scale=7.0,
            num_inference_steps=50,
            image=[resized_image, invert_image]
        ).images[0]

        restored_image = restore_image_process(image, trimmed_width, trimmed_height, min_row, min_col, mask_image, init_image, max_size)
        return restored_image

    else:
        resized_image, init_width, init_height = resize_image(init_image, max_size)
        invert_image = ImageOps.invert(resized_image)

        image = pipe(
            prompt="(greyscale, monochrome:1.4)," + prompt,
            negative_prompt=negative_prompt,
            guidance_scale=7.0,
            num_inference_steps=50,
            image=[resized_image, invert_image]
        ).images[0]
        restored_image = restore_image_size(image, init_width, init_height, max_size)
        return restored_image


if __name__ == "__main__":
    image_path = "1.png"
    mask_path = "1_mask.png"
    init_image = Image.open(image_path).convert("RGB")
    mask_image = Image.open(mask_path).convert("RGB")
    MaskON = True
    max_size = 960
    prompt = "1girl, solo,gloves, short hair, pants, tailcoat,full body, white background, simple background, looking at viewer,smile, long sleeves, standing, holding, formal, flute"
    image = main(init_image, mask_image, MaskON, max_size,prompt)
    image.save("Secta_diffuserss_960.png")