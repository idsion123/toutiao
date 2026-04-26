import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException


# 允许的图片格式
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
# 最大文件大小 (5MB)
MAX_FILE_SIZE = 5 * 1024 * 1024
# 上传目录 - 使用 media 而不是 static
UPLOAD_DIR = Path("media/avatars")


def validate_image(file: UploadFile) -> None:
    """
    验证上传的文件是否为合法图片
    """
    # 检查文件扩展名
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件格式，仅支持: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # 检查文件大小
    file.file.seek(0, 2)  # 移动到文件末尾
    file_size = file.file.tell()
    file.file.seek(0)  # 重置文件指针

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"文件大小超过限制（最大{MAX_FILE_SIZE // 1024 // 1024}MB）"
        )


async def save_upload_file(file: UploadFile, subdirectory: str = "avatars") -> str:
    """
    保存上传的图片文件
    参数:
        file: 上传的文件
        subdirectory: 子目录名称（如 avatars, news 等）
    返回: 图片的访问URL路径
    """
    # 构建上传目录路径
    upload_dir = Path("media") / subdirectory
    upload_dir.mkdir(parents=True, exist_ok=True)

    # 生成唯一文件名，避免冲突
    file_extension = Path(file.filename).suffix.lower()
    unique_filename = f"{uuid.uuid4().hex}{file_extension}"
    file_path = upload_dir / unique_filename

    # 读取并保存文件
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    # 返回访问URL（相对于/media的路径）
    return f"/media/{subdirectory}/{unique_filename}"


