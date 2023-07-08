import os
import requests

def download_file(url, output_file):
    # URLからファイルをダウンロードしてoutput_fileに保存する関数
    response = requests.get(url)
    with open(output_file, "wb") as f:
        f.write(response.content)

def download_files(repo_id, subfolder, files, cache_dir):
    # リポジトリから指定されたファイルをダウンロードする関数
    for file in files:
        url = f"https://huggingface.co/{repo_id}/resolve/main/{subfolder}/{file}"
        output_file = os.path.join(cache_dir, file)
        if not os.path.exists(output_file):
            print(f"{file} を {url} から {output_file} にダウンロードしています...")
            download_file(url, output_file)
            print(f"{file} のダウンロードが完了しました！")
        else:
            print(f"{file} は既にダウンロードされています")

def check_and_download_model(model_dir, model_id, sub_dirs, files):
    # モデルディレクトリが存在しない場合、モデルをダウンロードする
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
        print(f"モデルを {model_dir} にダウンロードしています。モデルID: {model_id}")

        # サブディレクトリごとにファイルをダウンロードする
        for sub_dir, sub_dir_files in sub_dirs:
            sub_dir_path = os.path.join(model_dir, sub_dir)
            if not os.path.exists(sub_dir_path):
                os.makedirs(sub_dir_path)
            download_files(model_id, sub_dir, sub_dir_files, sub_dir_path)

        # ルートディレクトリのファイルをダウンロードする
        for file in files:
            url = f"https://huggingface.co/{model_id}/resolve/main/{file}"
            output_file = os.path.join(model_dir, file)
            if not os.path.exists(output_file):
                print(f"{file} を {url} から {output_file} にダウンロードしています...")
                download_file(url, output_file)
                print(f"{file} のダウンロードが完了しました！")
            else:
                print(f"{file} は既にダウンロードされています")

        print("モデルのダウンロードが完了しました。")
    else:
        print("モデルは既にダウンロード済みです。")

def download_diffusion_model_Secta_hakoMayD(model_dir):
    MODEL_ID = "tori29umai/Secta_hakoMayD_diffusers"
    SUB_DIRS = [
        ("feature_extractor", ["preprocessor_config.json"]),
        ("scheduler", ["scheduler_config.json"]),
        ("text_encoder", ["config.json", "pytorch_model.bin"]),
        ("tokenizer", ["merges.txt", "special_tokens_map.json", "tokenizer_config.json", "vocab.json"]),
        ("unet", ["config.json", "diffusion_pytorch_model.bin"]),
    ]
    FILES = ["model_index.json"]

    check_and_download_model(model_dir, MODEL_ID, SUB_DIRS, FILES)

def download_diffusion_model_unlimited_replicant(model_dir):
    MODEL_ID = "alfredplpl/unlimited-replicant"
    SUB_DIRS = [
        ("scheduler", ["scheduler_config.json"]),
        ("text_encoder", ["config.json", "model.safetensors"]),
        ("tokenizer", ["merges.txt", "special_tokens_map.json", "tokenizer_config.json", "vocab.json"]),
        ("unet", ["config.json", "diffusion_pytorch_model.safetensors"]),
        ("vae", ["config.json", "diffusion_pytorch_model.safetensors"]),
    ]
    FILES = ["model_index.json","preprocessor_config.json"]
    check_and_download_model(model_dir, MODEL_ID, SUB_DIRS, FILES)


def download_vae_model(model_dir):
    MODEL_ID = "tori29umai/sd_vae_ft_ema_diffusers"
    FILES = ["config.json", "diffusion_pytorch_model.bin"]

    check_and_download_model(model_dir, MODEL_ID, [], FILES)

def download_controlnet_shadow_model(model_dir):
    MODEL_ID = "tori29umai/control_v11p_sd21_shadow_diffusers"
    SUB_DIRS = [
        ("control_v11p_sd21_shadow_front", ["config.json", "diffusion_pytorch_model.safetensors"]),
    ]
    check_and_download_model(model_dir, MODEL_ID, SUB_DIRS, [])

def download_controlnet_normalmap_model(model_dir):
    MODEL_ID = "tori29umai/control_v11p_sd21_normalmap_diffusers"
    SUB_DIRS = [
        ("control_v11p_sd21_normalmap", ["config.json", "diffusion_pytorch_model.safetensors"]),
    ]
    check_and_download_model(model_dir, MODEL_ID, SUB_DIRS, [])

def download_contolnet_canny_model(model_dir):
    MODEL_ID = "thibaud/controlnet-sd21-canny-diffusers"
    FILES = ["config.json","diffusion_pytorch_model.bin"]
    check_and_download_model(model_dir, MODEL_ID, [], FILES)

def download_textual_inversion_model(model_dir):
    MODEL_ID = "852wa/hakoMay"
    FILES = ["Mayng.safetensors","Mayng.yaml"]

    check_and_download_model(model_dir, MODEL_ID, [], FILES)

def download_tagger_model(model_dir):
    MODEL_ID = "SmilingWolf/wd-v1-4-convnext-tagger-v2"
    SUB_DIRS = [
        ("variables", ["variables.data-00000-of-00001", "variables.index"]),
    ]
    FILES = ["keras_metadata.pb", "saved_model.pb", "selected_tags.csv"]

    check_and_download_model(model_dir, MODEL_ID, SUB_DIRS, FILES)

if __name__ == "__main__":
    stable_diffusion_Secta_hakoMayD_path = "Models/Stable-diffusion/Secta_hakoMayD_diffusers"
    download_diffusion_model_Secta_hakoMayD(stable_diffusion_Secta_hakoMayD_path )

    vae_path = "Models/vae/sd_vae_ft_ema_diffusers"
    download_vae_model(vae_path)

    controlnet_shadow_path = "Models/controlnet"
    download_controlnet_shadow_model(controlnet_shadow_path)

    controlnet_normalmap_path = "Models/controlnet"
    download_controlnet_normalmap_model(controlnet_normalmap_path)

    contolnet_canny_path = "Models/controlnet/control_v11p_sd21_canny"
    download_contolnet_canny_model(contolnet_canny_path)

    textual_inversion_path = "Models/textual_inversion/hakoMay"
    download_textual_inversion_model(textual_inversion_path)

    tagger_path = "Models/wd14_tagger_model"
    download_tagger_model(tagger_path)
