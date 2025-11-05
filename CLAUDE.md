To orient read @README.md
- Never write defensive code.
  - *Never use try/except clauses unless you clarify with me first*
  - Never use kwargs with defaults. use args
  - Never have return types that can be {type} | None
  - Never add logic to support backwards compatibility
  - Never use some_dict.get() with a default to avoid crashing. just crash if an expected key is not there
  - If you hit an error and your instinct is to add defensive logic, instead add logging to help clarify the root cause of the error so it can be identified and later fixed, rather than suppressed
  - Be decisive. Don't implement a fn like this: def fetch_wikipedia_snapshots(page_name: str, dates: list[str | date]) -> None: that can defensively take multiple types of args. implement def fetch_wikipedia_snapshots(page_name: str, dates: list[date])
- Never truncate inputs/outputs/diffs
- return types should basically always just be one thing or a list of things, possibly a tuple. never object | other_object or object | None
- lean on pydantic models rather than dicts/dataclasses
- be a ruthless editor. try very hard to write only the bare essential logic. 
- if your function args or return types are numerous or convoluted, scrutinize why and fix things. you should basically never be returning list[tuple[str, datetime]], for example.
  - You never use kwargs -- just args, unless you check with me first.
- If one of my instructions does not make sense, do not implement it. Ask for clarification or explain why an instruction doesn't make sense
- If you're in the middle of a task and you realize something could use clarification, stop and ask for clarification or choose the best option (if one is obvious). Don't implement something that might work for either. 
- If you're creating a new file, before starting to code think critically about what interfaces make the most sense with the existing code base. Keep things as simple as possible.
- You may drive-by simplify if you notice opportunities, but only for true, small simplifications
- if you're doing a no-op refactoring job for pure code simplification and get to the end, check that you did actually make the code simpler. if not, consider reverting your change and (maybe) trying again
- aggregated metrics should NOT be stored if they can be easily calculated on the fly
- use uvr to make sure environment vars and pythonpath is correct. 
- always operate from the git root directory
- a new openai api is out and you should use that @openai_api_docs.md
- for websearch enabled apis see @how-to-websearch-api.md
- dont use emojis
- if i ask a question, do investigation required to answer my question, and then come back and respond to me. Dont make changes before responding to my question
- when adding things to a streamlit app, less is more. keep the UI simple and uncluttered. add only important functionality,headers,text etc
- never do sys.path.insert(0, str(Path(__file__).parent.parent.parent)). if there are path problems surface them to me
- when creating scripts that might take more than 10s always include some kind of stdout progress tracking, even if primitive

There are new models out since your training cut off
      # OpenAI 
        [
            "openai/gpt-5",
            "openai/gpt-5-mini",
            "openai/gpt-5-nano",
        ],
        # Anthropic models
        [
            "anthropic/claude-opus-4-1-20250805",
            "anthropic/claude-sonnet-4-5-20250929",
            "anthropic/claude-sonnet-4-20250514",
        ],
        # Google models
        [
            "google/gemini-2.5-flash",
            "google/gemini-2.5-pro",
        ],
        # Grok models
        [
            "grok/grok-4-0709",
            "grok/grok-4-fast-reasoning",
            "grok/grok-4-fast-non-reasoning",
            "grok/grok-3,

        ]

For getting structured model output always use pydantic models

use UV add to install packages. 
**TO RUN PYTHON CODE*
i created a uvr alias to uv run with local env file --env-file .env
uvr section_regeneration/section_writer.py

