from models.open_model import OpenAIClient
from models.mapping import model_path
from config import cfg


def get_model(args):
    model_name = model_path.get(args.model, None)
    if args.model in ["GPT-4o", "Gemini-1.5-Flash", "Claude-3.5-Sonnet"]:
        model = OpenAIClient(
            base_url=cfg.OPENAI.URL,
            api_key=cfg.OPENAI.KEY.get(args.model),
            prompt=args.prompt,
            model=model_name,
            temperature=args.temperature,
        )
    else:
        raise ValueError(f"Model {args.model} not supported.")
    return model