"""Prove DSPy and Instructor work for an agent, through the estate model router only.

Founder order 2026-08-31 (docs/tools/dspy-instructor.md). Prints one MEASURED_OK line per tool
or refuses, naming exactly what is missing. The router address comes from ROUTER_URL or the
estate zone in the environment; the key from ROUTER_KEY or ROUTER_KEY_FILE — never printed.
"""

import os
import pathlib
import sys


def router() -> tuple[str, str]:
    url = os.environ.get("ROUTER_URL", "").rstrip("/")
    if not url:
        zone = os.environ.get("ESTATE_ZONE", "")
        if not zone:
            raise SystemExit(
                "refused: set ROUTER_URL, or ESTATE_ZONE so the address can be derived"
            )
        url = f"https://llm.{zone}"
    key_file = os.environ.get("ROUTER_KEY_FILE", "")
    key = (
        pathlib.Path(key_file).read_text().strip()
        if key_file
        else os.environ.get("ROUTER_KEY", "") or os.environ.get("LITELLM_API_KEY", "")
    )
    if not key:
        raise SystemExit("refused: set ROUTER_KEY_FILE (a file) or ROUTER_KEY")
    return url, key


def main() -> int:
    url, key = router()
    lane = os.environ.get("SMOKE_LANE", "groq-fast")

    import dspy
    import instructor
    from openai import OpenAI
    from pydantic import BaseModel

    class Person(BaseModel):
        name: str
        age: int

    client = instructor.from_openai(OpenAI(base_url=f"{url}/v1", api_key=key))
    person = client.chat.completions.create(
        model=lane,
        response_model=Person,
        messages=[{"role": "user", "content": "Ada Lovelace was 36 when she died."}],
    )
    if not (person.name.lower().startswith("ada") and person.age == 36):
        raise SystemExit(f"instructor wrong extraction: {person!r}")
    print(f"instructor MEASURED_OK lane={lane}: {person!r}")

    dspy.configure(lm=dspy.LM(f"openai/{lane}", api_base=f"{url}/v1", api_key=key, max_tokens=100))
    out = dspy.Predict("question -> answer")(question="What is 2+2? Answer with one number.")
    if "4" not in out.answer:
        raise SystemExit(f"dspy wrong answer: {out!r}")
    print(f"dspy MEASURED_OK lane={lane}: answer={out.answer!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
