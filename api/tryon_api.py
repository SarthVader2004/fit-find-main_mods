from fastapi import APIRouter, UploadFile, Form
from fastapi.responses import JSONResponse
from gradio_client import Client, handle_file
from dotenv import load_dotenv
import tempfile
import shutil
import os
from datetime import datetime
import traceback  # ✅ Added to print full stack trace

router = APIRouter(prefix="/tryon", tags=["Virtual Try-On"])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
load_dotenv(dotenv_path=os.path.join(ROOT_DIR, ".env"))

HF_TOKEN = os.getenv("HF_TOKEN")
client = Client("yisol/IDM-VTON", hf_token=HF_TOKEN)

STATIC_DIR = os.path.join(ROOT_DIR, "static")
os.makedirs(STATIC_DIR, exist_ok=True)


@router.post("/")
async def try_on(
    background: UploadFile,
    garment: UploadFile,
    garment_desc: str = Form("A stylish outfit"),
):
    """Perform virtual try-on."""
    bg_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    garm_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")

    try:
        shutil.copyfileobj(background.file, bg_temp)
        shutil.copyfileobj(garment.file, garm_temp)
        background.file.close()
        garment.file.close()
        bg_temp.close()
        garm_temp.close()

        print("🚀 Running IDM-VTON prediction...")
        result = client.predict(
            dict={"background": handle_file(bg_temp.name), "layers": [], "composite": None},
            garm_img=handle_file(garm_temp.name),
            garment_des=garment_desc,
            is_checked=True,
            is_checked_crop=False,
            denoise_steps=30,
            seed=42,
            api_name="/tryon",
        )

        print("🧠 IDM-VTON raw output:", result)

        normalized_results = []
        if isinstance(result, (list, tuple)):
            for item in result:
                if isinstance(item, (list, tuple)):
                    normalized_results.extend(item)
                else:
                    normalized_results.append(item)
        elif isinstance(result, str):
            normalized_results = [result]

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_urls = []
        for i, path in enumerate(normalized_results):
            path = os.path.normpath(path)
            label = (
                "masked_person"
                if i == 0
                else "warped_garment"
                if i == 1
                else "final_composite"
            )
            filename = f"{timestamp}_{label}.png"
            dest = os.path.join(STATIC_DIR, filename)
            shutil.copy(path, dest)
            result_urls.append(
                {"label": label, "url": f"http://127.0.0.1:8000/static/{filename}"}
            )

        return {
            "status": "✅ Success",
            "description": "Final try-on result labeled 'final_composite'.",
            "results": result_urls,
        }

    except Exception as e:
        print("\n❌ ERROR IN TRY-ON ENDPOINT:")
        traceback.print_exc()  # ✅ This prints the full traceback to the terminal
        print("❌ Exception message:", str(e))
        return JSONResponse(content={"error": str(e)}, status_code=500)

    finally:
        # Always clean up temporary files safely
        try:
            os.unlink(bg_temp.name)
            os.unlink(garm_temp.name)
        except Exception:
            pass
